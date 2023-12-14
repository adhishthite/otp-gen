"""
(c) Adhish Thite

This module contains functions to generate OTPs

generator.py
"""

import secrets
import string


class OTPGenerator:
    """
    This class contains functions to generate OTPs
    """

    def __init__(self, meta: dict = None, length: int = 6, alphanumeric: bool = False, ttl: int = 3600, **kwargs):
        self.length = length
        self.alphanumeric = alphanumeric
        self.kwargs = kwargs
        self.meta = meta or {}

    def generate_otp(self) -> str:
        """
        Generate a random OTP

        :return: OTP (str)
        """

        if self.alphanumeric:
            alphabet = string.ascii_letters + string.digits
        else:
            alphabet = string.digits

        return "".join(secrets.choice(alphabet) for _ in range(self.length))