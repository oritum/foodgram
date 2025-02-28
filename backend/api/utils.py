"""Утилиты для приложения api."""

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from core.constants import (
    FOODGRAM_LOGO_HEIGHT,
    FOODGRAM_LOGO_PATH,
    FOODGRAM_LOGO_WIDTH,
    SHOPPING_CART_FONT,
)


def generate_shopping_list_pdf(
    ingredients: dict[tuple[str, str], int],
) -> BytesIO:
    """Генерация PDF-файла со списком покупок."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(TTFont('DejaVu', SHOPPING_CART_FONT))

    pdf.drawImage(
        FOODGRAM_LOGO_PATH,
        2 * cm,
        27 * cm,
        width=FOODGRAM_LOGO_WIDTH * cm,
        height=FOODGRAM_LOGO_HEIGHT * cm,
        preserveAspectRatio=True,
    )
    pdf.setFont('DejaVu', 16)
    pdf.drawString(2 * cm, 27 * cm, 'Список покупок')
    pdf.setFont('DejaVu', 12)
    pdf.line(2 * cm, 26.8 * cm, 18 * cm, 26.8 * cm)
    y_position = 25 * cm
    for index, ((name, unit), amount) in enumerate(ingredients.items(), 1):
        text = f'{index}. {name} — {amount} {unit}'
        pdf.drawString(2 * cm, y_position, text)
        y_position -= 1 * cm
        if y_position < 2 * cm:
            pdf.showPage()
            pdf.setFont('DejaVu', 12)
            y_position = 27 * cm
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
