"""Get a list of Threads from the user's mailbox.
"""

from apiclient import errors
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import email
import re
import os
import shutil
import time
import src.lib.base as base


class CheckEmail(object):
    def ListMessagesMatchingQuery(self, service, user_id, query=''):
        """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
        try:
            response = service.users().messages().list(userId=user_id,
                                                       q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print('An error occurred in ListMessagesMatchingQuery: %s' % error)
            return None

    def GetMimeMessage(self, service, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A MIME Message, consisting of data from Message.
      """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id,
                                                     format='full').execute()

            # print ('Message snippet: %s' % message['snippet'])

            msg_str = base64.urlsafe_b64decode(message['payload']['body']['data'].encode('ASCII'))

            mime_msg = email.message_from_string(msg_str.decode())

            return mime_msg
        except errors.HttpError as error:
            print('An error occurred in GetMimeMessage: %s' % error)

    def TrashMessage(self, service, user_id, msg_id):
        """Get a Thread.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        thread_id: The ID of the Thread required.

      Returns:
        Thread with matching ID.
      """
        try:
            # thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
            thread = service.users().messages().trash(userId=user_id, id=msg_id).execute()
            print(('message id: %s - is successfully moved to trash!') % (msg_id))
            return thread
        except errors.HttpError as error:
            print('An error occurred in TrashMessage: %s' % error)

    def get_mpart(self, mail):
        maintype = mail.get_content_maintype()
        if maintype == 'multipart':
            for part in mail.get_payload():
                # This includes mail body AND text file attachments.
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
            # No text at all. This is also happens
            return ""
        elif maintype == 'text':
            return mail.get_payload()

    def get_mail_body(self, mail):
        """
        There is no 'body' tag in mail, so separate function.
        :param mail: Message object
        :return: Body content
        """
        body = ""
        if mail.is_multipart():
            # This does not work.
            # for part in mail.get_payload():
            #    body += part.get_payload()
            body = self.get_mpart(mail)
        else:
            body = mail.get_payload()
        return body

    def get_auth(self):
        email_add = base.config['email_add']
        SCOPES = base.config['SCOPES']
        store = file.Storage(base.config['storage_file'])
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(base.config['client_secret'], SCOPES)
            creds = tools.run_flow(flow, store)
        service = discovery.build(base.config['mail'], base.config['m_version'], http=creds.authorize(Http()),
                                  cache_discovery=False)
        return email_add, service

    def get_email(self, typ, email_file, search_duration, name, broker=None):
        email_add, service = self.get_auth()
        typ = typ.lower()
        if "customized quote" in typ or "customizedquote" in typ:
            q = base.config['q_sub_cq'] + " " + broker
        elif "self-service quote" in typ:
            q = base.config['q_sub_ssq'] + " " + broker
        elif "baa" in typ:
            q = base.config['q_sub_baa'] + " " + broker
        elif "shopping cart quote" in typ:
            q = base.config['q_sub_scq'] + " " + broker
        elif "osign" in typ:
            q = base.config['q_sub_osign']
        messages = None
        timeout = None
        url = None
        exp_title = None
        check_duration = time.time() + search_duration
        while not messages:
            messages = self.ListMessagesMatchingQuery(service, email_add, query=q)
            if time.time() > check_duration:
                timeout = 'search_limit_reached'
                break
        if timeout:
            url, exp_title, uid = timeout
            return url, exp_title, uid
        id_ = []
        for list in messages:
            for key in list:
                if key == 'id':
                    id_.append(list[key])
        for id in id_:  # Gets the MIMEMessage for each message id
            getmimemessage = self.GetMimeMessage(service, email_add, id)
            body = self.get_mail_body(getmimemessage)
            if str(name).lower() in str(body).lower():
                """Gets the url"""
                regex = 'href=\"(.*?)\">here'
                matches = re.search(regex, str(body))
                url = matches.group(1)
                """Gets the page title"""
                regex = '<title>(.*?)</title>'
                matches = re.search(regex, str(body))
                exp_title = matches.group(1)
                i_d = id
                break
            else:
                continue
        uid = None
        if url:
            """Moves email to trash"""
            self.TrashMessage(service, email_add, i_d)
            """Gets the uid"""
            # regex = 'ID=(.*?)$'    #Extracting Unique ID from link
            # matches = re.search(regex, str(body))
            # uid = matches.group(1)
            if base.config['execution'] == 'local':
                file_html = open(email_file, 'w')
                file_html.write(body)  # str() converts to string
                file_html.close()
                email_folder = "emails"
                email_dir = os.path.join(os.getcwd(), email_folder)
                if not os.path.exists(email_dir):
                    os.makedirs(email_dir)
                e_file = os.path.join(os.getcwd(), email_file)
                if os.path.exists(os.path.join(email_dir, email_file)):
                    os.remove(os.path.join(email_dir, email_file))
                shutil.move(e_file, email_dir)
        print('URL = ', url, 'Title = ', exp_title)
        return url, exp_title, uid

    def clear_emails(self):
        email_add, service = self.get_auth()
        q = 'label:UNREAD'
        messages = self.ListMessagesMatchingQuery(service, email_add, query=q)
        id_ = []
        for list in messages:
            for key in list:
                if key == 'id':
                    id_.append(list[key])
        for id in id_:  #Deletes all unread messages
            self.TrashMessage(service, email_add, id)

# if __name__ == '__main__':
#     mail = CheckEmail()
#     mail.get_link("Customized Quote")
