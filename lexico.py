import re
from estruturas import Token, Simbolo

PALAVRAS_RESERVADAS = {
    "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "float", "for", "if",
    "int", "long", "return", "short", "static",
    "struct", "switch", "void", "while"
}

class AnalisadorLexico:
    def __init__(self):
        self.tokens = []
        self.tabela_simbolos = {}
        self.contador_simbolos = 1

    def analisar(self, codigo: str) -> bool:
        print("\n==========================================")
        print("1. ANÁLISE LÉXICA (LINGUAGEM C)")
        print("==========================================")

        linhas = codigo.splitlines()
        sem_erros = True

        especificacao_tokens = [
            ("DIRETIVA", r"#\s*(include|define)\b.*"),
            ("NUMERO",   r"\d+(?:\.\d+)?"),
            ("LITERAL",      r'(?:"[^"]*"|\'[^\']*\')'),
            ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("OP_ATRIB", r"="),
            ("OP_ARIT",  r"[+\-*/%]"),
            ("OP_END",   r"&"),
            ("DELIM",    r"[;(),{}\[\]]"),
            ("ESPACO",   r"[ \t]+"),
            ("ERRO",     r".")
        ]
        regex_geral = "|".join(f"(?P<{nome}>{padrao})" for nome, padrao in especificacao_tokens)

        for num_linha, texto_linha in enumerate(linhas, start=1):
            for match in re.finditer(regex_geral, texto_linha):
                grupo = match.lastgroup
                lexema = match.group()

                if grupo in ("ESPACO", "DIRETIVA"):
                    continue
                elif grupo == "ERRO":
                    print(f"[ERRO LÉXICO] Caractere inválido '{lexema}' na linha {num_linha}")
                    sem_erros = False
                elif grupo == "ID":
                    if lexema in PALAVRAS_RESERVADAS:
                        self.tokens.append(Token("PALAVRA_RESERVADA", lexema, num_linha))
                    else:
                        id_simbolo = self._registrar_simbolo(lexema, "Identificador", "Nao Definido")
                        self.tokens.append(Token("ID", lexema, num_linha, posicao_ts=id_simbolo))
                else:
                    self.tokens.append(Token(grupo, lexema, num_linha))

        print("\nLista de Tokens:")
        for token in self.tokens:
            print(token)

        return sem_erros

    def _registrar_simbolo(self, lexema: str, categoria: str, tipo_dado: str) -> int:
        if lexema not in self.tabela_simbolos:
            self.tabela_simbolos[lexema] = Simbolo(
                self.contador_simbolos, lexema, categoria, tipo_dado
            )
            self.contador_simbolos += 1
        return self.tabela_simbolos[lexema].id

    def exibir_tabela_simbolos(self):
        print("\nTABELA DE SÍMBOLOS")
        print(f"{'ID':<5} | {'SÍMBOLO':<15} | {'TIPO':<15}")
        print("-" * 40)
        for s in self.tabela_simbolos.values():
            id_formatado = f"#{s.id}"
            print(f"{id_formatado:<5} | {s.lexema:<15} | {s.tipo_dado:<15}")