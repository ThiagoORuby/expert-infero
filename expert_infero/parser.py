from expert_infero.lexer import Lexer
from expert_infero.tokens import Token
from expert_infero.sentences import Sentence, Symbol, Not, And, Or, Implication


class Parser:
    def __init__(self, data: str):
        self.scanner: Lexer = Lexer(data)
        self.lookahead: Token = self.scanner.scan()
        self.symtable: dict[str, Sentence] = {}
        self.symhash: dict[str, bool | None] = {}
        self.declarations: dict[str, str] = {}
        self.program: dict[str, list] = {
            "echos": [],
            "rules": [],
            "facts": [],
            "query": [],
        }

    def start(self):
        self.init_section()
        self.decl_section()
        self.rules_section()
        self.facts_section()
        self.query_section()

    def match(self, value: str):
        if self.lookahead.value == value:
            self.lookahead = self.scanner.scan()
            return True
        return False

    def init_section(self):
        """
        <init_section> ::= "init_section:" <echos> "end" | empty
        """
        if not self.match("init:"):
            if self.match("end"):
                raise SyntaxError(f"L{self.scanner.line}, 'end' sozinho")
        else:
            self.echos()

    def echos(self):
        """
        <echos> ::= <echo> <echos>
        <echo> ::= echo "'a-zA-Z'"
        """
        while not self.match("end"):
            self.match("echo")
            if self.lookahead.tag != "STRING":
                raise SyntaxError(f"L{self.scanner.line}, string esperada")
            self.program["echos"].append(self.lookahead.value)
            self.lookahead = self.scanner.scan()

    def decl_section(self):
        """
        <decl_section> ::= "declarations:" <decls> "end"
        """
        if not self.match("declarations:"):
            raise SyntaxError(f"L{self.scanner.line}, 'declarations:' esperado")
        self.decls()

    def decls(self):
        """
        <decls> ::= <decl> <decls>
        <decl> ::= <symbol> ":=" "'a-zA-z'"
        """
        while not self.match("end"):
            if self.lookahead.tag != "SYMBOL":
                raise SyntaxError(f"L{self.scanner.line}, simbolo esperado")
            symbol = self.lookahead.value
            if self.declarations.get(symbol):
                raise SyntaxError(
                    f"L{self.scanner.line}, simbolo já foi declarado anteriormente"
                )
            self.lookahead = self.scanner.scan()
            self.match(":=")
            if self.lookahead.tag != "STRING":
                raise SyntaxError(f"L{self.scanner.line}, string esperada")
            string = self.lookahead.value
            self.declarations[symbol] = string
            self.lookahead = self.scanner.scan()

    def rules_section(self):
        """
        <rules_section> ::= "rules:" <stmts> "end"
        """
        if not self.match("rules:"):
            raise SyntaxError(f"L{self.scanner.line}, 'rules:' esperado")
        self.stmts("rules")

    def facts_section(self):
        """
        <facts_section> ::= "facts:" <stmts> "end"
        """
        if not self.match("facts:"):
            raise SyntaxError(f"L{self.scanner.line}, 'facts:' esperado")
        self.stmts("facts")

    def query_section(self):
        """
        <query_section> ::= "query:" <stmts> "end"
        """
        if not self.match("query:"):
            raise SyntaxError(f"L{self.scanner.line}, 'query:' esperado")
        self.stmts("query")

    def stmts(self, kind: str):
        """
        <stmts> ::= <stmt> <stmts>
        <stmt> ::= <expr>
        """
        stmts_list: list = self.program[kind]
        while not self.match("end"):
            expr = self.expr()
            stmts_list.append(expr)

    def expr(self):
        """
        <expr> ::= <term> <imp>
        <imp> ::= "->" <term> | empty
        """
        left = self.term()
        if self.lookahead.value == "->":
            self.match("->")
            right = self.term()
            return Implication(left, right)
        else:
            return left

    def term(self):
        """
        <term> ::= <fact> <binary_op>
        <binary_op> ::= "&" <fact> | "|" <fact> | empty
        """
        left = self.fact()
        while True:
            if self.lookahead.value == "&":
                self.match("&")
                right = self.fact()
                if isinstance(left, And):
                    left.add(right)
                else:
                    left = And(left, right)
            elif self.lookahead.value == "|":
                self.match("|")
                right = self.fact()
                if isinstance(left, Or):
                    left.add(right)
                left = Or(left, right)
            else:
                break
        return left

    def fact(self):
        """
        <fact> ::= "(" <expr> ")" | "~" <fact> | <symbol>
        <symbol> ::= a-zA-Z
        """
        if self.lookahead.value == "(":
            self.match("(")
            expr = self.expr()
            if not self.match(")"):
                raise SyntaxError(f"L{self.scanner.line}, ')' esperado")
            return expr
        else:
            if self.lookahead.value == "~":
                self.match("~")
                operand = self.fact()
                return Not(operand)
            if self.lookahead.tag != "SYMBOL":
                raise SyntaxError(f"L{self.scanner.line}, simbolo esperado")
            symbol: str = self.lookahead.value
            if symbol not in self.declarations.keys():
                raise SyntaxError(
                    f"L{self.scanner.line}, simbolo {symbol} nao encontrado nas declarações"
                )
            finded = self.symtable.get(symbol)
            self.lookahead = self.scanner.scan()
            if finded:
                return finded

            self.symtable[symbol] = Symbol(symbol)
            self.symhash[symbol] = None
            return self.symtable[symbol]
