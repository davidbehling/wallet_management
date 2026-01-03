import requests
from bitcoin import random_key, privtopub, pubtoaddr, history, mktx, sign, pushtx

def generate_bitcoin_wallet():
  private_key = random_key()
  public_key = privtopub(private_key)
  address = pubtoaddr(public_key)
  return { 'private_key': private_key, 'public_key': public_key, 'address': address }

#-----------------------------
#  CONSULTAR VALOR DA CARTEIRA
#-----------------------------

# smallest_unit é uma unidade de medida padrão para todas as criptos, o bitcoin tem um com nome proprio chamada satoshi
def cold_wallet_bitcoin(address):
  smallest_unit = actual_balance_bitcoin(address)
  value_in_brl = smallest_unit_to_recurrence(smallest_unit, "brl")
  value_in_usd = smallest_unit_to_recurrence(smallest_unit, "usd")
  print(f"{smallest_unit} satoshis são equivalentes a R${value_in_brl:.2f} BRL")
  return { "smallest_unit": smallest_unit, "brl_value": value_in_brl, "value_usd": value_in_usd }

def actual_balance_bitcoin(address):
  url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}'
  response = requests.get(url)
  data = response.json()
  return data['balance']

def smallest_unit_to_recurrence(smallest_unit, recurrence):
  # Obtendo o valor atual do BTC na moeda corrente
  btc_brl = get_btc_recurrence_price(recurrence)

  # Convertendo satoshis para BTC
  value = smallest_unit / 100000000

  # Convertendo BTC para a moeda corrente
  value = value * btc_brl
  return value

def get_btc_recurrence_price(recurrence):
  # Requisição para pegar o preço atual do Bitcoin na moenda corrente
  url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={recurrence}"
  response = requests.get(url)
  data = response.json()

  # Obtendo o valor do BTC na moeda corrente
  btc_brl = data['bitcoin'][recurrence]
  return btc_brl

#----------------------------
#  LÓGICA DE ENVIO DE BITCOIN
#----------------------------

# Consulta a API da Coindesk.
# Retorna o valor do Bitcoin em reais (BRL) como float.
# Em caso de erro, retorna None.
# def get_btc_price_brl():
#   try:
#     r = requests.get("https://api.coindesk.com/v1/bpi/currentprice/BRL.json")
#     return r.json()["bpi"]["BRL"]["rate_float"]
#   except:
#     return None

# Retorna saldo em satoshis
# Usa history(address) da lib para recuperar todos os UTXOs.
# O valor do UTXO (u["value"]) às vezes vem em:
# - satoshis (< 100M)
# - BTC float (>= 1 BTC → multiplicado por 1e8)
#   value < 100000000   → satoshis
#   value ≥ 100000000   → assume que veio em BTC float
# obs: Essa lógica é gambiarra famosa porque a biblioteca é inconsistente.
# def get_balance_btc(address):
#   utxos = history(address)
#   total_sats = 0
# 
#   for u in utxos:
#     value = u.get("value", 0)
#     if value < 100000000:
#       total_sats += value
#     else:
#       total_sats += int(value * 1e8)
# 
#   return total_sats

# Converte satoshis para BTC (sats / 1e8)
# Multiplica pelo preço em reais.
# def get_balance_brl(address):
#   sats = get_balance_btc(address)
#   price = get_btc_price_brl()
#   if not price:
#     return None
#   return (sats / 1e8) * price

# Busca taxa da rede no mempool.space
# Se falhar → assume 2 sats/vbyte.
# def get_fee_per_byte():
#   try:
#     r = requests.get("https://mempool.space/api/v1/fees/recommended")
#     return r.json()["economyFee"]
#   except:
#     return 2


