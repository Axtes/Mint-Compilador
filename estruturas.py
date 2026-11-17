class Token:
    def __init__(self, tipo: str, lexema: str, linha: int, posicao_ts: int = None):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.posicao_ts = posicao_ts

    def __str__(self):
        if self.tipo == "ID" and self.posicao_ts is not None:
            return f"ID #{self.posicao_ts}"
        elif self.tipo == "PALAVRA_RESERVADA":
            return f"{self.tipo}, {self.lexema.upper()}"
        else:
            return f"{self.tipo}, {self.lexema}"


class Simbolo:
    def __init__(self, id_simbolo: int, lexema: str, categoria: str, tipo_dado: str = "-"):
        self.id = id_simbolo
        self.lexema = lexema
        self.categoria = categoria
        self.tipo_dado = tipo_dado


class NoAST:
    def __init__(self, rotulo: str, eh_operador: bool = True):
        self.rotulo = rotulo
        self.eh_operador = eh_operador
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def imprimir(self):
        linhas, _, _, _ = self._montar_diagrama()
        for linha in linhas:
            print(linha.rstrip())

    def _montar_diagrama(self):
        texto = f"({self.rotulo})" if self.eh_operador else str(self.rotulo)
        largura_no = len(texto)

        if not self.filhos:
            return [texto], largura_no, 1, largura_no // 2

        if len(self.filhos) == 1:
            linhas, w, h, meio = self.filhos[0]._montar_diagrama()
            novo_w = max(w, largura_no)
            desloc = (novo_w - w) // 2
            pos_raiz = meio + desloc

            linha1 = " " * max(0, pos_raiz - largura_no // 2) + texto
            linha2 = " " * pos_raiz + "|"
            linhas_ajustadas = [" " * desloc + l for l in linhas]
            return [linha1, linha2] + linhas_ajustadas, novo_w, h + 2, pos_raiz

        esq_linhas, esq_w, esq_h, esq_meio = self.filhos[0]._montar_diagrama()
        dir_linhas, dir_w, dir_h, dir_meio = self.filhos[1]._montar_diagrama()

        espaco_entre = 3
        pos_esq = esq_meio
        pos_dir = esq_w + espaco_entre + dir_meio
        pos_raiz = (pos_esq + pos_dir) // 2

        inicio_texto = pos_raiz - largura_no // 2
        desloc_global = max(0, -inicio_texto)
        pos_esq += desloc_global
        pos_dir += desloc_global
        pos_raiz += desloc_global
        inicio_texto += desloc_global

        largura_total = max(esq_w + espaco_entre + dir_w + desloc_global, inicio_texto + largura_no)

        linha_pai = list(" " * largura_total)
        for i, ch in enumerate(texto):
            linha_pai[inicio_texto + i] = ch

        dist = (pos_dir - pos_esq) // 2
        linhas_ramos = []
        for step in range(1, max(2, dist)):
            linha_r = list(" " * largura_total)
            idx_e = pos_raiz - step
            idx_d = pos_raiz + step
            if idx_e >= pos_esq:
                linha_r[idx_e] = "/"
            if idx_d <= pos_dir:
                linha_r[idx_d] = "\\"
            if "/" in linha_r or "\\" in linha_r:
                linhas_ramos.append("".join(linha_r))

        if not linhas_ramos:
            linha_r = list(" " * largura_total)
            linha_r[max(0, pos_raiz - 1)] = "/"
            linha_r[min(largura_total - 1, pos_raiz + 1)] = "\\"
            linhas_ramos.append("".join(linha_r))

        altura_max = max(esq_h, dir_h)
        esq_linhas += [" " * esq_w] * (altura_max - esq_h)
        dir_linhas += [" " * dir_w] * (altura_max - dir_h)

        linhas_filhos = []
        for l_e, l_d in zip(esq_linhas, dir_linhas):
            linhas_filhos.append((" " * desloc_global) + l_e + (" " * espaco_entre) + l_d)

        resultado = ["".join(linha_pai)] + linhas_ramos + linhas_filhos
        return resultado, largura_total, len(resultado), pos_raiz