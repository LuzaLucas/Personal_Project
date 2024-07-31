from PIL import Image


def resize_image(image_path, new_width=480):
    image_pillow = Image.open(image_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return

    new_height = round((new_width * original_height) / original_width)
    new_image = image_pillow.resize((new_width, new_height), resample=Image.LANCZOS) # type: ignore

    if new_image.mode == 'RGBA':
        new_image = new_image.convert('RGB')

    image_pillow.close()

    new_image.save(
        image_path,
        optimize=True,
        quality=80,
    )