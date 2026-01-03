import uuid
from services.db import wallets_table
from services.qrcode_service import generate_qrcode

class ColdWallet:
  def __init__(self, id=None, name=None, type=None, private_key=None, public_key=None, address=None, smallest_unit=0, qrcode_path=None):
    self.id = id or str(uuid.uuid4())
    self.name = name
    self.type = type
    self.private_key = private_key
    self.public_key = public_key
    self.address = address
    self.smallest_unit = int(smallest_unit or 0)
    self.qrcode_path = qrcode_path

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'type': self.type,
      'private_key': self.private_key,
      'public_key': self.public_key,
      'address': self.address,
      'smallest_unit': int(self.smallest_unit),
      'qrcode_path': self.qrcode_path,
    }

  def save(self):
    existing = wallets_table.get(lambda r: r.get('id') == self.id)
    if existing:
      wallets_table.update(self.to_dict(), lambda r: r.get('id') == self.id)
    else:
      wallets_table.insert(self.to_dict())

  def delete(self):
    wallets_table.remove(lambda r: r.get('id') == self.id)

  @staticmethod
  def all():
    return [ColdWallet(**w) for w in wallets_table.all()]

  @staticmethod
  def find_by_id(id):
    r = wallets_table.get(lambda rec: rec.get('id') == id)
    return ColdWallet(**r) if r else None

  def ensure_qrcode(self):
    if not self.qrcode_path and (self.public_key or self.address):
      self.qrcode_path = generate_qrcode(self.public_key or self.address, self.id)
      self.save()