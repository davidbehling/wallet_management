import os
import qrcode

QRCODE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'qrcodes')
QRCODE_DIR = os.path.abspath(QRCODE_DIR)
os.makedirs(QRCODE_DIR, exist_ok=True)

def generate_qrcode(text: str, wallet_id: str) -> str:
  filename = os.path.join(QRCODE_DIR, f"{wallet_id}.png")
  img = qrcode.make(text or "")
  img.save(filename)
  return filename