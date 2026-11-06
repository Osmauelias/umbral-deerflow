"""Normalize folio identifiers to the canonical UMB-NNN form."""

import re


_FOLIO_PATTERN = re.compile(r"(?:UMB-)?[0-9]+\Z")


def normalizar_folio(folio: str) -> str:
    """Return a normalized folio, or raise ValueError for invalid input.

    Surrounding whitespace is removed, letters are uppercased, and a missing
    ``UMB-`` prefix is added. Internal whitespace and any non-digit suffix or
    prefix are rejected. Leading zeroes are preserved.
    """
    if not isinstance(folio, str):
        raise ValueError("El folio debe ser texto")

    folio = folio.strip().upper()
    if not folio or not _FOLIO_PATTERN.fullmatch(folio):
        raise ValueError("Folio inválido")

    if folio.startswith("UMB-"):
        return folio
    return f"UMB-{folio}"
