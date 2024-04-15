def sanitize_string(string):
    return string.strip().replace("\xa0", " ")


class ParsingError(Exception):
    pass
