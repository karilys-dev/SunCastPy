import shutil
import tempfile


def create_temp_dir():
    return tempfile.mkdtemp(prefix="suncastpy_")


def cleanup_temp_dir(path):
    shutil.rmtree(path, ignore_errors=True)
