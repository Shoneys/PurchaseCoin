# pip install Flask==0.12.2 requests==2.18.4
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


# make it so it only mines, and automines, when a new transaciton coems in
# only useful if there is mass adoption

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
    if verify_transaction(values) is True:
        # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {'message': values['sender'] + ' does not have enough coins!'}

    return jsonify(response), 201


def verify_transaction(values):
    if values['sender'] in blockchain.wallet_balances:
        if blockchain.wallet_balances[values['sender']] > int(values['amount']):
            return True
        print('{} only has {} PurchaseCoins!'.format(values['sender'], blockchain.wallet_balances[values['sender']]))
        return False
    print('{} has no account'.format(values['sender']))


# outputs balance and total received
@app.route('/wallet', methods=['GET'])
def countmoneyrecieved():
    username = request.args.get('user')
    if username in blockchain.wallet_balances:
        moneycount = 0
        response = {'Current balance': blockchain.wallet_balances[username],
                    'Total Received': f"{username} has received {moneycount} coins in total"}
        return jsonify(response), 201
    else:
        response = {'error': '{} has no account'.format(username)}

    return jsonify(response), 400


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
