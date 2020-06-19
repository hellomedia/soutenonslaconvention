import hashlib
import os
import tempfile
from typing import Callable
from typing import IO
from typing import Tuple
from contextlib import contextmanager

from fresco.request import FileUpload


def upload(media_dir: str, fileupload: FileUpload) -> Tuple[str, str]:
    """
    Save a fresco FileUpload into a file named for the sha-256 hash of the file
    contents.
    """
    with content_addressed_file(media_dir) as (f, get_filename):
        fileupload.save(f.name)
    return get_filename()


@contextmanager
def content_addressed_file(dir: str) -> Tuple[IO, Callable[[], str]]:
    filename = None

    def ca_filename():
        return filename

    tmpfile = tempfile.NamedTemporaryFile(dir=dir, delete=False)
    try:
        yield tmpfile, ca_filename
        tmpfile.flush()
        tmpfile.close()
        h = hashlib.sha256()
        with open(tmpfile.name, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        filename = h.hexdigest()
        path = os.path.join(dir, filename)
        if not os.path.exists(path):
            os.rename(tmpfile.name, path)
    finally:
        try:
            os.unlink(tmpfile.name)
        except OSError:
            pass
