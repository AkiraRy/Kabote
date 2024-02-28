import sys
# note add font selector
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

TOP_PADDING_IN_PIXELS = -25
BOTTOM_PADDING_IN_PIXELS = 6
BASE_LEFT_PADDING_IN_PIXELS = 6
BASE_RIGHT_PADDING_IN_PIXELS = 6
TOTAL_VERTICAL_PADDING_IN_PIXELS = TOP_PADDING_IN_PIXELS + BOTTOM_PADDING_IN_PIXELS

FONT_FILE = 'KleeOne-Regular.ttf'
FONT_PATH = os.path.join(os.getcwd(), FONT_FILE)
# Create a font object
font = ImageFont.truetype(FONT_PATH, size=100)


def render(text, text_color=(0, 0, 0), background_color=(255, 255, 255), font_size=96):

    measurements = ImageDraw.Draw(Image.new('RGB', (1, 1))).multiline_textbbox((0, 0), text, font=font)

    left_padding_in_pixels = BASE_LEFT_PADDING_IN_PIXELS * ((len(text) // 4) + 1)
    right_padding_in_pixels = BASE_RIGHT_PADDING_IN_PIXELS * ((len(text) // 4) + 1)
    total_horizontal_padding_in_pixels = left_padding_in_pixels + right_padding_in_pixels

    canvas_width = measurements[2] + total_horizontal_padding_in_pixels
    canvas_height = measurements[3] + TOTAL_VERTICAL_PADDING_IN_PIXELS

    # Create a new image with the specified background color
    image = Image.new('RGB', (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw the text on the image with the specified text color and padding
    draw.text(
        (left_padding_in_pixels, TOP_PADDING_IN_PIXELS),
        text,
        font=font,
        fill=text_color
    )

    buffer = BytesIO()
    image.save(buffer, format='PNG')  # You can choose another format if needed

    # Return the bytes from the buffer
    return buffer.getvalue()


# render("夏休み")