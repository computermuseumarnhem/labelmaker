import os
import sys
from typing import Optional

import barcode
import click
from PIL import Image
from barcode.ean import SIZES
from barcode.writer import ImageWriter


@click.command()
@click.option('--start', type=int, help='Start inventory number')
@click.option('--end', type=int, default=-1, help='End inventory number (optional, if not specified only one label will'
                                                  'be printed')
@click.option('--dpi', type=int, default=200, help='DPI of generated image (default 200)')
@click.option('--image_size', type=float, default=4, help='Image size in cm (default 4)')
@click.option('--font_size', type=int, default=25, help='Font size in pt (default 25)')
@click.option('--module_width', type=float, default=None, help='Force module_width (mm), default is to use the largest'
                                                               'module_width that fits')
@click.option('--printer', type=str, default="", help="Print each label to printer")
def main(start, end, dpi, image_size, font_size, module_width, printer):
    if end == -1:
        end = start

    for code in range(start, end+1):
        image_name = f'{code}.png'
        click.echo(f'Generating {image_name}')

        width, height = _calculate_image_dimensions(dpi, image_size)
        barcode_image = _render_barcode(width, height, font_size, code, dpi, module_width)

        barcode_width, barcode_height = barcode_image.size

        image = Image.new('RGB', (width, height), (255, 255, 255))

        image.paste(barcode_image, ((width-barcode_width)//2, (height-barcode_height)//2))

        image.save(image_name)

        if printer:
            os.system(f'lpr -P "{printer}" "{image_name}"')


def _calculate_image_dimensions(dpi, image_size_cm):
    image_size_inch = image_size_cm / 2.54
    image_size_px = int(image_size_inch * dpi)
    return image_size_px, image_size_px


def _render_barcode(max_width: int, max_height: int, font_size: int, code: int, dpi: int, module_width: Optional[float]):
    if module_width:
        image = _render_barcode_with_size(code, dpi, font_size, module_width)
        width, height = image.size
        if width <= max_width and height <= max_height:
            return image
        click.echo('module_width too large to fit barcode in image')
        sys.exit(-1)

    for size in reversed(sorted(SIZES.keys())):  # try size from big to small until it fits
        image = _render_barcode_with_size(code, dpi, font_size, SIZES[size])
        width, height = image.size
        if width <= max_width and height <= max_height:
            return image

    click.echo('Image size too small to render EAN compliant barcode, consider using --module_width')
    sys.exit(-1)


def _render_barcode_with_size(code: int, dpi: int, font_size: int, module_width: float):
    code_str = f'{code:012}'
    ean = barcode.get('ean13', code_str, writer=ImageWriter())
    ean.writer.dpi = dpi
    image = ean.render(writer_options={'module_width': module_width, 'font_size': font_size}, text=f'{code}')
    return image


if __name__ == '__main__':
    main()
