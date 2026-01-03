import flet as ft
from models.cold_wallet import ColdWallet
from services.translator import t
import os

def show_qr_code_modal(page: ft.Page, wallet_id: str):
  w = ColdWallet.find_by_id(wallet_id)
  if not w:
    page.snack_bar = ft.SnackBar(ft.Text(t("wallet_not_found")))
    page.snack_bar.open = True
    page.update()
    return

  w.ensure_qrcode()

  img = None
  if w.qrcode_path and os.path.exists(w.qrcode_path):
    img = ft.Image(
      src=w.qrcode_path,
      fit=ft.ImageFit.CONTAIN,
      width=220,
      height=220
    )

  def close_dialog(e):
    dlg.open = False
    page.update()

  dlg = ft.AlertDialog(
    modal=True,
    title=ft.Text(f"{t('public_key')}: {w.name}", size=18, weight="bold"),
    content=ft.Container(
      content=img or ft.Text(t("qr_not_available")),
      padding=10,
      alignment=ft.alignment.center,
      width=250,
      height=None,
    ),
    actions=[
      ft.TextButton(t("close"), on_click=close_dialog)
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    inset_padding=20,
  )

  page.dialog = dlg
  dlg.open = True
  page.update()
