"""
(c) Adhish Thite

This module, generator.py, contains the OTPGenerator class for generating One-Time Passwords (OTPs).

The OTPGenerator class offers functionalities to create customizable OTPs which can be numeric or alphanumeric,
with a specified length and time-to-live (TTL).
The generated OTPs come along with metadata and information about their creation and expiration.
"""

import secrets
import string
import uuid
import time


class OTPGenerator:
    """
    A class for generating One-Time Passwords (OTPs).

    This class allows the generation of OTPs which can be numeric or alphanumeric, with a specified length and TTL.
    It also provides information about the generated OTP, such as creation time, expiration time, and TTL.
    Additionally, it generates a unique meta identifier for each OTP.

    Attributes:
        __length (int): The length of the OTP. Default is 6 characters.
        __alphanumeric (bool): A flag to determine if the OTP should be alphanumeric. Defaults to False (numeric only).
        __kwargs (dict): Additional keyword arguments.
        __meta (dict): Metadata associated with the OTP. Defaults to an empty dictionary.
        __ttl (int): Time-to-live in seconds for the OTP. Defaults to 3600 seconds (1 hour).
        __otp (str, None): The generated OTP. None until an OTP is generated.
        __otp_info (dict, None): Information about the generated OTP. None until an OTP is generated.

    Methods:
        generate_otp(): Generates a random OTP based on the specified length and alphanumeric flag.
        generate_meta(): Generates a random meta identifier for the OTP.
        get_otp(): Returns the generated OTP along with its information and metadata.

    Example:
        >>> otp_gen = OTPGenerator(length=4, alphanumeric=True)
        >>> otp_info = otp_gen.get_otp()
        >>> print(otp_info)
    """

    def __init__(
        self,
        meta: dict = None,
        length: int = 6,
        alphanumeric: bool = False,
        ttl: int = 3600,
        generate: bool = True,
        **kwargs
    ):

        """
        Constructs all the necessary attributes for the OTPGenerator object.

        Parameters:
            meta (dict): Metadata associated with the OTP. Defaults to None, which initializes to an empty dictionary.
            length (int): The length of the OTP. Default is 6 characters.
            alphanumeric (bool): A flag to determine if the OTP should be alphanumeric. Defaults to False (numeric only).
            ttl (int): Time-to-live in seconds for the OTP. Defaults to 3600 seconds (1 hour).
            generate (bool): A flag to determine if an OTP should be generated upon instantiation. Defaults to True.
            **kwargs: Additional keyword arguments.
        """
        # Validate length
        if not isinstance(length, int) or length <= 0:
            raise ValueError("Length must be a positive integer.")

        # Validate alphanumeric
        if not isinstance(alphanumeric, bool):
            raise ValueError("Alphanumeric must be a boolean value.")

        # Validate TTL
        if not isinstance(ttl, int) or ttl < 0 or ttl > 86400:  # 86400 seconds = 24 hours
            raise ValueError("TTL must be a non-negative integer, up to 86400 (24 hours).")

        # Validate meta (optional)
        if meta is not None and not isinstance(meta, dict):
            raise ValueError("Meta must be a dictionary.")

        self.__length = length
        self.__alphanumeric = alphanumeric
        self.__kwargs = kwargs
        self.__meta = meta or {}
        self.__ttl = ttl
        self.__otp = None
        self.__otp_info = None
        self.otp_dict = None

        # Generate OTP and meta
        if generate:
            self.otp_dict = self.get_otp()

    def generate_otp(self) -> None:
        """
        Generate a random OTP.

        This method creates a random OTP based on the specified length and alphanumeric flag.
        It also records the creation time, expiration time, and TTL of the OTP.

        Returns:
            None: This method updates the class attributes __otp and __otp_info in place.
        """

        if self.__alphanumeric:
            alphabet = string.ascii_letters + string.digits
        else:
            alphabet = string.digits

        self.__otp = "".join(secrets.choice(alphabet) for _ in range(self.__length))

        creation_time = time.time()
        expiration_time = creation_time + self.__ttl

        self.__otp_info = {
            "length": self.__length,
            "alphanumeric": self.__alphanumeric,
            "creation_time": creation_time,
            "expiration_time": expiration_time,
            "ttl": self.__ttl,
        }

    def generate_meta(self) -> None:
        """
        Generate a random meta identifier for the OTP.

        This method creates a unique meta identifier using UUID (Universally Unique Identifier).

        Returns:
            None: This method updates the class attribute __meta in place.
        """

        self.__meta = {
            "id": str(uuid.uuid4()),
        }

    def get_otp(self) -> dict:
        """
        Get the generated OTP along with its information and metadata.

        This method returns the OTP, its information (such as creation and expiration time, TTL),
        and its metadata (including a unique identifier).

        Returns:
            dict: A dictionary containing the OTP, OTP information, and metadata.
        """
        self.generate_otp()

        if not self.__meta:
            self.generate_meta()

        return {"otp": self.__otp, "otp_info": self.__otp_info, "meta": self.__meta}
