import mock
import os
import pytest
from rawkit.errors import InvalidFileType, NoFileSpecified
from rawkit.metadata import Metadata
from rawkit.raw import Raw, DarkFrame


@pytest.fixture
def input_file():
    return 'potato_salad.CR2'


@pytest.fixture
def output_file():
    return 'potato_salad.out'


@pytest.yield_fixture
def raw(input_file):
    with mock.patch('rawkit.raw.LibRaw'):
        with Raw(filename=input_file) as raw_obj:
            yield raw_obj
        raw_obj.libraw.libraw_close.assert_called_once_with(raw_obj.data)


@pytest.yield_fixture
def dark_frame(input_file):
    with mock.patch('rawkit.raw.LibRaw'):
        with DarkFrame(filename=input_file) as raw_obj:
            yield raw_obj
        raw_obj.libraw.libraw_close.assert_called_once_with(raw_obj.data)


def test_create(raw, input_file):
    raw.libraw.libraw_init.assert_called_once_with(0)
    raw.libraw.libraw_open_file.assert_called_once_with(
        raw.data,
        input_file.encode('ascii'),
    )


def test_create_no_filename():
    with pytest.raises(NoFileSpecified):
        Raw()


def test_dark_frame_is_raw(dark_frame):
    assert isinstance(dark_frame, Raw)


def test_unpack(raw):
    raw.unpack()
    raw.libraw.libraw_unpack.assert_called_once_with(raw.data)


def test_unpack_twice(raw):
    raw.unpack()
    raw.unpack()
    raw.libraw.libraw_unpack.assert_called_once_with(raw.data)


def test_unpack_thumb(raw):
    raw.unpack_thumb()
    raw.libraw.libraw_unpack_thumb.assert_called_once_with(raw.data)


def test_unpack_thumb_twice(raw):
    raw.unpack_thumb()
    raw.unpack_thumb()
    raw.libraw.libraw_unpack_thumb.assert_called_once_with(raw.data)


def test_save_dark_frame_cached(dark_frame, tmpdir):
    dark_frame.save()

    # Touch the file (as if LibRaw were installed and saved a file)
    with open(dark_frame.name, 'a'):
        pass

    dark_frame.save()
    dark_frame.libraw.libraw_dcraw_ppm_tiff_writer.assert_called_once_with(
        dark_frame.data,
        dark_frame.name.encode('ascii'),
    )


def test_save_dark_frame_with_filename_cached(dark_frame, tmpdir):
    tmpdir.join('somefile').write('')
    fn = os.path.join(str(tmpdir), 'somefile')
    dark_frame.save(filename=fn)
    dark_frame.save(filename=fn, filetype='tiff')
    assert not dark_frame.libraw.libraw_dcraw_ppm_tiff_writer.called


def _test_save(raw, output_file, filetype):
    raw.save(filename=output_file, filetype=filetype)

    raw.libraw.libraw_dcraw_ppm_tiff_writer.assert_called_once_with(
        raw.data,
        output_file.encode('ascii'),
    )


def test_save_no_filename(raw):
    with pytest.raises(NoFileSpecified):
        raw.save(filetype='ppm')


def test_save_ppm(raw, output_file):
    _test_save(raw, output_file, 'ppm')


def test_save_tiff(raw, output_file):
    _test_save(raw, output_file, 'tiff')


def test_save_invalid(raw, output_file):
    with pytest.raises(InvalidFileType):
        _test_save(raw, output_file, 'jpg')


def test_save_thumb(raw, output_file):
    raw.save_thumb(filename=output_file)

    raw.libraw.libraw_dcraw_thumb_writer.assert_called_once_with(
        raw.data,
        output_file.encode('ascii'),
    )


def test_save_thumb_no_filename(raw):
    with pytest.raises(NoFileSpecified):
        raw.save_thumb()


def test_to_buffer(raw):
    # Quick hack because to_buffer does some ctypes acrobatics
    with mock.patch('rawkit.raw.ctypes'):
        raw.to_buffer()

    raw.libraw.libraw_dcraw_make_mem_image.assert_called_once_with(
        raw.data,
    )

    raw.libraw.libraw_dcraw_clear_mem.assert_called_once_with(
        raw.libraw.libraw_dcraw_make_mem_image(raw.data),
    )


def test_thumbnail_to_buffer(raw):
    # Quick hack because thumbnail_to_buffer does some ctypes acrobatics
    with mock.patch('rawkit.raw.ctypes'):
        raw.thumbnail_to_buffer()

    raw.libraw.libraw_dcraw_make_mem_thumb.assert_called_once_with(
        raw.data,
    )

    raw.libraw.libraw_dcraw_clear_mem.assert_called_once_with(
        raw.libraw.libraw_dcraw_make_mem_thumb(raw.data),
    )


def test_metadata(raw):
    metadata = raw.metadata
    assert type(metadata) is Metadata
