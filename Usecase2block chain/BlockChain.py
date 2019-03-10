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