import flet as ft
from models.cold_wallet import ColdWallet
from pages.cold_wallet.destroy import delete_wallet
from pages.cold_wallet.modal_qrcode  import show_qr_code_modal
from helpers.generics import icon_control, limit_chars
from services.translator import t

def list_wallets(page: ft.Page, pageGo = '/', type_ = None):
  list_container = ft.Column(spacing=6)

  def load_items():
    list_container.controls.clear()

    wallets = ColdWallet.all()

    if type_:
      wallets = [w for w in wallets if w.type.lower() == type_.lower()]

    wallets = sorted(wallets, key=lambda x: (x.type.lower(), x.name.lower()))

    list_container.controls.append(ft.Text(t("wallets"), size=20, weight="bold"))
  
    for w in wallets:
      qr_code_btn = ft.IconButton(icon=ft.icons.QR_CODE, tooltip=t("address_qrcode"), on_click=lambda e, wid=w.id: show_qr_code_modal(page, wid))
      trash_btn = ft.IconButton(icon=ft.icons.DELETE, tooltip=t("trash"), on_click=lambda e, wid=w.id: delete_wallet(page, wid, '/', refresh))

      left_group = ft.Row(
        [
          icon_control(w.type),
          ft.Text(limit_chars(w.name, 10), size=16, color=ft.colors.WHITE, tooltip=w.name),
        ],
        spacing=8,
        alignment=ft.MainAxisAlignment.START,
        expand=True
      )
      center_group = ft.Row(
        [ft.Text(
          w.smallest_unit,
          size=16,
          weight="bold",
          color=ft.colors.BLUE_900
        )],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
      )

      right_group = ft.Row(
        [qr_code_btn, trash_btn],
        spacing=4,
        alignment=ft.MainAxisAlignment.END,
        expand=True,
      )

      row_line = ft.Container(
        content=ft.Row(
          [left_group, center_group, right_group],
          alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=ft.colors.GREEN_100,
        border_radius=8,
        ink=True,
        on_click=lambda e, wid=w.id: page.go(f"/show_wallet?id={wid}&back_page=list_wallets"),
      )

      list_container.controls.append(row_line)
  
    list_container.controls.append(ft.ElevatedButton(t("back"), on_click=lambda e: page.go(pageGo)))

    page.update()
  
  def refresh():
    load_items()
  
  refresh()

  return list_container
