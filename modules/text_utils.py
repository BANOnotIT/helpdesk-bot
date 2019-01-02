def is_yes(text: str):
    if 'д' in text.lower():
        return True
    elif 'н' in text.lower():
        return False

    raise ValueError('It\'s neither yes nor no')
