import uuid
from datetime import datetime
from services.db import trans_table

class Transaction:
  def __init__(self, id=None, observation=None, smallest_unit=0.0, date=None, cold_wallet_id=None, from_wallet_id=None):
    self.id = id or str(uuid.uuid4())
    self.observation = observation
    self.smallest_unit = int(smallest_unit or 0.0)
    self.date = date or datetime.utcnow().isoformat()
    self.cold_wallet_id = cold_wallet_id
    self.from_wallet_id = from_wallet_id

  def to_dict(self):
    return {
      'id': self.id,
      'observation': self.observation,
      'smallest_unit': int(self.smallest_unit),
      'date': self.date,
      'cold_wallet_id': self.cold_wallet_id,
      'from_wallet_id': self.from_wallet_id,
    }

  def save(self):
    trans_table.insert(self.to_dict())

  @staticmethod
  def all():
    return trans_table.all()