import requests
from litecoinutils.keys import PrivateKey as LTCPrivateKey

def generate_litecoin_wallet():
  public_key = LTCPrivateKey()
  address = public_key.get_address().to_string()
  private_key = public_key.to_wif()
  return { 'private_key': private_key, 'public_key': public_key, 'address': address }

def actual_balance_litecoin(address):
  url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}'
  response = requests.get(url)
  data = response.json()
  return data['balance']

