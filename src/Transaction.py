from dataclasses import dataclass, field
from hashlib import sha256
from time import time


@dataclass
class Transaction(object):
    hash: str = field(init=False, default="")
    sender: str
    recipient: str
    firm: str
    amount: float
    timestamp: int = field(default=time())
    
    @staticmethod
    def from_dict(transaction: dict) -> 'Transaction':
        return Transaction(
            transaction['sender'],
            transaction['recipient'],
            transaction['firm'],
            transaction['amount'],
            transaction['timestamp']
        )
        
    def __post_init__(self):
        self.hash = self.compute_hash()
    
    def compute_hash(self) -> str:
        dict = self.as_dict()
        dict.pop('hash', None)
        
        bytes = str(dict).encode()
        
        return sha256(bytes).hexdigest()
        
    
    def is_valid(self) -> bool:
        return (
                self.compute_hash() == self.hash
                and self.recipient != self.sender
                and self.amount > 0
        )
    
    def as_dict(self) -> dict:
        return {
            'hash': self.hash,
            'sender': self.sender,
            'recipient': self.recipient,
            'firm': self.firm,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        
    def __repr__(self) -> str:
        return str(self.as_dict())

    