import os
import requests
import time
from dotenv import load_dotenv


load_dotenv()

class BitcoinRPC:
    def __init__(self):
        self.endpoint = os.getenv("CHAINSTACK_ENDPOINT")
        self.auth = (os.getenv("RPC_USER"), os.getenv("RPC_PASS"))
        
    def rpc_call(self, method, params=[]):
        payload = {
            "jsonrpc": "2.0",
            "id": "hw3",
            "method": method,
            "params": params
        }
        response = requests.post(
            self.endpoint,
            json=payload,
            auth=self.auth,
            headers={'Content-Type': 'application/json'}
        )
        return response.json()
    
    def get_block_count(self):
        return self.rpc_call("getblockcount")
    
    def get_block(self, height):
        block_hash = self.rpc_call("getblockhash", [height])["result"]
        return self.rpc_call("getblock", [block_hash])
    
    def get_blockchain_info(self):
        return self.rpc_call("getblockchaininfo")

# Function to monitor blockchain progress
def monitor_chain():
    client = BitcoinRPC()
    prev_height = 0
    
    while True:
        info = client.get_blockchain_info()["result"]
        current_height = info["blocks"]
        
        if current_height > prev_height:
            print(f"New block: {current_height} ({current_height - prev_height} blocks added)")
            prev_height = current_height
        else:
            print("Chain height maintained")
        
        time.sleep(600)  # Check every 10 minutes

# Example usage
if __name__ == "__main__":
   
    # Example 1: Print blockchain info and current block height
    # client = BitcoinRPC()
    # print("Current block height:", client.get_block_count()["result"])
    # print("Blockchain info:", client.get_blockchain_info()["result"])
    
    # Example 2: Monitor blockchain progress
    monitor_chain()
