import getopt
import sys
from datetime import datetime
from random import randint
from zeep import Client


def get_content(num=5, c=None):
    client = Client("http://model.internalservice.uhone.com/ContentManagement/ContentManagement.asmx?WSDL")
    use_states = []
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
        "ME", "LA", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
        "OR", "OK", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "VI", "WA", "WV", "WI", "WY"
    ]
    content_codes = [
        {"ContentCode": "Quote.QuotePerson.DTC.Title"},
        {"ContentCode": "Quote.Header.Title"},
        {"ContentCode": "Footer.Disclaimers"},
        {"ContentCode": "Quote.ExpandYourCoverageModal.Header.Text"},
        {"ContentCode": "Quote.Product.BrochureLink.Text"}
    ]
    expected = {
        '003': {
            'Quote.Header.Title': 'UHOne',
            'Quote.QuotePerson.DTC.Title': 'Find the Plan that Fits Your Situation',
            'Footer.Disclaimers': 'Most products and services are underwritten by Golden Rule Insurance Company.',
            'Quote.ExpandYourCoverageModal.Header.Text': 'Expand Your Coverage',
            'Quote.Product.BrochureLink.Text': 'Plan Benefits, Exclusions, Limitations'
        },
        '055': {
            'Quote.Header.Title': '',
            'Quote.QuotePerson.DTC.Title': '',
            'Footer.Disclaimers': '',
            'Quote.ExpandYourCoverageModal.Header.Text': '',
            'Quote.Product.BrochureLink.Text': ''
        },
        '088': {
            'Quote.Header.Title': '',
            'Quote.QuotePerson.DTC.Title': '',
            'Footer.Disclaimers': '',
            'Quote.ExpandYourCoverageModal.Header.Text': '',
            'Quote.Product.BrochureLink.Text': ''
        },
        '107': {
            'Quote.Header.Title': 'UHOne',
            'Quote.QuotePerson.DTC.Title': 'Find the Plan that Fits Your Situation',
            'Footer.Disclaimers': 'Core Access fixed indemnity plans are underwritten by '
                                  'Independence American Insurance Company and administered by The Loomis Company',
            'Quote.ExpandYourCoverageModal.Header.Text': 'Expand Your Coverage',
            'Quote.Product.BrochureLink.Text': 'Plan Benefits, Exclusions, Limitations'
        },
        '777': {
            'Quote.Header.Title': 'Health Insurance and Personalized Healthcare Re-imagined',
            'Quote.QuotePerson.DTC.Title': 'Find the Plan that Fits You',
            'Footer.Disclaimers': 'Insurance products and services offered are underwritten by Harken Health '
                                  'Insurance Company',
            'Quote.ExpandYourCoverageModal.Header.Text': '',
            'Quote.Product.BrochureLink.Text': 'View Brochure'
        }
    }
    fail_count = 0
    pass_count = 0
    total = 0

    while len(use_states) <= num-1:
        i = randint(0, len(states)-1)
        if i not in use_states:
            print('')
            print('-' * 100)
            print('')
            use_states.append(i)
            # print states[i]
            e = randint(0, len(content_codes)-1)
            cc = content_codes[e]['ContentCode']
            # print expected[e]
            cr = {
                'CompanyCode': c,
                'State': states[i],
                'ContentCode': cc,
                'ContentDate': datetime.today().strftime('%Y-%m-%d')
            }
            print("ContentRequest: %s" % cr)
            invoke = client.service.GetContent(cr)
            # print invoke
            expected_result = expected[c][cc]
            actual_result = invoke['Content']
            if actual_result is None:
                actual_result = ''
            if expected_result != actual_result and expected_result not in actual_result:
                print("RESULTS: ")
                print('FAILED >>> "%s" != "%s"' % (expected_result, actual_result))
                fail_count += 1
            else:
                print("RESULTS: ")
                print('PASSED >>> Content "%s" is present in "%s"' % (expected_result, actual_result))
                pass_count += 1

    total += len(use_states)
    print('')
    print('='*100)
    print('')
    print('%i PASSED || %i FAILED || %i TOTAL' % (pass_count, fail_count, total))


if __name__ == '__main__':
    n = 5
    c = None
    p = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:c:", ["number", "company"])
    except getopt.GetoptError:
        print('SOAP.py -n <Number of States>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SOAP.py -n <Number of States> -c <003 UHO, 055 NHIC, 088 HCC, 107 IHC, 777 Harken>')
        elif opt == '-n':
            n = int(arg)
            p = True
        elif opt == '-c':
            c = arg
            p = True
    if p:
        get_content(n, c)
