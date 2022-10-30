from dataclasses import dataclass, field
from typing import List

from Block import Block
from Transaction import Transaction


@dataclass
class Blockchain(object):
    blocks: List[Block] = field(init=False)
    difficulty: int = field(default=5)
    pool_transactions: List[Transaction] = field(init=False)
    
    def __init__(self):
        self.blocks = []
        self.pool_transactions = []
     
    @property
    def genesis(self):
        return self.blocks[0]
    
    @property
    def last(self):
        return self.blocks[-1]
    
    def add_transaction(self, transaction: dict):
        self.pool_transactions.append(Transaction.from_dict(transaction))
    
    def create_block(self):
        
        transactions = self.pool_transactions.copy()
        transactions.insert(0, Transaction('', '', '', 30))
        
        block = Block(
            self.last.hash if len(self.blocks) != 0 else '',
            len(self.blocks),
            transactions
        )
         
        block.mine(self.difficulty)
        self.blocks.append(block)
        self.pool_transactions = []
        