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
    def fixconflicts(self)->bool:

        #Use the Longest Path of Network
        #if the node replaced return true
        #if not return False

        newChain=None
        #if you are searching about chain have length more than you it's not necessarily to search a chain less than you
        maxLen=len(self.blockchain.chain)
        #Traverse all neighbor nodes, determine the chain of neighbor nodes and their similarities and differences
        #If the chain of neighbor nodes is longer than its own, and the chain is legal, temporarily store this chain as the final
        #longest chain has been obtained after the traversal is the longest chain in the node network

        for node in self.neighbours:
            response = requests.get(
                f'http://localhost:{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > maxLen and self.validChain(chain):
                    maxLen = length
                    newChain = chain
        if newChain:
            self.blockchain.chain = []
            for temp in newChain:
                transactions = []
                transet = temp['transactions']
                for t in transet:
                    transactions.append(Transaction(t['sender'], t['receiver'], int(t['amount'])));
                self.blockchain.chain.append(
                    Block(temp['index'], temp['timestamp'], transactions, temp['proof'], temp['previous_Hash'])
                )
            return True
        return False

peer=peer()
app=Flask(__name__)

@app.route("/chain",methods=['GET'])
def getChain():
    # return ALL Chain information and Blocks
    temp = peer.blockchain.chain
    json_chain = []
    for block in temp:
        json_chain.append(block.toJson())
    response = {
        'chain': json_chain,
        'length': len(temp)
    }
    return jsonify(response), 200

@app.route('/transaction/new',methods=['POST'])
def addNewTransaction():
    def addNewTransaction():
        sender = request.values.get("sender")
        receiver = request.values.get("receiver")
        amount = request.values.get("amount")
        if sender == None or receiver == None or amount == None:
            return "The request parameters you sent are incomplete and cannot be operated.", 400
        index = peer.blockchain.addTransaction(sender, receiver, int(amount))
        response = {
            "Server message ": " added successfully",
            "Block index": index
        }
        return jsonify(response), 201 #created


@app.route("/mine",methods=['GET'])
def mine():

    last_block=peer.blockchain.lastBlock()
    last_proof=last_block.proof
    proof=peer.blockchain.proofWork(last_proof)

    peer.blockchain.addTransaction(sender="Blockchain system",receiver=f'http://127.0.0.1:{peer.address}',amount=1)

    block=peer.blockchain.createBlock(None,proof)

    response={
        "message":"New blocks are formed",
        "index":block.index,
        "transactions":[t.toJsonStr()
                        for t in block.transactions],
        "proof":block.proof,
        "previous_Hash":block.previous_Hash
    }
    return jsonify(response),200 #ok request

@app.route("/neighbour/add",methods=['POST'])
def addNeighbour():
    #accept values from Front End and add it to neighbour node
    node=request.values.get("node")
    print(node)
    print("-----------")
    if node==None:
        return "Parameters incomplete ",400 #bad request
    peer.addNeighbour(node)
    response={
        "peer added successfully",
        "node address:",peer.address,
        "number of nighbour nodes:",len(peer.neighbours)
    }
    return jsonify(response),200 #Ok Request

@app.route("/consensus")
def consensus():
    replaced=peer.fixconflicts()
    if replaced:
        response={
            "message":"Chain is updated",
            "length":len(peer.blockchain.chain)
        }
    else:
        response={
            "message":"Keep the chain unchanged",
            "length":len(peer.blockchain.chain)
        }
    return jsonify(response),200
if __name__ == '__main__':

    parser=ArgumentParser()
    parser.add_argument("-p","--port",default=5000,type=int,help="Listening port")
    port=parser.parse_args().port
    peer.setAddress(port)
    app.run(host='127.0.0.1',port=port)
