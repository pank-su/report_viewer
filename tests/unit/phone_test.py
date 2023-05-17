import unittest

from phone_check import validate_phone_number


class TestPhoneNumberValidation(unittest.TestCase):
    """Проверка паттерна на корректность его работы"""
    def test_valid_phone_numbers(self):
        """Проверка на корректных значениях"""
        valid_numbers = [
            "+7 963 7011087",
            "+9 999 2525252",
            "+1 123 4567890",
            "+11 123 4567890",
        ]
        for number in valid_numbers:
            self.assertTrue(validate_phone_number(number))

    def test_invalid_phone_numbers(self):
        """Проверка на некорректных значениях"""
        invalid_numbers = [
            "+7",
            "+8 12345678",
            "+6 999 12345678",
            "ABC 123 DEF4567",
            "1234567890",
            "++3 983 7011087",
            "+12 963 7011007 +7 963 7011087",
            "+5 963 701.1087",
            "+1  963  7011087",
            "+7-963-7011087",
            "+ 963 7011087",
            "+111 123 4567890",
            "+11 123 456789",
            "+1 1 1"
        ]
        for number in invalid_numbers:

            self.assertFalse(validate_phone_number(number))


if __name__ == "__main__":
    unittest.main()
