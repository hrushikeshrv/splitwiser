def get_group_code(pk: int) -> str:
    """
    Encodes the given PK into a base 26 string to generate
    a unique group code.
    :param pk: PK to encode
    :return: Base 26 string representation of the PK
    """
    result = []
    while pk > 0:
        pk -= 1
        result.append(chr(pk % 26 + ord('A')))
        pk //= 26
    return ''.join(reversed(result))