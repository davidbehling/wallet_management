from web3 import Web3
from eth_account import Account

def generate_ethereum_wallet():
  public_key = Account.create()
  address = public_key.address
  private_key = public_key.key.hex()
  return { 'private_key': private_key, 'public_key': public_key, 'address': address }

def actual_balance_ethereum(address):
  infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
  web3 = Web3(Web3.HTTPProvider(infura_url))
  balance = web3.eth.get_balance(address)
  balance_in_ether = web3.fromWei(balance, 'ether')
  return balance_in_ether

