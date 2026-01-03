import flet as ft
from models.cold_wallet import ColdWallet
from pages.cold_wallet.destroy import delete_wallet
from pages.cold_wallet.modal_qrcode import show_qr_code_modal
from helpers.generics import icon_control, toggle_button
from services.generic_service import update_actual_value, update_actual_value_test, crypto_to_prices
from services.translator import t
from enums.coin_type import CoinType


def show_wallet(page: ft.Page, wallet_id: str, pageGo = '/'):

  w = ColdWallet.find_by_id(wallet_id)
  if not w:
    page.snack_bar = ft.SnackBar(ft.Text(t("wallet_not_found")))
    page.snack_bar.open = True
    return
  
  def update_value(e, w):
    _wallet = update_actual_value_test(w)
    prices = crypto_to_prices(_wallet)
    brl_value.value = prices["brl"]
    usd_value.value = prices["usd"] 
    page.update()

  set_actual_value_btn = ft.IconButton(
    icon=ft.icons.CURRENCY_EXCHANGE,
    tooltip=t("wallet_value_updated"),
    on_click=lambda e: update_value(page, w)
  )

  qr_btn = ft.IconButton(
    icon=ft.icons.QR_CODE,
    tooltip=t("address_qrcode"),
    on_click=lambda e: show_qr_code_modal(page, w.id)
  )

  delete_btn = ft.IconButton(
    icon=ft.icons.DELETE,
    tooltip=t("trash"),
    icon_color=ft.colors.RED_600,
    on_click=lambda e: (delete_wallet(page, w.id, '/list_wallets'))
  )

  back_btn = ft.ElevatedButton(t("back"), on_click=lambda e: page.go(pageGo))

  coin_value = ft.Text(w.smallest_unit, size=18, color=ft.colors.BLUE_900, tooltip=CoinType[w.type.upper()].small_unit_label)

  prices = crypto_to_prices(w)

  brl_value = ft.Text(prices["brl"], size=14, color=ft.colors.BLUE_900, tooltip="Real (brl)")

  usd_value = ft.Text(prices["usd"], size=14, color=ft.colors.BLUE_900, tooltip="Dólar (usd)")

  content = ft.Column(
    [
      ft.Row([icon_control(w.type), ft.Text(w.name, size=22, weight="bold")]),
      coin_value,

      ft.Divider(),

      brl_value,
      usd_value,

      ft.Divider(),

      ft.Text(t("public_key"), weight="bold"),
      toggle_button(page, w.public_key),

      ft.Text(t("private_key"), weight="bold"),
      toggle_button(page, w.private_key),

      ft.Text(t("address"), weight="bold"),
      toggle_button(page, w.address),

      ft.Divider(),

      ft.Row([set_actual_value_btn, qr_btn, delete_btn], alignment=ft.MainAxisAlignment.CENTER),
      back_btn,
    ],
    spacing=12
  )

  return content







