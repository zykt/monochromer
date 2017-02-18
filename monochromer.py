from PIL import Image


def convert(path, output_path='output.png'):
    """
    Converts an image at :path: to greyscale and saves it at :output_path:
    """
    img = Image.open(path)
    out = img.convert('L')
    out.save(output_path)


if __name__ == '__main__':
    convert('image/image.png', 'image/output.png')
