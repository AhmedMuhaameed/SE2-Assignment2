import hashlib
import json
from argparse import ArgumentParser
import requests
from flask import Flask, jsonify,request

from Block import Block
from BlockChain import BlockChain
from Transaction import Transaction


class peer:
    def __init__(self):
        #initialize the chain
        self.blockchain=BlockChain()
        #initialize the Node
        self.neighbours = []
        self.address = 0

    def setAddress(self, addr):
        self.address = addr

    def addNeighbour(self,neighbour):
        #put a neighbour which address is 127.0.0.1:port to a node
        self.neighbours.append(neighbour)

    def validChain(self, chain) -> bool:

        index = 1
        lastBlock = chain[0]
        length = len(chain)
        while index < length:
            block = chain[index]
            #check Hash Value
            lastBlockHash = hashlib.sha256(json.dumps(lastBlock).encode()).hexdigest()
            if block['previous_Hash'] != lastBlockHash:
                return False
            #check proofofwork
            if not self.blockchain.validProof(lastBlock['proof'], block['proof']):
                return False
            lastBlock = block
            index += 1
        return True