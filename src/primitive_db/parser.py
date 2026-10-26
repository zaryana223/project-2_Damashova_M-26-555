import shlex


def convert_value(text):
    if text == "true":
        return True
    if text == "false":
        return False
    if text.isdigit():
        return int(text)
    return text


def parse_where(text):
    parts = shlex.split(text)
    key = parts[0]
    value = convert_value(parts[2])
    return {key: value}


def parse_set(text):
    parts = shlex.split(text)
    key = parts[0]
    value = convert_value(parts[2])
    return {key: value}


def parse_values(text):
    start = text.find("(")
    end = text.rfind(")")
    if start == -1 or end == -1 or end < start:
        return None
    inside = text[start + 1:end]
    chunks = inside.split(",")
    values = []
    for chunk in chunks:
        chunk = chunk.strip()
        if chunk.startswith('"') and chunk.endswith('"'):
            values.append(chunk[1:-1])
        elif chunk == "true":
            values.append(True)
        elif chunk == "false":
            values.append(False)
        else:
            if not chunk.isdigit():
                return None
            values.append(int(chunk))
    return values