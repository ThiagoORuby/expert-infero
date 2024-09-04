class Sentence:
    def evaluate(self, model) -> bool | None:
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")

    def formula(self) -> str | None:
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self) -> set:
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def apply_demorgan(cls, sentence):
        if isinstance(sentence, And):
            return Or(*[Not(conjunct) for conjunct in sentence.conjuncts])
        elif isinstance(sentence, Or):
            return And(*[Not(disjunct) for disjunct in sentence.disjuncts])
        elif isinstance(sentence, Implication):
            return And(sentence.antecedent, Not(sentence.consequent))
        else:
            raise Exception("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s) -> str:
        """Parenthesizes an expression if not already parenthesized."""

        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if (
            not len(s)
            or s.isalpha()
            or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1]))
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            if model[self.name] is None:
                return None
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def describe(self, descriptions):
        return descriptions[self.name]

    def symbols(self):
        return {self.name}


class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        if self.operand.evaluate(model) is None:
            return None
        return not self.operand.evaluate(model)

    def formula(self):
        return "~" + Sentence.parenthesize(self.operand.formula())

    def describe(self, descriptions):
        return "NÃO " + self.operand.describe(descriptions)

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        if all(conjunct.evaluate(model) for conjunct in self.conjuncts):
            return True
        elif any(conjunct.evaluate(model) is False for conjunct in self.conjuncts):
            return False
        return None

    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " & ".join(
            [Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts]
        )

    def describe(self, descriptions):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].describe(descriptions)
        return " E ".join(
            [conjunct.describe(descriptions) for conjunct in self.conjuncts]
        )

    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def add(self, disjunct):
        Sentence.validate(disjunct)
        self.disjuncts.append(disjunct)

    def evaluate(self, model):
        if any(disjunct.evaluate(model) for disjunct in self.disjuncts):
            return True
        elif any(disjunct.evaluate(model) is None for disjunct in self.disjuncts):
            return None
        return False

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " | ".join(
            [Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts]
        )

    def describe(self, descriptions):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].describe(descriptions)
        return " OU ".join(
            [disjunct.describe(descriptions) for disjunct in self.disjuncts]
        )

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (
            isinstance(other, Implication)
            and self.antecedent == other.antecedent
            and self.consequent == other.consequent
        )

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} -> {consequent}"

    def describe(self, descriptions):
        antecedent = self.antecedent.describe(descriptions)
        consequent = self.consequent.describe(descriptions)
        return f"SE {antecedent} ENTÃO {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())
