# Markdown_V2 format functions

def quot(text: str, nested:bool = False) -> str:
    return '\n'.join([f">{escape_special(line, nested)}" for line in text.split('\n')])


def bold(text: str, nested:bool = False) -> str:
    return f"*{escape_special(text, nested)}*"


def italic(text: str, nested:bool = False) -> str:
    return f"_{escape_special(text, nested)}_"


def underline(text: str, nested:bool = False) -> str:
    return f"__{escape_special(text, nested)}__"


def underline_italic(text: str, nested:bool = False) -> str:
    return f"___{escape_special(text, nested)}_\r__"


def spoiler(text: str, nested:bool = False) -> str:
    return f"||{escape_special(text, nested)}||"


def strikethrough(text: str, nested:bool = False) -> str:
    return f"~{escape_special(text, nested)}~"


def inline_url(text: str, url: str, nested:bool = False) -> str:
    e_text, e_url = escape_special(text), escape_special(url)
    return f"[{escape_special(text, nested)}]({url})"


def inline_mention(text: str, user_id: int, nested:bool = False) -> str:
    return f"[{escape_special(text, nested)}](tg://user?id={user_id})"


def inline_code(text: str, nested:bool = False) -> str:
    return f"`{escape_special(text,nested)}`"


def pre_formatted_code(text: str, nested:bool = False) -> str:
    return f"```\n{escape_special(text,nested)}```"


def pre_formatted_spec_language_code(language: str, text: str, nested:bool = False) -> str:
    # for supported languages
    # https://github.com/TelegramMessenger/libprisma#supported-languages
    return f"```{language}\n{escape_special(text, nested)}```"


def escape_special(input_string: str, nested:bool = False) -> str:
    special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!',
                          "\\"]
    return ''.join(['\\' + char if char in special_characters and not nested else char for char in input_string])
