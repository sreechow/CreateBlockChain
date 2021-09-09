
import hashlib
import datetime as dt
import json

#Constructor with list of chains and first chain
class BlockChain:
    def __init__(self):
        self.chain = []
        self.firstChain = self.create_block(proof = 1, previous_hash = 0)
    
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(dt.datetime.now()),
            'proof' : proof,
            'previoushash' : previous_hash
        }
        self.chain.append(block)
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
        previous_block = self.chain[0]
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



    

    