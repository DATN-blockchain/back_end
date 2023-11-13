import json
import base64
import gzip
import bz2


def compress_json(data):
    json_string = json.dumps(data)
    compressed_data = bz2.compress(json_string.encode('utf-8'))
    base64_str = base64.b64encode(compressed_data).decode('utf-8')
    return base64_str


def decompress_json(base64_str):
    compressed_data = base64.b64decode(base64_str)
    json_string = bz2.decompress(compressed_data).decode('utf-8')
    data = json.loads(json_string)
    return data


def compress_bytes(data_bytes):
    return gzip.compress(data_bytes)


def decompress_bytes_to_json(compressed_bytes):
    json_string = gzip.decompress(compressed_bytes).decode('utf-8')
    data = json.loads(json_string)

    return data


def encode_base4(data):
    base64_str = base64.b64encode(data).decode('utf-8')
    return base64_str


def decode_base64(base64_str):
    compressed_data = base64.b64decode(base64_str)
    decompressed_data = decompress_json(compressed_data)

    return decompressed_data


def write_binary_to_file(binary_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(binary_data)


def read_binary_from_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return binary_data


def encode_json(data):
    compressed_and_encoded = compress_json(data)
    return compressed_and_encoded


def decode_data(encode):
    decompressed_data = decompress_json(encode)
    return decompressed_data


