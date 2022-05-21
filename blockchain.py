import json
import logging
import sys
import time
import hashlib

import utils

MINING_DIFFICULTY = 3

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):

    ## NOTE:
    # transactionには、recipientとsenderのblock_chain Address 及び、送金額(value)を入れる
    def __init__(self):
        self.transaction_pool = [] # pool にある程度取引履歴が溜まってから、blockを生成する
        self.chain = []
        self.create_block(0, self.hash({}))
    
    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = [] # Re init
        return block
    
    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True) # Re sort block kaz double check
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self,
        sender_block_chain_address,
        recipient_block_chain_address,
        value
    ):
        transaction = utils.sorted_dict_by_key({
          'sender_block_chain_address': sender_block_chain_address,
          'recipient_block_chain_address': recipient_block_chain_address,
          'value': float(value)
        })
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self,
        transactions,
        previous_hash,
        nonce,
        difficulty=MINING_DIFFICULTY
    ):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0'*difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0 # challenge value
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce


if __name__ == '__main__':
    # init
    block_chain = BlockChain()
    utils._print(block_chain.chain)

    # add transaction
    block_chain.add_transaction('A', "B", 1.0)
    # proof of work
    nonce = block_chain.proof_of_work()
    # create block
    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(nonce, previous_hash)
    utils._print(block_chain.chain)

    # add transaction
    block_chain.add_transaction('A', "B", 2.0)
    block_chain.add_transaction('B', "C", 3.0)
    block_chain.add_transaction('C', "D", 10.0)
    # proof of work
    nonce = block_chain.proof_of_work()
    # create block
    previous_hash = block_chain.hash(block_chain.chain[-1])
    block_chain.create_block(nonce, previous_hash)
    utils._print(block_chain.chain)
