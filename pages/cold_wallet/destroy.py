import flet as ft
from models.cold_wallet import ColdWallet
from services.translator import t
import os

def delete_wallet(page: ft.Page, wallet_id: str, pageGo = '/', refresh_callback=None):
  w = ColdWallet.find_by_id(wallet_id)
  if not w:
    return
  
  def confirm(e):
    w.delete()
    if w.qrcode_path and os.path.exists(w.qrcode_path):
      try:
        os.remove(w.qrcode_path)
      except:
        pass
    page.dialog.open = False

    if refresh_callback:
      page.update()
      refresh_callback()
    else:
      page.go(pageGo)

  def close_dialog(e):
    dlg.open = False
    page.update()

  dlg = ft.AlertDialog(title=ft.Text(t("confirm")), 
                       content=ft.Text(f"{t('wallet_delete')} '{w.name}'?"), 
                       actions=[ft.ElevatedButton(t("yes"), on_click=confirm), 
                                ft.TextButton(t("no"), on_click=close_dialog)])
  page.dialog = dlg
  page.dialog.open = True
  page.update()