#!/usr/bin/env python3
"""Odczytuje sekret zapieczetowany w vault.bin i wypisuje go na konsole.

Format vault.bin:
    magic      9B   b"BUDDYVLT1"
    salt      16B   losowy
    iters      4B   big-endian uint32 (liczba iteracji PBKDF2-HMAC-SHA256)
    len        2B   big-endian uint16 (dlugosc szyfrogramu)
    ciphertext len  sekret XOR keystream
    mac       32B   HMAC-SHA256 calego naglowka + szyfrogramu

Keystream i klucz MAC sa wyprowadzane z passphrase + salt przez PBKDF2, wiec
sam podglad plikow (vault.bin ani tego skryptu) nie ujawnia sekretu - trzeba
ten skrypt uruchomic.
"""
import hashlib
import hmac
import struct
import sys
from pathlib import Path

MAGIC = b"BUDDYVLT1"
PASSPHRASE = b"buddy-vault-2026"
HEADER_LEN = len(MAGIC) + 16 + 4 + 2
MAC_LEN = 32


def unseal(blob: bytes) -> str:
    if len(blob) < HEADER_LEN + MAC_LEN or not blob.startswith(MAGIC):
        raise ValueError("to nie jest prawidlowy vault.bin")

    salt = blob[len(MAGIC):len(MAGIC) + 16]
    iters, = struct.unpack(">I", blob[len(MAGIC) + 16:len(MAGIC) + 20])
    ct_len, = struct.unpack(">H", blob[len(MAGIC) + 20:HEADER_LEN])

    body = blob[:HEADER_LEN + ct_len]
    ct = body[HEADER_LEN:]
    mac = blob[HEADER_LEN + ct_len:HEADER_LEN + ct_len + MAC_LEN]

    if len(ct) != ct_len:
        raise ValueError("vault.bin jest obciety")

    mac_key = hashlib.pbkdf2_hmac("sha256", PASSPHRASE, salt + b"mac", iters, dklen=32)
    if not hmac.compare_digest(hmac.new(mac_key, body, hashlib.sha256).digest(), mac):
        raise ValueError("vault.bin nie przechodzi weryfikacji HMAC (uszkodzony lub podmieniony)")

    keystream = hashlib.pbkdf2_hmac("sha256", PASSPHRASE, salt, iters, dklen=ct_len)
    return bytes(a ^ b for a, b in zip(ct, keystream)).decode()


def main() -> int:
    default_vault = Path(__file__).resolve().parent.parent / "vault.bin"
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else default_vault

    if not vault.is_file():
        print(f"blad: nie znaleziono vault.bin pod {vault}", file=sys.stderr)
        return 1

    try:
        secret = unseal(vault.read_bytes())
    except ValueError as exc:
        print(f"blad: {exc}", file=sys.stderr)
        return 1

    print(secret)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
