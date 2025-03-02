"""Константы для приложения api."""

from reportlab.lib.units import cm

# Константы для генерации PDF-файла со списком покупок:
BOTTOM_MARGIN: int = 2 * cm
FOODGRAM_LOGO_HEIGHT: int = 3 * cm
FOODGRAM_LOGO_PATH: str = 'static/images/foodgram_logo.png'
FOODGRAM_LOGO_WIDTH: int = 3 * cm
INITIAL_Y_POSITION: int = 25 * cm
LEFT_MARGIN: int = 2 * cm
LINE_END: int = 18 * cm
LINE_HEIGHT: int = 1 * cm
LINE_START: int = LEFT_MARGIN
LINE_Y_POSITION: int = 26.8 * cm
NEW_PAGE_Y_POSITION: int = 27 * cm
SHOPPING_CART_FONT: str = 'static/fonts/DejaVuSans.ttf'
SHOPPING_CART_FONT_NAME: str = 'DejaVu'
START_INDEX: int = 1
TEXT_FONT_SIZE: int = 12
TITLE_FONT_SIZE: int = 16
TOP_MARGIN: int = 27 * cm
