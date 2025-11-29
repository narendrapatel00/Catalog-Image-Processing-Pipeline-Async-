from PIL import Image
from pathlib import Path

def process_image(input_path: str, output_path: str, max_size=(800,800), quality=70):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as img:
        width_before, height_before = img.size
        img.thumbnail(max_size)
        img.save(output_path, optimize=True, quality=quality)
        width_after, height_after = img.size

    return {
        "width_before": width_before,
        "height_before": height_before,
        "width_after": width_after,
        "height_after": height_after
    }
