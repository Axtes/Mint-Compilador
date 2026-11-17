from estruturas import NoAST

TIPOS_C = ("int", "float", "double", "char")

class AnalisadorSintaticoSemantico:
    def __init__(self, tokens, tabela_simbolos):
        self.tokens = tokens
        self.tabela_simbolos = tabela_simbolos
        self.pos = 0
        self.variaveis_declaradas = set()
        self.arvores_geradas = []

    def analisar(self):
        print("\n==========================================")
        print("2. ANÁLISE SINTÁTICA (AST) E SEMÂNTICA")
        print("==========================================")

        while self.pos < len(self.tokens):
            atual = self.tokens[self.pos]

            if atual.tipo == "PALAVRA_RESERVADA" and atual.lexema in TIPOS_C:
                tipo_declarado = atual.lexema
                self.pos += 1

                if self.pos < len(self.tokens) and self.tokens[self.pos].tipo == "ID":
                    id_token = self.tokens[self.pos]
                    self.pos += 1

                    if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == "(":
                        self.tabela_simbolos[id_token.lexema].tipo_dado = f"funcao_{tipo_declarado}"
                        while self.pos < len(self.tokens) and self.tokens[self.pos].lexema != "{":
                            self.pos += 1
                        if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == "{":
                            self.pos += 1
                        continue

                    self.tabela_simbolos[id_token.lexema].tipo_dado = tipo_declarado
                    self.variaveis_declaradas.add(id_token.lexema)

                    no_decl = NoAST(f"Decl ({tipo_declarado})")
                    no_decl.adicionar_filho(NoAST(id_token.lexema, eh_operador=False))

                    if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == "=":
                        self.pos += 1
                        no_atrib = NoAST("=", eh_operador=True)
                        no_atrib.adicionar_filho(NoAST(id_token.lexema, eh_operador=False))
                        expr = self._parse_E(tipo_declarado, id_token.linha)
                        if expr:
                            no_atrib.adicionar_filho(expr)
                        no_raiz = no_atrib
                    else:
                        no_raiz = no_decl

                    if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == ";":
                        self.pos += 1
                        self.arvores_geradas.append(no_raiz)
                        print("\n[AST Gerada]:")
                        no_raiz.imprimir()
                    else:
                        print(f"[ERRO SINTÁTICO] Esperado ';' na linha {id_token.linha}")
                        while self.pos < len(self.tokens) and self.tokens[self.pos].lexema != ";":
                            self.pos += 1
                        if self.pos < len(self.tokens):
                            self.pos += 1

            elif atual.tipo == "ID":
                id_destino = atual
                self.pos += 1

                # Se vier '(', é chamada de função (ex: printf(...);)
                if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == "(":
                    while self.pos < len(self.tokens) and self.tokens[self.pos].lexema != ";":
                        self.pos += 1
                    if self.pos < len(self.tokens):
                        self.pos += 1
                    continue

                if id_destino.lexema not in self.variaveis_declaradas:
                    print(f"\n[ERRO SEMÂNTICO] Variável '{id_destino.lexema}' utilizada na linha {id_destino.linha} não foi declarada previamente.")

                tipo_esperado = self.tabela_simbolos[id_destino.lexema].tipo_dado

                if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == "=":
                    self.pos += 1
                    no_atrib = NoAST("=", eh_operador=True)
                    no_atrib.adicionar_filho(NoAST(id_destino.lexema, eh_operador=False))

                    expr = self._parse_E(tipo_esperado, id_destino.linha)
                    if expr:
                        no_atrib.adicionar_filho(expr)

                    if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == ";":
                        self.pos += 1
                        self.arvores_geradas.append(no_atrib)
                        print("\n[AST Gerada]:")
                        no_atrib.imprimir()
                    else:
                        print(f"[ERRO SINTÁTICO] Esperado ';' na linha {id_destino.linha}")
                else:
                    print(f"\n[ERRO SINTÁTICO] Comando inválido próximo a '{id_destino.lexema}' na linha {id_destino.linha} (esperado '=' ou '(').")
                    while self.pos < len(self.tokens) and self.tokens[self.pos].lexema != ";":
                        self.pos += 1
                    if self.pos < len(self.tokens):
                        self.pos += 1
            else:
                self.pos += 1

    def _parse_E(self, tipo_esperado: str, linha: int):
        no_esq = self._parse_T(tipo_esperado, linha)

        while self.pos < len(self.tokens) and self.tokens[self.pos].lexema in ("+", "-"):
            op = self.tokens[self.pos].lexema
            self.pos += 1
            no_dir = self._parse_T(tipo_esperado, linha)

            no_op = NoAST(op, eh_operador=True)
            no_op.adicionar_filho(no_esq)
            no_op.adicionar_filho(no_dir)
            no_esq = no_op

        return no_esq

    def _parse_T(self, tipo_esperado: str, linha: int):
        no_esq = self._parse_F(tipo_esperado, linha)

        while self.pos < len(self.tokens) and self.tokens[self.pos].lexema in ("*", "/", "%"):
            op = self.tokens[self.pos].lexema
            self.pos += 1
            no_dir = self._parse_F(tipo_esperado, linha)

            no_op = NoAST(op, eh_operador=True)
            no_op.adicionar_filho(no_esq)
            no_op.adicionar_filho(no_dir)
            no_esq = no_op

        return no_esq

    def _parse_F(self, tipo_esperado: str, linha: int) -> NoAST:
        if self.pos >= len(self.tokens):
            return NoAST("ERRO", eh_operador=True)

        token = self.tokens[self.pos]

        if token.lexema == "(":
            self.pos += 1
            no_expr = self._parse_E(tipo_esperado, linha)
            if self.pos < len(self.tokens) and self.tokens[self.pos].lexema == ")":
                self.pos += 1
            else:
                print(f"[ERRO SINTÁTICO] Esperado ')' na linha {linha}")
            return no_expr

        self.pos += 1

        if token.tipo == "ID":
            if token.lexema not in self.variaveis_declaradas:
                print(f"\n[ERRO SEMÂNTICO] Variável '{token.lexema}' utilizada na linha {linha} não foi declarada previamente.")
            return NoAST(token.lexema, eh_operador=False)

        elif token.tipo == "NUMERO":
            return NoAST(token.lexema, eh_operador=False)

        elif token.tipo == "LITERAL":
            if tipo_esperado == "char" and token.lexema.startswith("'") and len(token.lexema) == 3:
                return NoAST(token.lexema, eh_operador=False)

            if tipo_esperado in TIPOS_C:
                print(f"\n[ERRO SEMÂNTICO] Incompatibilidade de tipos na linha {linha}: Não é possível atribuir Literal ({token.lexema}) a um tipo '{tipo_esperado}'.")
            return NoAST(token.lexema, eh_operador=False)

        return NoAST(token.lexema, eh_operador=False)