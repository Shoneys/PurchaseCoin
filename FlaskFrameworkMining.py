# pip install Flask==0.12.2 requests==2.18.4
from multiprocessing import Process
from uuid import uuid4

from flask import Flask, jsonify, request

from Blockchain_DataStructure import Blockchaininst

blockchain = Blockchaininst

# Instantiate our Node
app = Flask(__name__)
from FlaskFrameworkNode import NodeApp

app.register_blueprint(NodeApp)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
print('Node 128-bit Universal Unique Identifier: {}'.format(node_identifier))


@app.route('/mine', methods=['GET'])
def mine():
    if len(blockchain.chain) > 1:
        if len(blockchain.current_transactions) < 1:
            return "There are no transactions in this block", 403  # correct code?

    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="Blockchain Federal Reserve",
        recipient=node_identifier,
        amount=5
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # verify sender has received enough coins to their private keys (for now, private keys are just "recipient")
    if verify_transaction(values) is not False:
        # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {'message': values['sender'] + ' does not have enough coins!'}

    return jsonify(response), 201


def verify_transaction(values):
    if blockchain.wallet_balances[values['sender']][0] < int(values['amount']):
        print('{} only has {} PurchaseCoins!'.format(values['sender'], blockchain.wallet_balances[values['sender']][0]))
        return False

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        # for x in range(a, b):
        #     for y in range(0, len(blockchain.chain[x]['transactions'])):
        #         print('Sender from chain: {}'.format(blockchain.chain[x]['transactions'][y]['sender']))
        #         print('Sender in transaction: {}'.format(values['sender']))
        #                 # if values['sender'] == blockchain.chain[x]['transactions'][y]['recipient']:
        # blockchain.chain[x]['transactions'][y]['amount'] = 0
    # need separate document to keep track of coins that are already spent, or experiment with setting values equal to 0

=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"

=======
=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"
=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"

# counts how much money you got
@app.route('/wallet', methods=['GET'])
def countmoneyrecieved():
    username = request.args.get('username')
    moneycount = 0
    for x in range(0, len(blockchain.chain)):
        for y in range(0, len(blockchain.chain[x]['transactions'])):
            if username == blockchain.chain[x]['transactions'][y]['recipient']:
                moneycount += blockchain.chain[x]['transactions'][y]['amount']
    response = {'Current balance': " " + blockchain.wallet_balances['username'][0],
                'Total Received': username + " has received " + str(moneycount) + " coins in total"}
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"
=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"
=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"
=======
>>>>>>> parent of 6bfdc0c... Revert "laid framework for anti double spending"


# counts how much money you got
# @app.route('/nodes/(recipient)', methods=['GET'])
# def countmoneyrecieved():
#     moneycount = 0
#     for x in range(0, len(blockchain.chain)):
#         for y in range(0, len(blockchain.chain[x]['transactions'])):
#             print(path)
#             if  == blockchain.chain[x]['transactions'][y]['recipient']:
#                 moneycount += blockchain.chain[x]['transactions'][y]['amount']
#     print("{} has recieved {} coins".format(recipient, moneycount))

@app.errorhandler(404)
def page_not_found(e):
    return "STOP BREAKING THE BLOCKCHAIN!", 404


while __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port, threaded=True)
