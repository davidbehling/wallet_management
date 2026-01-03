import flet as ft
from enums.coin_type import CoinType
from models.cold_wallet import ColdWallet
from collections import defaultdict
from helpers.generics import icon_control
from services.translator import t

def balance_view(page: ft.Page, coin_type=None):
  wallets = ColdWallet.all()
  totals = defaultdict(float)
  per_type = defaultdict(list)

  for w in wallets:
    totals[w.type] += w.smallest_unit
    per_type[w.type].append(w)

  controls = [ft.Text(t("balance_to_type_coin"), size=20, weight='bold')]

  for coin, total in totals.items():
    def open_wallet_list(e, coin_type_=coin):
      page.go(f"/list_wallets?coin_type={coin_type_}&back_page=balance_wallets")

    coinn = next((c for c in CoinType if c.label == coin), None)

    left_group = ft.Row(
      [
        icon_control(coin),
        ft.Text(coinn.label, size=16, color=ft.colors.WHITE),
      ],
      spacing=8,
      alignment=ft.MainAxisAlignment.START,
      expand=True
    )

    right_group = ft.Row(
      [ft.Text(total, size=16,  weight="bold", color=ft.colors.BLUE_900)],
      spacing=4,
      alignment=ft.MainAxisAlignment.END,
      expand=True,
    )

    row_line = ft.Container(
      content=ft.Row(
        [left_group, right_group],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      ),
      padding=10,
      bgcolor=ft.colors.GREEN_100,
      border_radius=8,
      ink=True,
      on_click=open_wallet_list,
    )

    controls.append(row_line)
    
  controls.append(ft.ElevatedButton(t("back"), on_click=lambda e: page.go('/' if not coin_type else '/saldo')))
  return ft.Column(controls, spacing=8)