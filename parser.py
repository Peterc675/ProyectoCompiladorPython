class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.generated_code = ""  # Aquí se almacenará el código generado

    def parse(self):
        while self.position < len(self.tokens):
            self._parse_table()
        return self.generated_code  # Devuelve el código generado

    def _parse_table(self):
        self._match("CREATE")
        self._match("TABLE")
        table_name = self._peek()
        self._match("IDENTIFICADOR")
        self._match("(")
        columns = self._parse_columns()
        self._match(")")
        self._match(";")

        # esto código para la tabla como una clase en Python
        self._generate_class(table_name, columns)

    def _parse_columns(self):
        columns = [self._parse_column()]
        while self._peek() == ",":
            self._match(",")
            columns.append(self._parse_column())
        return columns

    def _parse_column(self):
        column_name = self._peek()
        self._match("IDENTIFICADOR")
        column_type = self._peek()
        self._match("INT|VARCHAR|BOOLEAN")
        if self._peek() in ["PRIMARY", "FOREIGN"]:
            self._parse_restriction()
        return column_name, column_type

    def _parse_restriction(self):
        self._match("PRIMARY|FOREIGN")
        self._match("KEY")

    def _match(self, expected):
        """
        Verifica si el token actual coincide con el patrón esperado.
        Si no coincide, lanza una excepción detallada del error sintáctico.
        """
        import re

        # Validación para asegurar que `expected` no sea vacío
        if not expected:
            raise Exception("Error interno: patrón vacío en _match().")

        
        pattern = re.escape(expected) if "|" not in expected else expected

        # Comparar el token actual con el patrón esperado
        if self._peek() and re.match(f"^{pattern}$", self._peek()):
            self.position += 1  
        else:
            raise Exception(f"Error sintáctico: Se esperaba '{expected}', pero se encontró '{self._peek()}'.")

    def _peek(self):
        """
        Devuelve el token actual o `None` si no hay más tokens.
        """
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _generate_class(self, table_name, columns):
        """
        Genera una clase en Python para la tabla SQL.
        """
        class_code = f"class {table_name.capitalize()}:\n"
        class_code += "    def __init__(self, " + ", ".join([f"{name}: {self._map_type(typ)}" for name, typ in columns]) + "):\n"
        for name, typ in columns:
            class_code += f"        self.{name} = {name}\n"
        class_code += "\n"

        # Depuración: imprimir la clase generada en la consola
        print(f"Clase generada para {table_name}:\n{class_code}")

        self.generated_code += class_code

    def _map_type(self, sql_type):
        """
        Mapea los tipos de datos SQL a tipos de datos en Python.
        """
        mapping = {
            "INT": "int",
            "VARCHAR": "str",
            "BOOLEAN": "bool"
        }
        return mapping.get(sql_type, "str")
