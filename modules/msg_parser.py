def get_messages(text: str):
    result = dict()
    current_key = None
    for no, line in enumerate(text.split("\n")):
        line = line.strip()
        # Если строка является комментарием
        if line.startswith('#'):
            continue

        is_key = line.startswith(':')

        if not current_key:
            if not line:
                continue
            if not is_key:
                raise ValueError('File must start with key name. Line {}'.format(no))

        if is_key:
            current_key = line[1:]
            result[current_key] = ''
            continue

        result[current_key] = (result[current_key] + '\n' + line).strip()

    return result
