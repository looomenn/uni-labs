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
) -> str:
    """
    Translates given phrase from given module and language
    :rtype: object
    """
    module_prefixes: dict = {
        'ukr': {
            'menu': '[Меню]',
            'queues': '[Черги]',
            'equations': '[Рівняння]',
            'system': '[Система]',
        },
        'eng': {
            'menu': '[Menu]',
            'queues': '[QEs]',
            'equations': '[EQs]',
            'system': '[SYS]',
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


def tprint(
        language: str,
        module: str,
        phrase: str,
        status: str = 'general',
        use_prefixes: bool = True,
        **kwargs: object
) -> None:
    """ translates and prints translated text
    :param language: language to translate
    :param module: phrase from which module to take
    :param phrase: code for phrase from locale file
    :param status: status prefix (see translate func for more details)
    :param use_prefixes: whether to use module and status prefixes
    :param kwargs: additional keyword arguments for dynamic strings
    :rtype: None
    """
    translated_text = translate(language, module, phrase, status, use_prefixes, **kwargs)
    print(translated_text)
