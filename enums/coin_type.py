from enum import Enum

class CoinType(Enum):
  BITCOIN = ('Bitcoin', 'assets/bitcoin.png', 'satoshis', 100_000_000)
  ETHEREUM = ('Ethereum', 'assets/ethereum.png', 'wei', 1_000_000_000_000_000_000)
  LITECOIN = ('Litecoin', 'assets/litecoin.png', 'litoshis', 100_000_000)

  @property
  def label(self):
    return self.value[0]
  
  @property
  def label_lower(self):
    return self.value[0].lower()

  @property
  def icon_path(self):
    return self.value[1]
  
  @property
  def small_unit_label(self):
    return self.value[2]
  
  @property
  def small_unit_value(self):
    return self.value[3]