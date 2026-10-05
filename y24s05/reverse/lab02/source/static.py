#!/usr/bin/env python3
"""Find XOR key and decode the data."""

import argparse
import sys

DECODER_STUB_END: bytes = b'\xe8\xd8\xff\xff\xff'
MARKER_CONSTANT: int = 0xfc


def extract_key(data: bytes) -> tuple[int, int] | None:
    """
    Extract the dynamic key from the binary data.

    Args:
        data (bytes): The binary data read from the file.

    Returns:
        Optional[int]: The dynamic key as an integer if found and valid, otherwise None.
    """
    pos = data.find(DECODER_STUB_END)
    if pos == -1:
        return None

    key_start = pos + len(DECODER_STUB_END)
    if key_start + 4 > len(data):
        return None

    key_block = data[key_start: key_start + 4]
    key_value = key_block[0]
    marker = key_block[1]

    marker_pos = key_start + data[key_start:].find(bytes([marker, MARKER_CONSTANT]))
    if marker_pos == -1:
        return None

    return key_value, marker_pos + 2


def xor_decode(data: bytes, key: int) -> bytes:
    """Decode data using XOR with the provided key.

    Args:
        data: Data to decode
        key: Key value for XOR operation

    Returns:
        Decoded bytes
    """
    return bytes(b ^ key for b in data)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract dynamic key from a binary file containing a decoder stub."
    )

    parser.add_argument("filename", help="Path to the binary file")

    args = parser.parse_args()

    try:
        with open(args.filename, "rb") as file:
            file_data = file.read()
    except Exception as err:
        sys.exit(f'[!] Error reading file {err}')

    key_value, data_offset = extract_key(file_data)
    if key_value is None:
        sys.exit("Dynamic key not found in the file.")

    print(f"[+] Found key value: 0x{key_value:02x}")
    print(f"[+] Data offset: 0x{data_offset:x}")

    encoded_data = file_data[data_offset:]
    decoded = xor_decode(encoded_data, key_value)

    print(f'[i] Output data:\n{decoded}')

    output_path = args.filename + '.decoded'
    try:
        with open(output_path, "wb") as file:
            file.write(decoded.strip())
        print(f'[+] Decoded data saved to: {output_path}')
    except Exception as err:
        sys.exit(f'[!] Error occurred while saving decoded data: {err}')


if __name__ == "__main__":
    main()
