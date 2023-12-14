"""
(c) Adhish Thite

Test cases for generator.py

test_generator.py
"""

import pytest
from app.core.generator import OTPGenerator


class TestOTPGenerator:
    """
    Test cases for OTPGenerator class
    """

    @pytest.mark.parametrize("length, alphanumeric, length_expected, check_method", [
        (None, False, 6, 'isnumeric'),
        (8, False, 8, 'isnumeric'),
        (None, True, 6, 'isalnum'),
        (8, True, 8, 'isalnum'),
        (100, None, 100, 'isnumeric'),
        (100, False, 100, 'isalnum'),
    ])
    def test_generate_otp(self, length, alphanumeric, length_expected, check_method):
        """
        Parametrized test for the generate_otp() function.
        """
        if length is None:
            otp = OTPGenerator(alphanumeric=alphanumeric).generate_otp()
        else:
            otp = OTPGenerator(length=length, alphanumeric=alphanumeric).generate_otp()

        assert len(otp) == length_expected
        assert getattr(otp, check_method)()