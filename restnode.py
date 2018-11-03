import socket
import select
import threading
import json
import time
import flask
import requests
import random

import blockchain

"""
PEARSCOIN CHAIN TRANSFER PROTOCOL:

MESSAGE TYPES:
 
Message     Description         Response
/chain      Get current chain   JSON chain object

"""

def ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("40.114.26.190", 80)) # doesn't actually send traffic
    ipa = s.getsockname()[0]
    s.close()
    return ipa

def getPort():
    return random.randint(1024, 65535)

class Node:
    def __init__(self, port):
        self.peers = []
        self.chain = blockchain.Blockchain()
        self.chain.genesis()
        self.staging = [] # staging data to add to block

        # socket stuff
        self.port = port

    def consensus(self):
        chains = []
        for peer in peers:
            pass # get that peer's chain
        for chain in chains:
            self.chain.consensus(chain)

    def add_block(self):
        self.chain.add_block(self.staging)

    def add_data(self, data):
        self.staging.append(data)

    def peer(self, addr, port):
        self.peers.append(Peer(addr, port))

    def serve_chain(self, app):
        app.run("0.0.0.0", self.port)

    def check_consensus(self):
        while True:
            for peer in self.peers:
                chain = peer.get_chain()
                if self.chain.consensus(chain):
                    print("Checked chain with {}, ours is right".format(
                                                        (peer.addr, peer.port)))
                else:
                    print("Checked chain with {}, theirs is right".format(
                                                        (peer.addr, peer.port)))
            time.sleep(5)

    def add_blocks(self):
        while True:
            if len(self.staging) > 0:
                print("Mining new block...")
                self.add_block()
                print("Added new block!")
                self.staging = []
            else:
                time.sleep(5)

    def handle_input(self):
        while True:
            cmd = input("> ").split(";")
            if cmd[0] == "peer":
                self.peer(cmd[1], int(cmd[2]))
            if cmd[0] == "txion":
                self.staging.append(cmd[1])
            if cmd[0] == "chain":
                print([block.data for block in self.chain.blocks])

class Peer:
    def __init__(self, address, port):
        self.addr = address
        self.port = port

        
    def get_chain(self):
        print("Fetching chain from {}".format((self.addr, self.port)))
        message = requests.get("http://{}:{}/chain".format(self.addr,
                                                               self.port)).text
        return blockchain.Blockchain.fromjson(message)

def start(listen_port):
    me = Node(listen_port)

    app = flask.Flask(__name__)

    @app.route("/chain")
    def chain():
        return me.chain.jsonrep()

    server_thread = threading.Thread(target=me.serve_chain, args=(app,))
    consensus_thread = threading.Thread(target=me.check_consensus)
    miner_thread = threading.Thread(target=me.add_blocks)
    #input_thread = threading.Thread(target=me.handle_input)

    server_thread.start()
    consensus_thread.start()
    miner_thread.start()
    #me.handle_input()
    return me

