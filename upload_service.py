from PIL import ImageDraw, Image, ImageFont

def watermark(img, text="KEYZ"):
    # Ensure image is in RGBA mode for transparency compositing
    img = img.convert("RGBA")

    # Create a transparent layer the same size as the image
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Use a smaller font size (36 instead of 72)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        # Fallback just in case arial.ttf isn't found on the server
        font = ImageFont.load_default()

    # Get the bounding box of the text to calculate its width and height
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate X and Y to place the text exactly in the middle
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    # Draw the text
    # Color: White (255, 255, 255)
    # Alpha (Opacity): 0.3 * 255 = ~77
    draw.text(
        (x, y),
        text,
        fill=(255, 255, 255, 77),
        font=font
    )

    # Composite the watermark layer over the original image
    return Image.alpha_composite(img, layer).convert("RGBA")