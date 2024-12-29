class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.tables = {}

    def parse(self):
        while self.position < len(self.tokens):
            self._parse_table()
        return self.tables

    def _parse_table(self):
        self._expect("CREATE")
        self._expect("TABLE")
        table_name = self._peek()
        self._expect("IDENTIFICADOR")
        self._expect("(")
        columns = self._parse_columns()
        self._expect(")")
        self._expect(";")
        self.tables[table_name] = columns

    def _parse_columns(self):
        columns = [self._parse_column()]
        while self._peek() == ",":
            self._expect(",")
            columns.append(self._parse_column())
        return columns

    def _parse_column(self):
        column_name = self._peek()
        self._expect("IDENTIFICADOR")
        column_type = self._peek()
        self._expect(["INT", "VARCHAR", "BOOLEAN", "DECIMAL", "DATE"])
        restriction = None
        if self._peek() in ["PRIMARY", "FOREIGN"]:
            restriction = self._parse_restriction()
        return {"name": column_name, "type": column_type, "restriction": restriction}

    def _parse_restriction(self):
        restriction = self._peek()
        self._expect(["PRIMARY", "FOREIGN"])
        self._expect("KEY")
        if restriction == "FOREIGN":
            self._expect("IDENTIFICADOR")  # Nombre de la tabla referenciada
        return restriction

    def _expect(self, expected):
        current_token = self._peek()
        if isinstance(expected, list):
            if current_token in expected:
                self.position += 1
            else:
                raise Exception(f"Error sintáctico: Se esperaba uno de '{' | '.join(expected)}', pero se encontró '{current_token}'.")
        elif current_token == expected:
            self.position += 1
        else:
            raise Exception(f"Error sintáctico: Se esperaba '{expected}', pero se encontró '{current_token}'.")

    def _peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None
