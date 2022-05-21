import json
import logging
import sys
import time
import hashlib

import utils

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

    
def _print(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            print(f'{k:15}{v}')
    print(f'{"*"*25}')


if __name__ == '__main__':
    block_chain = BlockChain()
    _print(block_chain.chain)
    block_chain.create_block(5, 'hash 1')
    _print(block_chain.chain)
    block_chain.create_block(2, 'hash 2')
    _print(block_chain.chain)
