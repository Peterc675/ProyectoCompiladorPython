class SemanticAnalyzer:
    def __init__(self, tables):
        self.tables = tables
        self.symbol_table = []

    def analyze(self):
        for table_name, columns in self.tables.items():
            self._check_primary_keys(table_name, columns)
            self._check_foreign_keys(table_name, columns)
        self._generate_symbol_table()

    def _check_primary_keys(self, table_name, columns):
        primary_keys = [col for col in columns if col.get("restriction") == "PRIMARY KEY"]
        if len(primary_keys) > 1:
            raise Exception(f"Error semántico: La tabla '{table_name}' tiene múltiples claves primarias.")
        if not primary_keys:
            print(f"Advertencia: La tabla '{table_name}' no tiene clave primaria.")

    def _check_foreign_keys(self, table_name, columns):
        for col in columns:
            if col.get("restriction") == "FOREIGN KEY":
                ref_table, ref_column = col["reference"].split(".")
                if ref_table not in self.tables:
                    raise Exception(f"Error semántico: La tabla referenciada '{ref_table}' no existe.")
                if ref_column not in [c["name"] for c in self.tables[ref_table]]:
                    raise Exception(f"Error semántico: La columna referenciada '{ref_column}' no existe en la tabla '{ref_table}'.")

    def _generate_symbol_table(self):
        for table_name, columns in self.tables.items():
            for col in columns:
                self.symbol_table.append({
                    "Tabla": table_name,
                    "Columna": col["name"],
                    "Tipo": col["type"],
                    "Restricción": col.get("restriction", "-"),
                    "Referencia": col.get("reference", "-")
                })

    def get_symbol_table(self):
        return self.symbol_table
