#!/usr/bin/env python3
"""x86_64 code emulator."""

import argparse
import sys
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_32, Cs

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_32, Uc
from unicorn.x86_const import UC_X86_REG_ESP


def create_disassembler() -> Cs:
    """
    Create and configure Capstone disassembler.

    Returns:
        Configured Capstone disassembler instance.
    """
    return Cs(CS_ARCH_X86, CS_MODE_32)


def hook_code(uc: Uc, address: int, size: int, _user_data: Any):
    """
    Hook the callback for code execution.

    Args:
        uc (Uc): Unicorn engine instance.
        address (int): Current instruction address.
        size (int): Size of the instruction.
        _user_data: Unused.
    """
    cs = create_disassembler()
    instruction = uc.mem_read(address, size)

    for i in cs.disasm(instruction, address):
        print(
            f"hook 0x{address:03x} "
            f"size {size:2d} "
            f"0x{i.address:03x}: "
            f"{i.bytes.hex():20s} "
            f"{i.mnemonic} {i.op_str}"
        )


def emulate_code(code: bytes, base_addr: int = 0) -> None:
    """
    Emulate provided x86_64 code.

    Args:
        code (bytes): Binary code to emulate.
        base_addr (int): Base address for code loading.
    """
    mu = Uc(UC_ARCH_X86, UC_MODE_32)

    mu.mem_map(base_addr, base_addr + 0x2000)
    mu.mem_write(base_addr, code)
    mu.reg_write(UC_X86_REG_ESP, base_addr + 0x1000)

    mu.hook_add(UC_HOOK_CODE, hook_code)

    #  mitigate Invalid memory fetch error
    mu.emu_start(base_addr, base_addr + len(code) + 1)

    #  0x2a - size of the decoder
    #  needed some tweaking to display clear decoded text
    print(mu.mem_read(0x2a + 2, len(code) - 0x2a - 4))
    print('[+] Emulation completed!')


def read_file(file_path: str) -> bytes | None:
    """
    Read binary file content.

    Args:
        file_path (str): Path to binary file.

    Returns:
        bytes | None: File content as bytes or None if error occurs.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError as err:
        print(f'[!] Error reading file: {err}', file=sys.stderr)
        return None


def main() -> None:
    """Start here."""
    parser = argparse.ArgumentParser(
        description='Emulate x86_64 binary code using Unicorn engine.'
    )

    parser.add_argument(
        'filename',
        help='Path to binary file'
    )

    args = parser.parse_args()

    code = read_file(args.filename)
    if code is None:
        sys.exit(1)

    try:
        emulate_code(code)
    except Exception as err:
        print(f'[!] Emulation error: {err}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
