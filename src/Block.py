
from typing import List
from dataclasses import dataclass, field
from time import time
from functools import reduce
from hashlib import sha256
import sys
from random import randrange

from Transaction import Transaction


@dataclass
class Block(object):
    hash: str = field(init=False, default='')
    previous_hash: str
    merkle_tree: str = field(init=False, default='')
    height: int
    nonce: int = field(init=False, default=randrange(sys.maxsize))
    transactions: List[Transaction]
    timestamp: int = field(default=time())
    
    def __post_init__(self):
        self.hash = self.compute_hash()
        self.merkle_tree = self.compute_merkle_tree()

    @staticmethod
    def from_dict(dict: dict):
        
        required = ['pervious_hash', 'height', 'nonce', 'transactions', 'timestamp']
        if not all(key in dict for key in required):
            raise ValueError("Invalid block")
        
        return Block(
            dict['pervious_hash'],
            dict['height'],
            dict['nonce'],
            [Transaction.from_dict(key) for key in required['transactions']],
            dict['timestamp']
        )
     
    def compute_hash(self) -> str:
        dict = self.as_dict()
        dict.pop('hash', None)
        
        return sha256(str(dict).encode()).hexdigest()
    
    def compute_merkle_tree(self) -> str:        
        return reduce(self.__inner_compute_merkle_tree, [tr.hash for tr in self.transactions])
    
    def __inner_compute_merkle_tree(self, a: bytes, b: bytes):
        return sha256(
                bytearray(a).append(b)
            ).hexdigest()
        
    def mine(self, difficulty: int):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()
        
    def as_dict(self) -> dict:
        return {
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'merkle_tree': self.merkle_tree,
            'height': self.height,
            'nonce': self.nonce,
            'transactions': [tx.as_dict() for tx in self.transactions],
            'timestamp': self.timestamp
        }
    
    def __repr__(self) -> str:
        return str(self.as_dict())

