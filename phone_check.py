from re import fullmatch


def validate_phone_number(phone_number):
    """Функция для проверки телефонного номера в формате "+X XXX XXXXXXX" """
    return fullmatch(r"\+\d{1,2}\s\d{3}\s\d{7}", phone_number) is not None
