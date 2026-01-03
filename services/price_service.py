from pycoingecko import CoinGeckoAPI
from models.crypto_price import CryptoPrice

COINS = ["bitcoin", "ethereum", "litecoin"]
CURRENCIES = ["usd", "brl"]

def update_prices():
  cg = CoinGeckoAPI()

  data = cg.get_price(
    ids=COINS,
    vs_currencies=CURRENCIES
  )

  for coin, values in data.items():
    price = CryptoPrice(
      coin=coin,
      usd=values["usd"],
      brl=values["brl"]
    )

    price.save()

def get_prices():
  for coin in COINS:
    price = CryptoPrice.get(coin)

    if not price or price.needs_update():
      update_prices()
      break

  return CryptoPrice.all()

def get_price(coin):
  price = CryptoPrice.get(coin)

  if not price or price.needs_update():
    update_prices()

  return CryptoPrice.get(coin)


