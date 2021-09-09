import datetime as dt
import json
from flask import Flask, jsonify, request
from SreechoCoin import BlockChain
from uuid import uuid4
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# create address for the node on port 5000
node_address = str(uuid4()).replace('-', '')

blockchain = BlockChain()


@app.route('/mine_block', methods=['GET'])
def mine_blockchain():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.gethash(previous_block)
    blockchain.add_transactions(sender=node_address, receiver='2_chow', amount=1)
    block = blockchain.create_block(proof, previous_hash)

    #response = { 'chain': block }
    response = {
        'message': 'New block has been mined!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previoushash': block['previoushash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid'}
    else:
        response = {'message': 'The Blochain is invalid'}

    return jsonify(response), 200


@app.route('/add_transaction', methods=['PUT'])
def add_transaction():
    jsondata = request.get_json() # in generaly, it should be kind of filling details with web app but we will use json file with list of transactions and the file will be generated via
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key for key in transaction_keys if key in jsondata):
        return 'some elements of the transaction are missing', 400
    index = blockchain.add_transactions(jsondata['sender'], jsondata['receiver'], jsondata['amount'])
    response = {'message': f'This transaction will be added to the block {index}'}

    return jsonify(response), 201

#connecting new nodes
@app.route('/add_nodes', methods=['PUT'])
def add_nodes():
    jsondata = request.get_json()
    nodes = jsondata['nodes'] #json file must have nodes
    if len(nodes) == 0:
        return "No Nodes", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All teh nodes are connected. The SreechoCoins contains the following nodes',
                'total_nodes': list(blockchain.nodes)
        }
    
    return jsonify(response), 201

#Replacing the chain by teh longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longgest chain',
                    'new_chain': blockchain.chain
        }
    else:
        response = {'message': 'The chain is the largest one hence no replacement',
                    'actual_chain': blockchain.chain }

    return jsonify(response), 200

# running the app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5002)

