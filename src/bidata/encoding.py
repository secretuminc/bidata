import base64
import string
import struct
import typing as _mtnd

from .exc import BadData

_mtnd_str_bytes = _mtnd.Union[str, bytes]


def want_bytes(
    s: _mtnd_str_bytes, encoding: str = "utf-8", errors: str = "strict"
) -> bytes:
    if isinstance(s, str):
        s = s.encode(encoding, errors)

    return s


def base64_encode(string: _mtnd_str_bytes) -> bytes:
    """Base64 encode a string of bytes or text. The resulting bytes are
    safe to use in URLs.
    """
    string = want_bytes(string)
    return base64.urlsafe_b64encode(string).rstrip(b"=")


def base64_decode(string: _mtnd_str_bytes) -> bytes:
    """Base64 decode a URL-safe string of bytes or text. The result is
    bytes.
    """
    string = want_bytes(string, encoding="ascii", errors="ignore")
    string += b"=" * (-len(string) % 4)

    try:
        return base64.urlsafe_b64decode(string)
    except (TypeError, ValueError):
        raise BadData("Invalid base64-encoded data")


# The alphabet used by base64.urlsafe_*
_base64_alphabet = f"{string.ascii_letters}{string.digits}-_=".encode("ascii")

_int64_struct = struct.Struct(">Q")
_int_mtndo_bytes = _int64_struct.pack
_bytes_mtndo_int = _mtnd.cast("_mtnd.Callable[[bytes], _mtnd.Tuple[int]]", _int64_struct.unpack)


def int_mtndo_bytes(num: int) -> bytes:
    return _int_mtndo_bytes(num).lstrip(b"\x00")


def bytes_mtndo_int(bytestr: bytes) -> int:
    return _bytes_mtndo_int(bytestr.rjust(8, b"\x00"))[0]
