from datetime import datetime, timedelta
from services.db import price_table

from services.db import price_table

class CryptoPrice:
  UPDATE_INTERVAL = timedelta(hours=24)

  def __init__(self, coin, usd=0.0, brl=0.0, updated_at=None):
    self.coin = coin
    self.usd = float(usd)
    self.brl = float(brl)
    self.updated_at = updated_at or datetime.utcnow().isoformat()

  def to_dict(self):
    return {
      "coin": self.coin,
      "usd": self.usd,
      "brl": self.brl,
      "updated_at": self.updated_at,
    }

  def save(self):
    price_table.upsert(
      self.to_dict(),
      lambda r: r.get("coin") == self.coin
    )

  @staticmethod
  def all():
    return price_table.all()

  @staticmethod
  def get(coin):
    result = price_table.get(lambda r: r.get("coin") == coin)
    return CryptoPrice(**result) if result else None

  def needs_update(self):
    last_update = datetime.fromisoformat(self.updated_at)
    return datetime.utcnow() - last_update > self.UPDATE_INTERVAL
