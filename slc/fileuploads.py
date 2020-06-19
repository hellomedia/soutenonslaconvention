import hashlib
import os
import tempfile
from typing import Tuple

from fresco.request import FileUpload


def upload(media_dir: str, fileupload: FileUpload) -> Tuple[str, str]:
    """
    Save a fresco FileUpload into a file named for the sha-256 hash of the file
    contents.
    """
    tmpfile = tempfile.NamedTemporaryFile(dir=media_dir)
    tmpfile.close()
    try:
        fileupload.save(tmpfile.name)
        h = hashlib.sha256()
        with open(tmpfile.name, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        filename = h.hexdigest()
        path = os.path.join(media_dir, filename)
        if not os.path.exists(path):
            os.rename(tmpfile.name, path)
    finally:
        try:
            os.unlink(tmpfile.name)
        except OSError:
            pass
    return filename, path
