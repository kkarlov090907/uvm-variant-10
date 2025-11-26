from textual import on
from uvm_asm import full_asm
from uvm_interp import execute
from textual.app import App, ComposeResult
from textual.widgets import Button, TextArea
import json

# Пример программы
EXAMPLE_PROGRAM = """load_const;0
load_const;100
write_value;0
load_const;1
load_const;50
write_value;0
load_const;2
load_const;25
write_value;0"""


class UVMApp(App):
    CSS = """
    Screen { 
        align: center middle; 
        background: #1e1e1e;
    }
    TextArea {
        width: 90%;
        height: 40%;
        margin: 1;
    }
    Button {
        width: 30;
        margin: 1;
    }
    #output {
        height: 30%;
    }
    """

    def compose(self) -> ComposeResult:
        yield TextArea(text=EXAMPLE_PROGRAM, id="input", language="text")
        yield Button(label="Ассемблировать и выполнить", id="main", variant="primary")
        yield TextArea(id="output", text="Результат появится здесь...", language="text")

    @on(Button.Pressed, "#main")
    def execute_program(self) -> None:
        try:
            program = self.query_one("#input").text
            bytecode, ir = full_asm(program)
            stack, memory = execute(bytecode)

            # Форматируем вывод
            memory_str = " ".join([f"[{i}]={memory[i]}" for i in range(10)])

            result = f"""Выполнено команд: {len(ir)}

Стек: {stack}
Память: {memory_str}

Байткод: {len(bytecode)} байт"""

            self.query_one("#output").text = result
        except Exception as e:
            self.query_one("#output").text = f"Ошибка: {str(e)}"


if __name__ == "__main__":
    app = UVMApp()
    app.run()