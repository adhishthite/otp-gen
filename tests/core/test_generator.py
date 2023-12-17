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
        (100, False, 100, 'isalnum'),
    ])
    def test_generate_otp(self, length, alphanumeric, length_expected, check_method):
        """
        Parametrized test for the generate_otp() function.
        """
        if length is None:
            otp = OTPGenerator(alphanumeric=alphanumeric).otp_dict['otp']
        else:
            otp = OTPGenerator(length=length, alphanumeric=alphanumeric).otp_dict['otp']

        assert len(otp) == length_expected
        assert getattr(otp, check_method)()

    def test_generate_meta(self):
        otp_gen1 = OTPGenerator()
        otp_gen2 = OTPGenerator()

        meta1 = otp_gen1.otp_dict['meta']
        meta2 = otp_gen2.otp_dict['meta']

        assert 'id' in meta1 and 'id' in meta2
        assert meta1['id'] != meta2['id']

    def test_ttl_functionality(self):
        ttl = 120
        otp_gen = OTPGenerator(ttl=ttl)
        otp_info = otp_gen.otp_dict['otp_info']

        assert otp_info['ttl'] == ttl
        assert otp_info['expiration_time'] - otp_info['creation_time'] == ttl

    @pytest.mark.parametrize("invalid_input", [
        (-1, False),
        ('invalid', False),
        (None, 'invalid')
    ])
    def test_invalid_input_handling(self, invalid_input):
        with pytest.raises(ValueError):
            OTPGenerator(*invalid_input)

    def test_metadata_integrity(self):
        otp_gen = OTPGenerator()
        otp_info = otp_gen.otp_dict['otp_info']
        meta = otp_gen.otp_dict['meta']

        assert 'creation_time' in otp_info
        assert 'id' in meta
        assert isinstance(otp_info['creation_time'], float)
        assert isinstance(meta['id'], str)