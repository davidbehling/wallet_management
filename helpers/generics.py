import flet as ft
from enums.coin_type import CoinType

def icon_control(coin_type):
  coin = next((c for c in CoinType if c.label == coin_type), None)
  return (
    ft.Image(src=coin.icon_path, width=24, height=24, tooltip=coin.label)
    if coin else ft.Icon(ft.icons.MONETIZATION_ON, size=40)
  )

def toggle_button(page, text):
  visible = False

  ft_text = ft.Text(
    "************",
    size=16,
    selectable=False
  )

  def toggle_action(e):
    nonlocal visible, ft_text
    visible = not visible

    ft_text.value = (
      text if visible else "************"
    )
    page.update()

  return ft.TextButton(
    content=ft_text,
    on_click=toggle_action,
  )

def limit_chars(text, limit=20):
  return text if len(text) <= limit else text[:limit] + "…"
