import flet as ft
from pages.home import home_view
from pages.cold_wallet.balance import balance_view
from pages.cold_wallet.create import create as create_wallet
from pages.cold_wallet.list import list_wallets
from pages.cold_wallet.show import show_wallet

def page_routes(page, route):
  page.views.clear()
  r = page.route
  params = page.query

  # root
  if r == "/":
    page.views.append(ft.View("/", [home_view(page)]))
  elif r == "/balance_wallets":
    page.views.append(ft.View(r, [balance_view(page)]))
  elif r.startswith("/list_wallets"):      
    coin_type = qs_get(params, "coin_type")
    pageGo = back_page(params)
    page.views.append(ft.View(r, [list_wallets(page, pageGo, coin_type)]))
  elif r == "/create_wallet":
    page.views.append(ft.View(r, [create_wallet(page)]))
  elif r.startswith("/show_wallet"):
    wallet_id = qs_get(params, "id")
    pageGo = back_page(params)
    page.views.append(ft.View(r, [show_wallet(page, wallet_id, pageGo)]))
  else:
    page.views.append(ft.View("/", [ft.Text("Rota não encontrada"), ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))]))
  page.update()


def qs_get(qs, key, default=None):
  try:
    return qs.get(key)
  except KeyError:
    return default
  
def back_page(params):
  return f"/{qs_get(params, 'back_page', '')}"
