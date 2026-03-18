import os
from PIL import Image, ImageDraw, ImageFont
from config import ROOT_DIR, get_fonts_dir, get_font

def generate_thumbnail(image_path: str, title: str, output_path: str = None) -> str:
    """
    Generates a YouTube thumbnail from an image and title text.

    Args:
        image_path: Path to the base image
        title: Video title to overlay
        output_path: Output path (default: .mp/thumbnail.png)

    Returns:
        path: Path to the generated thumbnail
    """
    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", "thumbnail.png")

    # Open and resize image to YouTube thumbnail size (1280x720)
    img = Image.open(image_path)
    img = img.resize((1280, 720), Image.LANCZOS)

    draw = ImageDraw.Draw(img)

    # Add a semi-transparent dark overlay at the bottom
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [(0, 480), (1280, 720)],
        fill=(0, 0, 0, 160)
    )
    img = Image.alpha_composite(img.convert('RGBA'), overlay)

    draw = ImageDraw.Draw(img)

    # Load font
    font_path = os.path.join(get_fonts_dir(), get_font())
    try:
        font = ImageFont.truetype(font_path, 60)
    except Exception:
        font = ImageFont.load_default()

    # Truncate title if too long
    if len(title) > 40:
        title = title[:37] + "..."

    # Draw title text with outline
    text_x = 40
    text_y = 560
    # Black outline
    for dx in [-3, -2, 0, 2, 3]:
        for dy in [-3, -2, 0, 2, 3]:
            draw.text((text_x + dx, text_y + dy), title, font=font, fill=(0, 0, 0))
    # White text
    draw.text((text_x, text_y), title, font=font, fill=(255, 255, 0))

    # Save as PNG (convert back to RGB for saving)
    img.convert('RGB').save(output_path, 'PNG')

    return output_path
