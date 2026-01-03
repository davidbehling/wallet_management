import flet as ft
from routes import page_routes

def main(page: ft.Page):
  page.title = "Wallet App"
  page.window_width = 400
  page.window_height = 700
  page.theme_mode = ft.ThemeMode.LIGHT
  page.vertical_alignment = ft.MainAxisAlignment.START
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  
  def route_change(route):
    page_routes(page, route)

  page.on_route_change = route_change
  page.go("/")

if __name__ == "__main__":
  ft.app(target=main)

# import pdb; pdb.set_trace()