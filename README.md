# Expert Infero

Expert Infero é uma ferramenta de geração de sistemas especialistas, projetada para facilitar a criação e gerenciamento de inferências. Utilizando uma linguagem específica em arquivos .efo, o Expert Infero organiza seu conhecimento em quatro seções principais:

- **Declarações:** Onde símbolos são associados a descrições detalhadas, formando a base do conhecimento.
- **Regras:** Estrutura que permite construir regras de inferência complexas utilizando os símbolos previamente declarados.
- **Fatos:** Seção dedicada a armazenar símbolos previamente determinados dentro do sistema.
- **Query:** Onde são especificados os objetivos ou questões que o sistema especialista deve resolver.

O Expert Infero utiliza encadeamento para frente e para trás. Além disso, conta com um módulo de explanação interativo, que questiona a veracidade de símbolos durante o processo de inferência, oferecendo explicações detalhadas sobre como o algoritmo chegou à solução final. Inspirado no funcionamento do Expert Sinta.

## Instalação

- Certifique-se de que tem o [Poetry](https://python-poetry.org/docs/) instalado
- Clone o repositório: `git clone https://github.com/ThiagoORuby/expert-infero.git`
- Entre na pasta: `cd expert-infero`
- Rode os comandos do poetry: `poetry install` e `poetry shell`

## Como Usar ?

### Compilação

```bash
python -m expert-infero compile arquivo.efo
```

#### Análise de Risco

```
python -m expert-infero compile examples/risco.efo
```

```
============================
ANALISE DE RISCO DE CRÉDITO
============================


Garantia Adequada é verdade? (S/N) N
Nenhuma Garantia é verdade? (S/N) S
Renda > 35k é verdade? (S/N) N
15k < Renda <= 35k é verdade? (S/N) S
Dívida Baixa é verdade? (S/N) N
Divida Alta é verdade? (S/N) S

  ==+==+==+== SOLUTION ==+==+==+==
  Risco Moderado é verdade se Nenhuma Garantia E 15k < Renda <= 35k E Divida Alta
  Nenhuma Garantia é verdade!
  15k < Renda <= 35k é verdade!
  Divida Alta é verdade!
  Então Risco Moderado é verdade!
```

#### Mini Akinator

```
python -m expert-infero compile examples/akinator.efo
```

```
====================
   MINI AKINATOR
====================
Descobrirei qual classe de animal você está pensando!


Produz leite é verdade? (S/N) N
Possui penas é verdade? (S/N) N
Possui nadadeiras é verdade? (S/N) N
Possui Coluna Vertebral é verdade? (S/N) S
É aquático é verdade? (S/N) N
Consegue voar é verdade? (S/N) S


  ==+==+==+== SOLUTION ==+==+==+==

  Inseto é verdade se NÃO Produz leite E NÃO Possui penas E NÃO Possui nadadeiras E NÃO Possui Coluna Vertebral E Consegue voar
  NÃO Possui Coluna Vertebral é verdade!
  Consegue voar é verdade!
  Então Inseto é verdade!
```

## BNF da linguagem

```
<program> ::= <init_section> <decl_section> <rules_section> <facts_section> <query_section>

<init_section> ::= "init_section:" <echos> "end" | empty
<decl_section> ::= "declarations:" <decls> "end"
<rules_section> ::= "rules:" <stmts> "end"
<facts_section> ::= "facts:" <stmts> "end" | empty
<query_section> ::= "query:" <stmts> "end"

<echos> ::= <echo> <echos>
<echo> ::= echo "'a-zA-Z'"

<decls> ::= <decl> <decls>
<decl> ::= <symbol> ":=" "'a-zA-z'"

<stmts> ::= <stmt> <stmts>
<stmt> ::= <expr>
<expr> ::= <term> <imp>
<imp> ::= "->" <term> | empty
<term> ::= <fact> <binary_op>
<binary_op> ::= "&" <fact> | "|" <fact> | empty
<fact> ::= "(" <expr> ")" | "~" <fact> | <symbol>
<symbol> ::= "a-zA-z0-9"
```
