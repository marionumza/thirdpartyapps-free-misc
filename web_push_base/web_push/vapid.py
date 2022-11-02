# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from py_vapid import b64urlencode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from typing import Tuple


def generate_vapid() -> Tuple[str, str]:
    """
    :return: Private key and Public Key
    """
    server_key = ec.generate_private_key(ec.SECP256R1, default_backend())
    public_bytes = server_key.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    private_bytes = server_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return b64urlencode(private_bytes), b64urlencode(public_bytes)
