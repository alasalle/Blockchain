import hashlib
import requests

import sys

from blockchain import Blockchain

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = 'http://localhost:5000'

    coins_total = 0

    valid_proof = Blockchain.valid_proof

    def proof_of_work(last_block_string):

        proof = 0
        
        while valid_proof(last_block_string, proof) != True:
            proof += 1

        return proof
        

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server and look for a new one
        request = requests.get(f'{node}/last-block-string')
        last_block_string = request.json()['last_block_string']

        new_proof = proof_of_work(last_block_string)
        # : When found, POST it to the server {"proof": new_proof}
        post = requests.post(f'{node}/mine', json={'proof': f'{new_proof}'})
        
        # If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if post.json()['message'] == 'New Block Forged':
            coins_total += 1
            print(f'You\'ve earned another coin! New total: {coins_total} coin(s).')
        else:
            print(post.json()['message'])

