class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0

    def get_tokens(self):
        tokens = []
        reserved_words = ["CREATE", "TABLE", "INT", "VARCHAR", "BOOLEAN", "PRIMARY", "KEY", "FOREIGN"]

        while self.position < len(self.input):
            current_char = self.input[self.position]

            if current_char.isspace():
                self.position += 1
            elif current_char.isalpha():
                word = self._read_word()
                if word in reserved_words:
                    tokens.append(word)
                else:
                    tokens.append("IDENTIFICADOR")  # Aquí eliminamos el formato con paréntesis
            elif current_char.isdigit():
                tokens.append(f"NÚMERO({self._read_number()})")
            elif current_char in "(),;":
                tokens.append(current_char)
                self.position += 1
            else:
                raise Exception(f"Error léxico: Carácter no reconocido '{current_char}' en posición {self.position}")
        
        return tokens

    def _read_word(self):
        start = self.position
        while self.position < len(self.input) and (self.input[self.position].isalnum() or self.input[self.position] == "_"):
            self.position += 1
        return self.input[start:self.position]

    def _read_number(self):
        start = self.position
        while self.position < len(self.input) and self.input[self.position].isdigit():
            self.position += 1
        return self.input[start:self.position]
