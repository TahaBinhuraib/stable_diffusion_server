import io
import os


def get_bytes(file_path):
    return_data = io.BytesIO()
    with open(file_path, "rb") as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(file_path)
    return return_data
