import datetime as dt
import json
from flask import Flask, jsonify
from BlockChain import BlockChain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


blockchain = BlockChain()

@app.route('/mine_block', methods=['GET'])
def mine_blockchain():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.gethash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    #response = { 'chain': block }
    response = {
        'message': 'New block has been mined!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previoushash': block['previoushash']

    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain) }
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid'}
    else:
        response = {'message': 'The Blochain is invalid'}
    
    return jsonify(response), 200

#running the app

if __name__ == '__main__':
    app.run(host='0.0.0.0')