# Envia BTC em satoshis.
# Retorna dict:
# {
#   "success": True/False,
#   "message": "...",
#   "tx_id": "..."
# }
# def send_bitcoin(private_key, to_address, amount_sats):
#   pub = privtopub(private_key)
#   from_address = pubtoaddr(pub)
# 
#   balance = get_balance_btc(from_address)
# 
#   if balance < amount_sats:
#     return {
#       "success": False,
#       "message": f"Saldo insuficiente. Saldo atual: {balance} sat."
#     }
# 
#   fee_byte = get_fee_per_byte()
#   estimated_size = 200
#   fee = fee_byte * estimated_size
# 
#   if balance < amount_sats + fee:
#     return {
#       "success": False,
#       "message": "Saldo insuficiente para cobrir taxa da rede."
#     }
# 
#   utxos = history(from_address)
#   inputs = []
#   total = 0
# 
#   for u in utxos:
#     v = u["value"] if u["value"] < 100000000 else int(u["value"] * 1e8)
#     inputs.append({"output": u["output"], "value": v})
#     total += v
#     if total >= amount_sats + fee:
#       break
# 
#   change = total - (amount_sats + fee)
# 
#   outputs = [{"address": to_address, "value": amount_sats}]
#   if change > 0:
#     outputs.append({"address": from_address, "value": change})
# 
#   raw = mktx(inputs, outputs)
# 
#   for i in range(len(inputs)):
#     raw = sign(raw, i, private_key)
# 
#   tx_id = pushtx(raw)
# 
#   return {
#     "success": True,
#     "message": "Transação enviada com sucesso!",
#     "tx_id": tx_id
#   }





#-------------------------------
#  LÓGICA DE ENVIO DE BITCOIN V2
#-------------------------------

# def to_satoshis(value):
#   if isinstance(value, float):
#     return int(value * 100_000_000)
#   return int(value)
# 
# def list_utxos(address):
#   r = requests.get(f"https://mempool.space/api/address/{address}/utxo")
#   r.raise_for_status()
#   return r.json()
# 
# def get_balance_sats(address):
#   utxos = list_utxos(address)
#   return sum(to_satoshis(u["value"]) for u in utxos)
# 
# def get_fee_rate():
#   try:
#     r = requests.get("https://mempool.space/api/v1/fees/recommended")
#     return int(r.json()["economyFee"])
#   except:
#     return 2  # fallback seguro
#   
# def estimate_tx_size(num_inputs, num_outputs, legacy=False):
#   if legacy:
#     # Valores para transação LEGACY (P2PKH)
#     return num_inputs * 148 + num_outputs * 34 + 10
#   else:
#     # Valores para transação SEGWIT (P2WPKH)
#     return num_inputs * 68 + num_outputs * 31 + 10
# 
# def select_utxos(utxos, amount_sats, fee_rate):
#   selected = []
#   total = 0
# 
#   for u in sorted(utxos, key=lambda x: x["value"]):
#     selected.append(u)
#     total += u["value"]
# 
#     size = estimate_tx_size(len(selected), 2)
#     fee = size * fee_rate
# 
#     if total >= amount_sats + fee:
#       return selected, total, fee
# 
#   raise ValueError("Saldo insuficiente para cobrir valor + taxa")
# 
# def send_bitcoin_v2(private_key, to_address, amount_sats):
#   pub = privtopub(private_key)
#   from_address = pubtoaddr(pub)
# 
#   utxos = list_utxos(from_address)
#   fee_rate = get_fee_rate()
# 
#   selected, total, fee = select_utxos(
#     utxos,
#     amount_sats,
#     fee_rate
#   )
# 
#   change = total - amount_sats - fee
# 
#   inputs = [
#     {
#       "txid": u["txid"],
#       "vout": u["vout"],
#       "value": u["value"]
#     }
#     for u in selected
#   ]
# 
#   outputs = [{"address": to_address, "value": amount_sats}]
#   if change > 546:  # evita dust
#     outputs.append({"address": from_address, "value": change})
# 
#   raw = mktx(inputs, outputs)
# 
#   for i in range(len(inputs)):
#     raw = sign(raw, i, private_key)
# 
#   tx_id = pushtx(raw)
# 
#   return {
#     "success": True,
#     "tx_id": tx_id,
#     "fee": fee,
#     "change": change
#   }


#-------------------------------
#  LÓGICA DE ENVIO DE BITCOIN 3
#-------------------------------

# Esse código:
# 
# Identifica o tipo do endereço Bitcoin
# 
# Busca os UTXOs desse endereço
# 
# Obtém a taxa de fee atual da rede
# 
# Estima o tamanho da transação
# 
# Seleciona UTXOs suficientes para pagar o valor + fee
# 
# Calcula o troco, respeitando o dust limit
# 
# Constrói uma PSBT (Partially Signed Bitcoin Transaction)
# 
# Ele não assina nem transmite a transação — só prepara os dados.




# Valor mínimo (em satoshis) para que uma saída seja considerada válida.
# 
# Outputs menores que isso são considerados dust
# 
# Se o troco for menor que 546 sats → ele é descartado e vira fee

DUST_LIMIT = 546

