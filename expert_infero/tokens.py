from dataclasses import dataclass

TOKENS = [
    ("INIT_SECTION", r"init:"),  # Identifica o inicio da seção de impressões
    ("DECLR_SECTION", r"declarations:"),  # Identifica o inicio da seção de declarações
    ("RULES_SECTION", r"rules:"),  # Identifica o início da seção de regras
    ("FACTS_SECTION", r"facts:"),  # Identifica o início da seção de fatos
    ("QUERY_SECTION", r"query:"),  # Identifica o início da seção de perguntas
    ("ENDSECTION", r"end"),  # Identifica o final de uma seção
    ("SYMBOL", r"[A-Za-z][A-Za-z0-9]*"),  # Variáveis: A, B, C...
    ("ASSIGN", r":="),  # Atribuição de descrição
    ("STRING", r'"([^"]*)"'),  # informação textual
    ("ECHO", "echo"),  # keyword para imprimir algo na tela
    ("AND", r"&"),  # Operador E
    ("OR", r"\|"),  # Operador OU
    ("IMPLIES", r"->"),  # Operador Implicação
    ("NOT", r"~"),  # Operador Negação
    ("LPAREN", r"\("),  # Parêntese esquerdo
    ("RPAREN", r"\)"),  # Parêntese direito
    ("NEWLINE", r"\n"),  # Nova linha (usada para separação de regras)
    ("WHITESPACE", r"\s+"),  # Espaços em branco
]


@dataclass
class Token:
    value: str
    tag: str

    def __repr__(self):
        return f"<{self.value}, {self.tag}>"
