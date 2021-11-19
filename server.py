import html
import time
from multiprocessing.pool import ThreadPool
import subprocess

import src.lib.imgdiff as imgdiff
import src.lib.base as base
import src.lib.config as configs
from src.lib.remote import SauceHelper
from src.lib.websocket_server import WebsocketServer


configs.setup_configs(option='username')
configs.setup_configs(option='access_key')


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")
    base.ws['server'] = server
    # base.ws['client'] = client


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s" % (client['id'], message))

    server.send_message_to_all("Preparing to run Automation with parameters: %s" % message)
    automate = subprocess.run("python -m pytest %s" % message, stdout=subprocess.PIPE)
    stdout = automate.stdout.decode('utf-8')
    print(stdout)
    server.send_message_to_all(html.escape(stdout))
    exit_code = automate.returncode
    # exit_code = 0
    server.send_message_to_all("Automation Exit Code: %s" % str(exit_code))

    if exit_code <= 1 and 'collect-only' not in message:
        base_flag = ""
        if "baseline" in message:
            base_flag = "--baseline"
        visual = subprocess.run("python visual.py .\\reports\\repots.json %s" % base_flag)
        print(visual.stdout.decode('utf-8'))

    server.send_message_to_all("----- Message End -----")


PORT = 9001
server = WebsocketServer(PORT, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.timeout = 42000
server.run_forever()
