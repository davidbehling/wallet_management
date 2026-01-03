from enums.coin_type import CoinType
from services.bitcoin_service import generate_bitcoin_wallet, actual_balance_bitcoin
from services.ethereum_service import generate_ethereum_wallet, actual_balance_ethereum
from services.litecoin_service import generate_litecoin_wallet, actual_balance_litecoin
from services.price_service import get_price
from models.cold_wallet import ColdWallet
from pycoingecko import CoinGeckoAPI
import random
# import requests

SMALLEST_UNIT_FACTORS = {
  CoinType.BITCOIN.label_lower: CoinType.BITCOIN.small_unit_value,                       # satoshis
  CoinType.ETHEREUM.label_lower: CoinType.ETHEREUM.small_unit_value,                     # wei
  CoinType.LITECOIN.label_lower: CoinType.LITECOIN.small_unit_value,                     # litoshis  
}

GENERATE_TYPE = {
  CoinType.BITCOIN.label: generate_bitcoin_wallet,
  CoinType.ETHEREUM.label: generate_ethereum_wallet,
  CoinType.LITECOIN.label: generate_litecoin_wallet
}

ACTUAL_BALANCE_TYPE = {
  CoinType.BITCOIN.label: actual_balance_bitcoin,
  CoinType.ETHEREUM.label: actual_balance_ethereum,
  CoinType.LITECOIN.label: actual_balance_litecoin
}

def generate_wallet(type):
  action = GENERATE_TYPE.get(type)
  if action:
    return action()
  
def update_actual_value(wallet: ColdWallet):  
  action = ACTUAL_BALANCE_TYPE.get(wallet.type)
  wallet.smallest_unit = action(wallet.address)
  wallet.save()
  return wallet

def update_list_actual_value():
  wallets = ColdWallet.all()
  for wallet in wallets:
    update_actual_value(wallet)

# Os métodos get_btc_recurrence_price, smallest_unit_to_recurrence e value_format_text
# foram substituídos pelo método genérico convert_crypto abaixo.
# Mas foi deixa-lo aqui comentado para referência futura e aprendizado.

#def get_btc_recurrence_price(type: str, recurrence: str) -> float:
#  # Requisição para pegar o preço atual do Bitcoin na moenda corrente
#  url = "https://api.coingecko.com/api/v3/simple/price"
#  resp = requests.get(url, params={"ids": type, "vs_currencies": recurrence})  
#
#  if resp.status_code != 200:
#    print(f"[ERRO] Falha no CoinGecko: HTTP {resp.status_code}")
#    return 0.0
#
#  data = resp.json()
#  
#  if type not in data:
#    print(f"[ERRO] CoinGecko não retornou valor para '{type}'")
#    print(f"Payload recebido: {data}")
#    return 0.0
#  
#  # Obtendo o valor do BTC na moeda corrente
#  return data[type].get(recurrence, 0.0)

#def smallest_unit_to_recurrence(type: str, smallest_unit: int, recurrence: str) -> float:
#  price = get_btc_recurrence_price(type, recurrence)
#  value = (smallest_unit / SMALLEST_UNIT_FACTORS.get(type)) * price
#  return value

#def value_format_text(type: str, smallest_unit: int, recurrence: str):
#  type = type.lower()
#  return f"{recurrence.upper()} R$ {smallest_unit_to_recurrence(type, smallest_unit, recurrence):.2f}"

# O método abaixo, convert_crypto, foi substituído pelo método crypto_to_prices.
# Como a cada visualização era feita um consulta na API do CoinGecko, o ideal
# é atualizar os preços em lote e armazená-los localmente, para depois apenas
# fazer o cálculo do valor da carteira com base nesses preços armazenados.

#def convert_crypto(
#  crypto: str,
#  currency: str,
#  amount: float
#) -> float:
#  cg = CoinGeckoAPI()
#
#  crypto = crypto.lower()
#  currency = currency.lower()
#  
#  price = cg.get_price(
#    ids=crypto,
#    vs_currencies=currency
#  )
#  
#  value = (amount / SMALLEST_UNIT_FACTORS.get(crypto)) * price[crypto][currency]
#
#  return f"{currency.upper()} R$ {value:.2f}"

def crypto_to_prices(wallet):
  price = get_price(wallet.type.lower())

  brl_value = (wallet.smallest_unit / SMALLEST_UNIT_FACTORS.get(wallet.type.lower())) * price.brl
  usd_value = (wallet.smallest_unit / SMALLEST_UNIT_FACTORS.get(wallet.type.lower())) * price.usd

  return { "brl": f"R$ {brl_value:.2f}", "usd": f"$ {usd_value:.2f}" }

# --------------------------
# MÉTODOS DE TESTE DE FLUXO:
# --------------------------

def generate_wallet_test(type):
  return { 'private_key': f"{type} private_key", 'public_key': f"{type} public_key", 'address': f"{type} address" }

def update_actual_value_test(wallet: ColdWallet):  
  wallet.smallest_unit = random.uniform(100,4000)
  wallet.save()
  return wallet


  