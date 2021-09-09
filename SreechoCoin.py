
import hashlib
import datetime as dt
import json
import requests
from urllib.parse import urlparse

class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.firstChain = self.create_block(proof = 1, previous_hash = 0)
    
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(dt.datetime.now()),
            'proof' : proof,
            'previoushash' : previous_hash,
            'transactions': self.transactions
        }
        self.chain.append(block)
        self.transactions = []
        return block 

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operaiions = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operaiions[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def gethash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        block_index = 1
        previous_block = chain[0]
        while block_index < len(chain):
            block = chain[block_index]
            if block['previoushash'] != self.gethash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operaiions =  hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operaiions[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        
        return True

    def add_transactions(self, sender, receiver, amount):
        self.transactions.append(
            {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
            }
        )
        
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc) #returns ip and port
    
    def replace_chain(self):
        network = self.nodes #all the nodes of the blockchain system, few might registred for mining and few others to do transactions
        longest_chain = None
        max_length = len(self.chain) #At first, we assume local chain has highest blocks

        #get chain of each node and find the longgest chain
        for node in network:
            print(node)
            response = requests.get(f'http://{node}/get_chain') #this chain method implemented in miningblock.py
            if response.status_code == 200: 
                result = response.json()
                chain = result['chain']
                length = result['length']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain: #if there is any longgest chain than current
                self.chain = longest_chain
                return True
            return False

            






    

    