from re import fullmatch


def validate_phone_number(phone_number):
    """Функция для проверки телефонного номера в формате "+7 999 9999999" """
    return bool(fullmatch(r"\+7\s\d{3}\s\d{7}", phone_number))
