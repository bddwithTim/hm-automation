# /automation/lib/
import http.client
import json
import glob
import requests

import src.lib.base as base


class Elements(object):
    """
    This Elements class queries the elements to either on a API server or a JSON downloaded file
    """

    def __init__(self):
        self.data = {}
        self.__prep_offline()

    def __prep_offline(self):
        if base.config['server_connection'] == 'offline':
            path = "./Elements_*.json"
            g = glob.glob(path)
            if len(g) >= 1:
                filename = g[len(g) - 1]
                with open(filename, 'r') as data_file:
                    contents = json.load(data_file)

                for content in contents:
                    name = content['Name']
                    value = content['Value']
                    self.data[name] = value

    def get_data(self, name):
        data = not _name_helper(name)
        name = _trim_name(name)

        if data:
            data = name
        else:
            if base.config['server_connection'] == 'offline':
                try:
                    data = self.data[name]
                except KeyError:
                    print("KeyError!")
                except Exception as ex:
                    print(ex)

            elif base.config['server_connection'] == 'online':
                r = requests.get("http://%s/DSA/api/elements?name=%s&min=true" % (base.config['server_address'], name))
                if r.status_code != 200:
                    return False
                data = r.json()['Value']

        return data


def _trim_name(string):
    if _name_helper(string):
        string = string.replace('<', '')
        string = string.replace('>', '')
    string = string.strip()

    return string


def _name_helper(string):
    flag = False
    if '<' in string and '>' in string:
        flag = True

    return flag


def __batch(data):
    server = "localhost"
    port = 56110
    req = http.client.HTTPConnection(server, port)

    for x in data:
        body = json.dumps({
            "Name": x,
            "Value": data[x]
        })
        print(body)
        print("Sending the API Request...")
        req.request('POST', '/api/Elements', body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": ""
                    })
        print("Getting the Response...")
        result = req.getresponse()
        print("Response %s" % result.read())
        print("*" * 100)


def __register(email, password):
    server = "localhost"
    port = 56110
    req = http.client.HTTPConnection(server, port)
    body = json.dumps({
        "Email": email,
        "Password": password,
        "ConfirmPassword": password
    })
    req.request('POST', '/api/Account/Register', body,
                headers={
                    "Content-Type": "application/json"
                })
    print("Getting the Response...")
    result = req.getresponse()
    print(result.status)
    print("Response %s" % result.read())
    print("*" * 100)

if __name__ == '__main__':
    # e = Elements()
    # __batch(e.data)
    __register(email="email", password="password")
