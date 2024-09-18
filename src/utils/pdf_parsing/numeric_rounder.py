def round_to_half(number):
    try:
        number = float(number)
    except ValueError:
        return None

    integer_part = int(number)
    decimal_part = number - integer_part

    if decimal_part < 0.25:
        result = integer_part
    elif 0.25 <= decimal_part < 0.75:
        result = integer_part + 0.5
    else:
        result = integer_part + 1

    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)