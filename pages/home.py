import flet as ft
from services.translator import t

def home_view(page: ft.Page):
  return ft.Column([
    ft.Text(t("wallet_management"), size=22, weight='bold'),
    ft.ElevatedButton(t("balance"), on_click=lambda e: page.go('/balance_wallets')),
    ft.ElevatedButton(t("wallets"), on_click=lambda e: page.go('/list_wallets')),
    ft.ElevatedButton(t("create_wallet"), on_click=lambda e: page.go('/create_wallet')),
    #ft.ElevatedButton(t("pay"), on_click=lambda e: page.go('/pay')),
    #ft.ElevatedButton(t("close_app"), on_click=lambda e: page.window_close()),
    ], spacing=12)