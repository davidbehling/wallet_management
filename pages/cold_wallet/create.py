import flet as ft
from models.cold_wallet import ColdWallet
from services.generic_service import generate_wallet, generate_wallet_test
from services.qrcode_service import generate_qrcode
from enums.coin_type import CoinType
from services.translator import t

COIN_TYPE = [ft.dropdown.Option(e.label) for e in CoinType]

def create(page: ft.Page):
  name = ft.TextField(label=t("wallet_name"))
  coin_type = ft.Dropdown(label=t("coin_type"), options=COIN_TYPE)
  priv = ft.TextField(label=t("private_key_opt"))
  pub = ft.TextField(label=t("public_key_opt"))
  address = ft.TextField(label=t("address_opt"))
  def on_save(e):
    if not name.value or not coin_type.value:
      page.snack_bar = ft.SnackBar(ft.Text(t("name_and_type_required")))
      page.snack_bar.open = True
      page.update()
      return

    w = ColdWallet(
      name=name.value, 
      type=coin_type.value or "Other", 
      private_key=priv.value, 
      public_key=pub.value, 
      address=address.value, 
      smallest_unit=0.0)

    if bool(set(["", None]) & set([address.value, priv.value, pub.value])):
      result = generate_wallet_test(coin_type.value) #generate_wallet(coin_type.value)
      w.address = result['address']
      w.private_key = result['private_key']
      w.public_key = result['public_key']
    
    if w.public_key:
      w.qrcode_path = generate_qrcode(w.address, w.id)
  
    w.save()
    page.snack_bar = ft.SnackBar(ft.Text(t("created_wallet")))
    page.snack_bar.open = True
    refresh_route(page)

  return ft.Column([
    ft.Text(t("create_wallet"), size=20, weight="bold"),
    name, coin_type, priv, pub, address,
    ft.Row([ft.ElevatedButton(t("save"), on_click=on_save), ft.ElevatedButton(t("back"), on_click=lambda e: page.go("/"))])
  ], spacing=8)

def refresh_route(page: ft.Page):
    # re-navigate to current route to force page redraw
    page.go(page.route)



