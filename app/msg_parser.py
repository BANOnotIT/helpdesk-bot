def get_messages(text: str):
    result = dict()
    current_key = None
    for line in text.split("\n"):

        # Если строка является комментарием
        if line.startswith('#'):
            continue

        is_key = line.startswith(':')

        if not current_key:
            if not line:
                continue
            if not is_key:
                raise ValueError('File must start with key name')

        if is_key:
            if result.get(current_key):
                result[current_key] = result[current_key].strip()

            current_key = line[1:]
            result[current_key] = ''
            continue

        result[current_key] += '\n' + line

    return result
