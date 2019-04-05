"""
credit due to Daniel van Flymen
https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
"""

import hashlib
import json
from time import time 
from urllib.parse import urlparse
import requests



class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


Blockchaininst = Blockchain()

# import hashlib
# import json
# import requests
#
# from time import time
# from urllib.parse import urlparse
#
#
# class Blockchain(object):
#     def __init__(self):
#         self.current_transactions = []
#         self.chain = []
#
#         self.nodes = set()  # holds list of nodes (idempotent)
#         # Create the genesis block
#         self.new_block(previous_hash=1,
#                        proof=100)  # may be able to figure out hashes based on these 2 first numbers?? odd and even.
#
#     def new_block(self, proof, previous_hash=None):
#         """
#         Create a new Block in the Blockchain
#         :param proof: <int> The proof given by the Proof of Work algorithm
#         :param previous_hash: (Optional) <str> Hash of previous Block
#         :return: <dict> New Block
#         """
#
#         block = {
#             'index': len(self.chain) + 1,  # shows index of chain
#             'timestamp': time(),  # gives time
#             'transactions': self.current_transactions,  # shows current transactions of block
#             'proof': proof,
#             'previous_hash': previous_hash or self.hash(self.chain[-1]),
#         }
#         # Reset the current list of transactions?
#         self.current_transactions = []
#
#         self.chain.append(block)
#
#         return block
#
#     def new_transaction(self, sender, recipient, amount):
#         """
#         Creates a new transaction to go into the next mined Block
#         :param sender: <str> Address of the Sender
#         :param recipient: <str> Address of the Recipient
#         :param amount: <int> Amount
#         :return: <int> The index of the Block that will hold this transaction
#         """
#         current_transactions_addition = {
#             'sender': sender,
#             'recipient': recipient,
#             'amount': amount,
#         }
#
#         self.current_transactions.append(current_transactions_addition)
#         return self.last_block['index'] + 1
#
#     @property
#     def last_block(self):
#         return self.chain[-1]
#
#     @staticmethod
#     def hash(block):
#         """
#         Creates a SHA-256 hash of a Block
#         :param block: <dict> Block
#         :return: <str>
#         """
#
#         # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
#         block_string = json.dumps(block, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()
#
#     def proof_of_work(self, last_proof):
#         """
#         Simple Proof of Work Algorithm:
#         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
#         - p is the previous proof, and p' is the new proof
#         :param last_proof: <int>
#         :return: <int>
#         """
#
#         proof = 0
#         while self.valid_proof(last_proof, proof) is False:
#             proof += 1
#
#         return proof
#
#     @staticmethod
#     def valid_proof(last_proof, proof):
#         """
#         Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
#         :param last_proof: <int> Previous Proof
#         :param proof: <int> Current Proof
#         :return: <bool> True if correct, False if not.
#         """
#
#         guess = f'{last_proof}{proof}'.encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash[:4] == "0000"
#
#     def register_node(self, address):
#         """
#         Add a new node to the list of nodes
#         :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
#         :return: None
#         """
#
#         parsed_url = urlparse(address)
#         self.nodes.add(parsed_url.netloc)
#
#     def valid_chain(self, chain):
#         """
#         Determine if a given blockchain is valid
#         :param chain: <list> A blockchain
#         :return: <bool> True if valid, False if not
#         """
#
#         last_block = chain[0]
#         current_index = 1
#
#         while current_index < len(chain):
#             block = chain[current_index]
#             print(f'{last_block}')
#             print(f'{block}')
#             print("\n-----------\n")
#             # Check that the hash of the block is correct
#             if block['previous_hash'] != self.hash(last_block):
#                 return False
#
#             # Check that the Proof of Work is correct
#             if not self.valid_proof(last_block['proof'], block['proof']):
#                 return False
#
#             last_block = block
#             current_index += 1
#
#         return True
#
#     def resolve_conflicts(self):
#         """
#         This is our Consensus Algorithm, it resolves conflicts
#         by replacing our chain with the longest one in the network.
#         :return: <bool> True if our chain was replaced, False if not
#         """
#
#         neighbours = self.nodes
#         new_chain = None
#
#         # We're only looking for chains longer than ours
#         max_length = len(self.chain)
#
#         # Grab and verify the chains from all the - in our network
#         for node in neighbours:
#             response = requests.get(f'http://{node}/chain')
#
#             if response.status_code == 200:
#                 length = response.json()['length']
#                 chain = response.json()['chain']
#
#                 # Check if the length is longer and the chain is valid
#                 if length > max_length and self.valid_chain(chain):
#                     max_length = length
#                     new_chain = chain
#
#         # Replace our chain if we discovered a new, valid chain longer than ours
#         if new_chain:
#             self.chain = new_chain
#             return True
#
#         return False
