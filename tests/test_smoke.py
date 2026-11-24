"""Smoke-Test: Das Paket ist installiert und importierbar.

pytest bricht mit Exit-Code 5 ab, wenn es keine Tests findet. Dieser Test hält die CI
grün, bis echte Tests aus AP2–AP4 dazukommen.
"""

from importlib.metadata import version

import tender_ingest


def test_package_is_importable() -> None:
    assert callable(tender_ingest.main)


def test_package_is_installed() -> None:
    # Funktioniert nur, wenn das Paket installiert ist (src-Layout), nicht bloß als Ordner im Pfad.
    assert version("tender-ingest")
