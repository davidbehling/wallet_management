import uuid
from services.db import dest_table

class FromWallet:
  def __init__(self, id=None, from_name=None, from_public_key=None, type=None, observation=None):
    self.id = id or str(uuid.uuid4())
    self.from_name = from_name
    self.from_public_key = from_public_key
    self.type = type
    self.observation = observation

  def to_dict(self):
    return {
      'id': self.id,
      'from_name': self.from_name,
      'from_public_key': self.from_public_key,
      'type': self.type,
      'observation': self.observation,
    }

  def save(self):
    existing = dest_table.get(lambda r: r.get('id') == self.id)
    if existing:
      dest_table.update(self.to_dict(), lambda r: r.get('id') == self.id)
    else:
      dest_table.insert(self.to_dict())

  def delete(self):
    dest_table.remove(lambda r: r.get('id') == self.id)

  @staticmethod
  def all():
    return [FromWallet(**w) for w in dest_table.all()]

  @staticmethod
  def find_by_id(id):
    r = dest_table.get(lambda rec: rec.get('id') == id)
    return FromWallet(**r) if r else None