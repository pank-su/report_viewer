import unittest

from phone_check import validate_phone_number


class TestPhoneNumberValidation(unittest.TestCase):
    def test_valid_phone_numbers(self):
        valid_numbers = [
            "+7 962 7011087",
            "+7 999 1234567",
            "+7 123 4567890"
        ]
        for number in valid_numbers:
            self.assertTrue(validate_phone_number(number))

    def test_invalid_phone_numbers(self):
        invalid_numbers = [
            "+7",
            "+7 12345678",
            "+7 999 12345678",
            "ABC 123 DEF4567",
            "1234567890"
        ]
        for number in invalid_numbers:
            self.assertFalse(validate_phone_number(number))


if __name__ == "__main__":
    unittest.main()
