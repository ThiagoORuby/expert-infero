from expert_infero.sentences import And, Implication, Not, Or, Sentence, Symbol


def backward_chaining(
    rules: list[Implication],
    queries: list[Sentence],
    symtable: dict[str, bool | None],
    desc: dict[str, str],
):
    explanation: list[str] = []

    def ask(question: Sentence):
        if isinstance(question, Symbol):
            if symtable[question.name] is False:
                return False
        elif isinstance(question, Not):
            if isinstance(question.operand, Symbol):
                if symtable[question.operand.name] is False:
                    return True
                question = question.operand  # faz a pergunta em relacao ao simbolo
            else:
                return question.evaluate(symtable)
        else:
            return question.evaluate(symtable)
        ans = None
        while ans not in ("S", "N"):
            ans = input(f"{question.describe(desc)} é verdade? (S/N) ")[0].upper()
            if ans == "S":
                symtable[question.name] = True
                explanation.append(f"{question.describe(desc)} é verdade!")
                break
            elif ans == "N":
                symtable[question.name] = False
                break
            else:
                print("Por favor, responda com S ou N")
        return symtable[question.name]

    def solve(query):
        if isinstance(query, Symbol):
            value = query.evaluate(symtable)
            if value is True:
                explanation.append(f"{query.describe(desc)} é verdade!")
                return True
        elif isinstance(query, Not):
            if isinstance(query.operand, Not):
                # if Not(Not(something)), verifico se something é verdade
                return solve(query.operand.operand)
            elif isinstance(query.operand, Symbol):
                value = query.evaluate(symtable)
                if value is False:
                    explanation.append(f"{query.describe(desc)} é verdade!")
                    return True
            else:
                demorgan = Sentence.apply_demorgan(query)
                return solve(demorgan)
        elif isinstance(query, And):
            if all(solve(conjunct) or ask(conjunct) for conjunct in query.conjuncts):
                return True
        elif isinstance(query, Or):
            if any(solve(disjunct) or ask(disjunct) for disjunct in query.disjuncts):
                return True
        for rule in rules:
            if rule.consequent == query:
                explanation.append(
                    f"{rule.consequent.describe(desc)} é verdade se {rule.antecedent.describe(desc)}"
                )
                if solve(rule.antecedent) or ask(rule.antecedent):
                    # TODO: função pra validar o consequente (pode ser uma expr composta)
                    explanation.append(f"Então {query.describe(desc)} é verdade!")
                    if isinstance(query, Symbol):
                        symtable[query.name] = True
                    return True
                explanation.clear()

        return False

    for query in queries:
        ret = solve(query)
        if ret:
            return explanation, ret
        else:
            explanation.clear()

    explanation.append("Não foi possível chegar a uma conclusão :(")
    return explanation, False
