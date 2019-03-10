import json
from typing import *
class Transaction:

    def __init__(self,sender1:str,receive1:str,amount1:int):
        self.sender=sender1
        self.receiver=receive1
        self.amount=amount1
    def toJsonStr(self):
        return {
            'sender':self.sender,
            'receiver':self.receiver,
            'amount':self.amount
        }