from expert_infero.tokens import Token, TOKENS
import re


class Lexer:
    def __init__(self, data):
        self.data: str = data
        self.line: int = 1
        self.id_table: dict[str, Token] = {}

    def scan(self) -> Token:
        if not self.data:
            return Token("", "")

        for token_type, regex in TOKENS:
            match = re.match(regex, self.data)
            if match:
                if token_type == "STRING":
                    value = match.group(1)
                    self.data = self.data[(len(value) + 2) :]
                else:
                    value = match.group(0)
                    self.data = self.data[len(value) :]
                if token_type != "WHITESPACE":
                    if token_type == "NEWLINE":
                        self.line += 1
                        return self.scan()
                    if token_type == "SYMBOL":
                        finded = self.id_table.get(value)
                        if finded:
                            return finded
                        else:
                            self.id_table[value] = Token(value, token_type)
                            return self.id_table[value]
                    return Token(value, token_type)
                else:
                    return self.scan()
        else:
            raise SyntaxError(f"Unexpected char: {self.data[0]}")
