"""Утилиты для приложения api."""

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from api.constants import (
    BOTTOM_MARGIN,
    FOODGRAM_LOGO_HEIGHT,
    FOODGRAM_LOGO_PATH,
    FOODGRAM_LOGO_WIDTH,
    INITIAL_Y_POSITION,
    LEFT_MARGIN,
    LINE_END,
    LINE_HEIGHT,
    LINE_START,
    LINE_Y_POSITION,
    NEW_PAGE_Y_POSITION,
    SHOPPING_CART_FONT,
    SHOPPING_CART_FONT_NAME,
    START_INDEX,
    TEXT_FONT_SIZE,
    TITLE_FONT_SIZE,
    TOP_MARGIN,
)


def generate_shopping_list_pdf(
    ingredients: dict[tuple[str, str], int],
) -> BytesIO:
    """Генерация PDF-файла со списком покупок."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(
        TTFont(SHOPPING_CART_FONT_NAME, SHOPPING_CART_FONT)
    )

    pdf.drawImage(
        FOODGRAM_LOGO_PATH,
        LEFT_MARGIN,
        TOP_MARGIN,
        width=FOODGRAM_LOGO_WIDTH,
        height=FOODGRAM_LOGO_HEIGHT,
        preserveAspectRatio=True,
    )
    pdf.setFont(SHOPPING_CART_FONT_NAME, TITLE_FONT_SIZE)
    pdf.drawString(LEFT_MARGIN, TOP_MARGIN, 'Список покупок')
    pdf.setFont(SHOPPING_CART_FONT_NAME, TEXT_FONT_SIZE)
    pdf.line(LINE_START, LINE_Y_POSITION, LINE_END, LINE_Y_POSITION)
    y_position = INITIAL_Y_POSITION
    for index, ((name, unit), amount) in enumerate(
        ingredients.items(), START_INDEX
    ):
        text = f'{index}. {name} — {amount} {unit}'
        pdf.drawString(LEFT_MARGIN, y_position, text)
        y_position -= LINE_HEIGHT
        if y_position < BOTTOM_MARGIN:
            pdf.showPage()
            pdf.setFont(SHOPPING_CART_FONT_NAME, TEXT_FONT_SIZE)
            y_position = NEW_PAGE_Y_POSITION
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
