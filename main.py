import tkinter as tk
from lexer import Lexer
from parser import Parser

def analizar_codigo():
    codigo_sql = text_input.get("1.0", tk.END).strip()
    try:
        # Analizador Léxico
        lexer = Lexer(codigo_sql)
        tokens = lexer.get_tokens()

        # Mostrar tokens
        tokens_display.delete("1.0", tk.END)
        tokens_display.insert(tk.END, "\n".join(tokens))

        # Analizador Sintáctico
        parser = Parser(tokens)
        generated_code = parser.parse()  # Generar el código Python

        # Validación: mostrar en consola para depuración
        print("Código Generado:", generated_code)  # Verifica que no esté vacío

        # Mostrar resultados
        resultado_display.delete("1.0", tk.END)
        resultado_display.insert(tk.END, "Análisis sintáctico completado sin errores.")

        # Mostrar código generado
        code_display.delete("1.0", tk.END)
        if generated_code.strip():
            code_display.insert(tk.END, generated_code)
        else:
            code_display.insert(tk.END, "No se generó ningún código. Revisa el SQL ingresado.")
    except Exception as e:
        resultado_display.delete("1.0", tk.END)
        resultado_display.insert(tk.END, str(e))

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Compilador SQL - Análisis y Generación de Código")

# Entrada del código SQL
tk.Label(root, text="Ingrese el código SQL:").pack()
text_input = tk.Text(root, height=10, width=60)
text_input.pack()

# Botón de análisis
tk.Button(root, text="Analizar Código", command=analizar_codigo).pack()

# Área de tokens
tk.Label(root, text="Tokens generados:").pack()
tokens_display = tk.Text(root, height=10, width=60, state="normal")
tokens_display.pack()

# Resultados del análisis
tk.Label(root, text="Resultados del análisis:").pack()
resultado_display = tk.Text(root, height=5, width=60, state="normal")
resultado_display.pack()

# Código generado
tk.Label(root, text="Código generado:").pack()
code_display = tk.Text(root, height=10, width=60, state="normal")
code_display.pack()

# Ejecutar la interfaz
root.mainloop()