# Tamanho médio em bytes (ou vbytes) de cada input, dependendo do tipo:
# 
# P2PKH (legacy): mais caro
# 
# SegWit (P2WPKH): mais barato
# 
# Taproot (P2TR): o mais eficiente

# 👉 Isso é essencial para estimar corretamente o fee.

INPUT_SIZE_BY_TYPE = {
  "p2pkh": 148,
  "p2sh-p2wpkh": 91,
  "p2wpkh": 68,
  "p2tr": 58
}

# Tamanho padrão de um output SegWit (em vbytes).

OUTPUT_SIZE = 31

# Overhead fixo da transação (version, locktime, etc).

TX_OVERHEAD = 10

def detect_address_type(address: str):
  address = address.lower()

  if address.startswith("bc1p"):
    return "p2tr"
  if address.startswith("bc1q"):
    return "p2wpkh"
  if address.startswith("3"):
    return "p2sh-p2wpkh"
  if address.startswith("1"):
    return "p2pkh"

  raise ValueError("Endereço Bitcoin inválido")

# Chama a API do mempool.space
# 
# Retorna uma lista de UTXOs com:
# txid
# vout
# value (em satoshis)
# 
# Esses UTXOs são os inputs possíveis da transação.

def list_utxos(address: str):
  r = requests.get(f"https://mempool.space/api/address/{address}/utxo")
  r.raise_for_status()

  return [
    {
      "txid": u["txid"],
      "vout": u["vout"],
      "value": int(u["value"])
    }
    for u in r.json()
  ]

def get_fee_rate():
  r = requests.get("https://mempool.space/api/v1/fees/recommended")
  r.raise_for_status()
  return int(r.json()["economyFee"])

# Isso gera o tamanho estimado da transação em vbytes, usado para calcular o fee.

def estimate_tx_size(num_inputs, num_outputs, input_type):
  input_size = INPUT_SIZE_BY_TYPE[input_type]
  return (
    num_inputs * input_size
    + num_outputs * OUTPUT_SIZE
    + TX_OVERHEAD
  )

# Lógica de seleção de UTXOs (Coin Selection)

# 1. Ordena UTXOs do menor para o maior
# 2. Vai adicionando UTXOs até cobrir:
# 3. Sempre assume 2 outputs:
#   * destino
#   * troco

# O fee é recalculado a cada input adicionado, porque:
#   * Mais inputs → transação maior → fee maior

# Se não conseguir → "Saldo insuficiente".

def select_utxos(utxos, amount_sats, fee_rate, input_type):
  selected = []
  total = 0

  utxos = sorted(utxos, key=lambda x: x["value"])

  for u in utxos:
    selected.append(u)
    total += u["value"]

    size = estimate_tx_size(
      num_inputs=len(selected),
      num_outputs=2,
      input_type=input_type
    )

    fee = size * fee_rate

    if total >= amount_sats + fee:
      return selected, total, fee

  raise ValueError("Saldo insuficiente")

def calculate_change(total, amount, fee):
  change = total - amount - fee
  return change if change >= DUST_LIMIT else 0

# Cria um objeto simples com:
# 
# Inputs
# UTXOs selecionados
# 
# Outputs
# Sempre o pagamento principal

# Troco apenas se for válido
# ⚠️ Isso não é uma PSBT real em base64, é apenas a estrutura lógica.

def create_psbt(inputs, to_address, amount_sats, change_address, change_sats):
  outputs = [
    {
      "address": to_address,
      "value": amount_sats
    }
  ]

  if change_sats > 0:
    outputs.append(
      {
        "address": change_address,
        "value": change_sats
      }
    )

  return {
    "inputs": inputs,
    "outputs": outputs
  }

def build_bitcoin_send(
  from_address: str,
  to_address: str,
  amount_sats: int,
  fee_rate: int = None
):
  input_type = detect_address_type(from_address)

  utxos = list_utxos(from_address)

  if not fee_rate:
    fee_rate = get_fee_rate()

  selected, total, fee = select_utxos(
    utxos,
    amount_sats,
    fee_rate,
    input_type
  )

  change = calculate_change(total, amount_sats, fee)

  psbt = create_psbt(
    inputs=selected,
    to_address=to_address,
    amount_sats=amount_sats,
    change_address=from_address,
    change_sats=change
  )

  return {
    "psbt": psbt,
    "fee": fee,
    "fee_rate": fee_rate,
    "inputs": selected,
    "change": change
  }






