from pathlib import Path

from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from typer import Argument, Context, Exit, Option, Typer, echo

from expert_infero import __app_name__, __version__
from expert_infero.parser import Parser
from expert_infero.solvers import backward_chaining

console = Console()
app = Typer()


def version_func(flag):
    if flag:
        print(f"{__app_name__} v{__version__}")
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context, version: bool = Option(False, callback=version_func, is_flag=True)
):
    message = """Forma de uso: [b]expert_infero [SUBCOMANDO] [ARGUMENTOS][/]

 Existem 3 subcomandos disponíveis para essa aplicação

- [b]compile[/]: Compila um arquivo .efo, fornecendo a solução da derivação
- [b]tokenize[/]: Fornece os tokens presentes no arquivo
- [b]ast[/]: Fornece a árvore sintática do arquivo

[b]Exemplo de uso:[/]

expert_infero compile examples/example.efo

[b]Para mais informações rápidas: [red]infero --help[/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(Padding(message, pad=(0, 0, 0, 2)))
