from typing import List
from Block import Block
from fastapi import FastAPI
from time import time

from Blockchain import Blockchain
from Block import Block
from Transaction import Transaction
from threading import Thread


def mining_task(blockchain: Blockchain):
    while True:
        start = time()
        blockchain.create_block()
        print("Time elapsed to mine block {} ms".format(time() - start))


app = FastAPI()
chain = Blockchain()
Thread(target=mining_task, args=(chain,)).start()
    
@app.get("/blocks")
async def get_blocks() -> List[Block]:
    return [block.as_dict() for block in chain.blocks]


@app.get("/blocks/{index}")
async def get_block(index: int) -> Block:
    return chain.blocks[index].as_dict()

@app.get("/transactions")
async def get_transactions() -> List[Transaction]:
    return [transaction.as_dict() for transaction in chain.transactions]

@app.post("/transactions/new")
async def new_transaction(transaction: dict):
    try:
        t = Transaction.from_dict(transaction)
    except ValueError:
        return {"error": "Invalid transaction"}

    return chain.add_transaction(t.sender, t.recipient, t.amount).as_dict()

@app.get("wallet/{address}/balance")
async def get_balance(address: str) -> float:
    pass

@app.get("wallet/{address}/transactions")
async def get_transactions(address: str) -> float:
    pass