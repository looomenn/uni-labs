""" Localised strings """

import json


def load_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


TRANSLATIONS = load_translations('locales.json')


def translate(
    language: str,
    module: str,
    phrase: str,
    status: str = 'general',
    use_prefixes: bool = True,
    **kwargs
):
    module_prefixes: dict = {
        'ukr': {
            'menu': '[Меню]',
            'queues': '[Черги]',
            'equations': '[Рівняння]',
            'system': '[Система]',
        },
        'eng': {
            'menu': '[Menu]',
            'queues': '[Queues]',
            'equations': '[Equations]',
            'system': '[System]',
        }
    }

    status_prefix: dict = {
        'general': '[*]',
        'input': '[?]',
        'add': '[+]',
        'delete': '[-]',
        'error': '[!]',
        'success': '[✔]',
        'debug': '[&]',
    }

    try:
        translated = TRANSLATIONS[language][module][phrase]

        if use_prefixes:
            phrase = f'{module_prefixes[language][module]}{status_prefix[status]} {translated}'
        else:
            phrase = translated

        phrase = phrase.format(**kwargs) if kwargs else phrase

        return phrase

    except KeyError as err:
        return (f"{module_prefixes[language]['system']}"
                f"{status_prefix['error']} "
                f"{TRANSLATIONS[language]['system']['no_translation']}"
                f"(key error: {err})")
