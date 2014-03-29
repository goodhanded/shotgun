from tester import *

from PIL import Image
from PIL import PngImagePlugin

codecs = dir(Image.core)

if "zip_encoder" not in codecs or "zip_decoder" not in codecs:
    skip("zip/deflate support not available")

# sample png stream

file = "Images/lena.png"
data = open(file, "rb").read()

# stuff to create inline PNG images

MAGIC = PngImagePlugin._MAGIC

def chunk(cid, *data):
    file = StringIO()
    apply(PngImagePlugin.putchunk, (file, cid) + data)
    return file.getvalue()

o32 = PngImagePlugin.o32

IHDR = chunk("IHDR",  o32(1), o32(1), chr(8)+chr(2), chr(0)*3)
IDAT = chunk("IDAT")
IEND = chunk("IEND")

HEAD = MAGIC + IHDR
TAIL = IDAT + IEND

def load(data):
    return Image.open(StringIO(data))

def roundtrip(im, **options):
    out = StringIO()
    im.save(out, "PNG", **options)
    out.seek(0)
    return Image.open(out)

# --------------------------------------------------------------------

def test_sanity():

    # internal version number
    assert_match(Image.core.zlib_version, "\d+\.\d+\.\d+(\.\d+)?$")

    file = tempfile("temp.png")

    lena("RGB").save(file)

    im = Image.open(file)
    im.load()
    assert_equal(im.mode, "RGB")
    assert_equal(im.size, (128, 128))
    assert_equal(im.format, "PNG")

    lena("1").save(file)
    im = Image.open(file)

    lena("L").save(file)
    im = Image.open(file)

    lena("P").save(file)
    im = Image.open(file)

    lena("RGB").save(file)
    im = Image.open(file)

    lena("I").save(file)
    im = Image.open(file)

# --------------------------------------------------------------------

def test_broken():
    # Check reading of totally broken files.  In this case, the test
    # file was checked into Subversion as a text file.

    file = "Tests/images/broken.png"
    assert_exception(IOError, lambda: Image.open(file))

def test_bad_text():
    # Make sure PIL can read malformed tEXt chunks (@PIL152)

    im = load(HEAD + chunk('tEXt') + TAIL)
    assert_equal(im.info, {})

    im = load(HEAD + chunk('tEXt', 'spam') + TAIL)
    assert_equal(im.info, {'spam': ''})

    im = load(HEAD + chunk('tEXt', 'spam\0') + TAIL)
    assert_equal(im.info, {'spam': ''})

    im = load(HEAD + chunk('tEXt', 'spam\0egg') + TAIL)
    assert_equal(im.info, {'spam': 'egg'})

    im = load(HEAD + chunk('tEXt', 'spam\0egg\0') + TAIL)
    assert_equal(im.info,  {'spam': 'egg\x00'})

def test_interlace():

    file = "Tests/images/pil123p.png"
    im = Image.open(file)

    assert_image(im, "P", (162, 150))
    assert_true(im.info.get("interlace"))

    assert_no_exception(lambda: im.load())

    file = "Tests/images/pil123rgba.png"
    im = Image.open(file)

    assert_image(im, "RGBA", (162, 150))
    assert_true(im.info.get("interlace"))

    assert_no_exception(lambda: im.load())

def test_load_transparent_p():
    file = "Tests/images/pil123p.png"
    im = Image.open(file)

    assert_image(im, "P", (162, 150))
    im = im.convert("RGBA")
    assert_image(im, "RGBA", (162, 150))

    # image has 124 uniqe qlpha values
    assert_equal(len(im.split()[3].getcolors()), 124)

def test_load_verify():
    # Check open/load/verify exception (@PIL150)

    im = Image.open("Images/lena.png")
    assert_no_exception(lambda: im.verify())

    im = Image.open("Images/lena.png")
    im.load()
    assert_exception(RuntimeError, lambda: im.verify())

    # see test_image_verify for additional tests

def test_roundtrip_dpi():
    # Check dpi roundtripping

    im = Image.open(file)

    im = roundtrip(im, dpi=(100, 100))
    assert_equal(im.info["dpi"], (100, 100))

def test_roundtrip_text():
    # Check text roundtripping

    im = Image.open(file)

    info = PngImagePlugin.PngInfo()
    info.add_text("TXT", "VALUE")
    info.add_text("ZIP", "VALUE", 1)

    im = roundtrip(im, pnginfo=info)
    assert_equal(im.info, {'TXT': 'VALUE', 'ZIP': 'VALUE'})
    assert_equal(im.text, {'TXT': 'VALUE', 'ZIP': 'VALUE'})

def test_scary():
    # Check reading of evil PNG file.  For information, see:
    # http://scary.beasts.org/security/CESA-2004-001.txt

    import base64
    file = "Tests/images/pngtest_bad.png.base64"
    data = base64.decodestring(open(file).read())
    file = StringIO(data)
    assert_exception(IOError, lambda: Image.open(file))

def test_trns_rgb():
    # Check writing and reading of tRNS chunks for RGB images.
    # Independent file sample provided by Sebastian Spaeth.

    file = "Tests/images/caption_6_33_22.png"
    im = Image.open(file)
    assert_equal(im.info["transparency"], (248, 248, 248))

    im = roundtrip(im, transparency=(0, 1, 2))
    assert_equal(im.info["transparency"], (0, 1, 2))
