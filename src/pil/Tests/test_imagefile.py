from tester import *

from PIL import Image
from PIL import ImageFile

# save original block sizes
MAXBLOCK = ImageFile.MAXBLOCK
SAFEBLOCK = ImageFile.SAFEBLOCK

def test_parser():

    def roundtrip(format):

        im = lena("L").resize((1000, 1000))
        if format in ("MSP", "XBM"):
            im = im.convert("1")

        file = StringIO()

        im.save(file, format)

        data = file.getvalue()

        parser = ImageFile.Parser()
        parser.feed(data)
        imOut = parser.close()

        return im, imOut

    assert_image_equal(*roundtrip("BMP"))
    assert_image_equal(*roundtrip("GIF"))
    assert_image_equal(*roundtrip("IM"))
    assert_image_equal(*roundtrip("MSP"))
    try:
        # force multiple blocks in PNG driver
        ImageFile.MAXBLOCK = 8192
        assert_image_equal(*roundtrip("PNG"))
    finally:
        ImageFile.MAXBLOCK = MAXBLOCK
    assert_image_equal(*roundtrip("PPM"))
    assert_image_equal(*roundtrip("TIFF"))
    assert_image_equal(*roundtrip("XBM"))

    im1, im2 = roundtrip("JPEG") # lossy compression
    assert_image(im1, im2.mode, im2.size)

    assert_exception(IOError, lambda: roundtrip("PCX"))
    assert_exception(IOError, lambda: roundtrip("PDF"))


def test_safeblock():

    im1 = lena()

    try:
        ImageFile.SAFEBLOCK = 1
        im2 = fromstring(tostring(im1, "PNG"))
    finally:
        ImageFile.SAFEBLOCK = SAFEBLOCK
    
    assert_image_equal(im1, im2)
