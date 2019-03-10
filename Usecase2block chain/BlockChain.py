import hashlib
import json
from Block import Block
from time import time

from Transaction import Transaction


class BlockChain:
    publicBlock=Block(0,100.01,[],30,"The creation block has no front hash")
    def __init__(self):
        self.transactions=[]
        self.chain=[]
        self.chain.append(BlockChain.publicBlock)
        #self.createBlock(previusHash="111",proof=100)
    def createBlock(self,previusHash:str,proof:int):

        index=len(self.chain)+1
        hashValue=previusHash or self.hash(self.chain[-1])
        block=Block(index,time(),
                    self.transactions,
                    proof,hashValue
                    )
        self.transactions=[]
        self.chain.append(block)
        return block

    def addTransaction(self,sender:str,receiver:str,amount:int)->int:

        newTransaction=Transaction(sender,receiver,amount)
        self.transactions.append(newTransaction)
        return self.lastBlock().index+1
    def hash(self,block)->str:

        blockInfo=json.dumps(block.toJson(),sort_keys=True).encode()
        return hashlib.sha256(blockInfo).hexdigest()

    def proofWork(self,lastProof:int)->int:

        proof=0
        while not self.validProof(lastProof,proof):
            proof+=1
        return proof

    @staticmethod
    def validProof(lastproof:int,proof:int)->bool:

        test=f'{lastproof}{proof}'.encode()
        hashStr=hashlib.sha256(test).hexdigest()
        return hashStr[0:4]=="0000"

    def lastBlock(self):

        try:
            obj=self.chain[-1]
            return obj
        except:
            return None