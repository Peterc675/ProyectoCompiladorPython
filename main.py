import tkinter as tk
from tkinter import ttk, scrolledtext
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

def compilar_codigo():
    codigo_sql = text_input.get("1.0", tk.END).strip()
    try:
        # Analizador Léxico
        lexer = Lexer(codigo_sql)
        tokens = lexer.get_tokens()

        # Mostrar tokens
        tokens_display.config(state="normal")
        tokens_display.delete("1.0", tk.END)
        tokens_display.insert(tk.END, "\n".join(tokens))
        tokens_display.config(state="disabled")

        # Analizador Sintáctico
        parser = Parser(tokens)
        tables = parser.parse()

        # Analizador Semántico
        analyzer = SemanticAnalyzer(tables)
        analyzer.analyze()

        # Mostrar Tabla de Símbolos
        symbol_table = analyzer.get_symbol_table()
        symbol_display.config(state="normal")
        symbol_display.delete("1.0", tk.END)
        for entry in symbol_table:
            symbol_display.insert(tk.END, f"{entry}\n")
        symbol_display.config(state="disabled")

        # Generar Código Python
        code_output = ""
        for table_name, columns in tables.items():
            # Crear la clase
            code_output += f"class {table_name.capitalize()}:\n"
            # Constructor con columnas como parámetros
            code_output += "    def __init__(self, " + ", ".join([f"{col['name']}: {map_python_type(col['type'])}" for col in columns]) + "):\n"
            for col in columns:
                code_output += f"        self.{col['name']} = {col['name']}\n"
            code_output += "\n"

        # Mostrar el código generado
        code_display.config(state="normal")
        code_display.delete("1.0", tk.END)
        code_display.insert(tk.END, code_output)
        code_display.config(state="disabled")

        # Mostrar resultados del análisis
        resultado_display.config(state="normal")
        resultado_display.delete("1.0", tk.END)
        resultado_display.insert(tk.END, "Compilación completada sin errores.")
        resultado_display.config(state="disabled")
    except Exception as e:
        resultado_display.config(state="normal")
        resultado_display.delete("1.0", tk.END)
        resultado_display.insert(tk.END, f"Error: {str(e)}")
        resultado_display.config(state="disabled")

def map_python_type(sql_type):
    """
    Mapea los tipos de datos SQL a sus equivalentes en Python.
    """
    mapping = {
        "INT": "int",
        "VARCHAR": "str",
        "BOOLEAN": "bool",
        "DECIMAL": "float",
        "DATE": "str"
    }
    return mapping.get(sql_type, "str")

root = tk.Tk()
root.title("Compilador SQL - Funcional")

# Interfaz Gráfica
ttk.Label(root, text="Ingrese el código SQL:").pack(anchor="w")
text_input = scrolledtext.ScrolledText(root, height=10, width=70)
text_input.pack()

ttk.Button(root, text="Compilar Código", command=compilar_codigo).pack(pady=5)

ttk.Label(root, text="Tokens generados:").pack(anchor="w")
tokens_display = scrolledtext.ScrolledText(root, height=10, width=70, state="disabled")
tokens_display.pack()

ttk.Label(root, text="Resultados del análisis:").pack(anchor="w")
resultado_display = scrolledtext.ScrolledText(root, height=5, width=70, state="disabled")
resultado_display.pack()

ttk.Label(root, text="Tabla de símbolos:").pack(anchor="w")
symbol_display = scrolledtext.ScrolledText(root, height=10, width=70, state="disabled")
symbol_display.pack()

ttk.Label(root, text="Código generado en Python:").pack(anchor="w")
code_display = scrolledtext.ScrolledText(root, height=10, width=70, state="disabled")
code_display.pack()

root.mainloop()
