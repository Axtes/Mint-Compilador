import sys
import os
import glob
from lexico import AnalisadorLexico
from sintatico import AnalisadorSintaticoSemantico

def selecionar_arquivo_c() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]

    pasta_local = os.path.dirname(os.path.abspath(__file__))
    arquivos_c = sorted(glob.glob(os.path.join(pasta_local, "*.c")))

    if not arquivos_c:
        return ""

    if len(arquivos_c) == 1:
        return arquivos_c[0]

    print("\nArquivos .c encontrados na pasta local:")
    for idx, caminho in enumerate(arquivos_c, start=1):
        print(f"  [{idx}] {os.path.basename(caminho)}")

    while True:
        escolha = input("\nDigite o número do arquivo que deseja compilar: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos_c):
            return arquivos_c[int(escolha) - 1]
        print("Opção inválida. Tente novamente.")

def main():
    caminho_arquivo = selecionar_arquivo_c()

    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        print("Erro: Nenhum arquivo '.c' encontrado na pasta local do programa.")
        return

    try:
        print(f"\nLendo arquivo fonte: {os.path.basename(caminho_arquivo)}")
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            codigo_fonte = arquivo.read()

        lexico = AnalisadorLexico()
        lexico.analisar(codigo_fonte)

        sintatico = AnalisadorSintaticoSemantico(lexico.tokens, lexico.tabela_simbolos)
        sintatico.analisar()

        lexico.exibir_tabela_simbolos()

    except Exception as e:
        print(f"Erro ao processar o arquivo '{caminho_arquivo}': {e}")

if __name__ == "__main__":
    main()