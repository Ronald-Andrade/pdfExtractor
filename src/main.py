import PyPDF2 # Biblioteca para manipular e extrair dados de arquivos PDF
import os # Biblioteca para interagir com o sistema de arquivos do computador

# Função que recebe a entrada do arquivo e garante que o caminho seja válido
def obter_caminho_arquivo():
# Solicita que o usuário digite o local do arquivo no computador
    caminho_input = input("Digite o nome do arquivo ou o caminho completo (ex: C:\\Pasta\\meu.pdf): ").strip()
#Remove aspas que o Windows coloca automaticamente ao "Copiar como  caminho"
    caminho = caminho_input.replace('"', '').replace("'", "")
    
# Verifica se o arquivo realmente existe no endereço fornecido
    if not os.path.exists(caminho):
        # abspath mostra o caminho completo(absoluto) para ajudar a conferir o erro
        print(f"--- [!] ERRO: Arquivo não encontrado em: {os.path.abspath(caminho)} ---")
        return None
    #  Retorna o caminho limpo e validado para quem chamou a função
    return caminho

# Função que converte o que o usuário quer em algo entendível para o computador.
def definir_paginas(total):
    # Mistra ao usuário o limite de páginas do documento atual
    """Gerencia a lógica de escolha de páginas."""
    print(f"\nTotal de páginas: {total}")
    print("Escolha: [Número único] ou [Início-Fim] ou [ENTER para tudo]")
    escolha = input("Sua escolha: ").strip()

    #Se o usuário apenas apertar Enter, retorna todas as páginas
    if not escolha:
        return list(range(total)), "completo"
    
    try:
        if "-" in escolha:
            # Verifica se o usuário digitou um untervalo usando hífen (ex: '-5)
            inicio, fim = map(int, escolha.split("-"))
            # cria a lista de páginas. Subtrai 1 pois o Python começa a contar do 0.
            #  0 min() garante que o fim não ultrapasse o total de páginas do PDF
            indices = list(range(inicio - 1, min(fim, total)))
            return indices, f"pag_{escolha}"
        else:
            # Se for apenas um número, converte para inteiro e subtrai 1
            p = int(escolha) - 1
            # Verifica se a página escolhida existe dentro do documento
            if 0 <= p < total:
                return [p], f"pag_{escolha}"
    except ValueError:
        # Se o usuário digitar letras ou símbolos inválidos cai aqui
        pass
    
    # Caso ocorra algum erro na digitação, o padrão é processar tudo
    print("--- [!] Entrada inválida. Usando documento completo. ---")
    return list(range(total)), "completo"

#Função que interage com a lib PyPDF2.
def extrair_texto(caminho, lista_paginas):
    """Realiza a extração bruta do texto das páginas selecionadas."""
    texto = "" #Variável para acumular o texto de todas as páginas
    try:
        # Abre o arquivo  PDF em modo de leitura binária ('rb')
        with open(caminho, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            # Percorre apenas as páginas que o usuário selecionou anteriormente
            for i in lista_paginas:
                print(f"--- Lendo página {i+1}... ---")
                # Extrai o texto da páginas atual(i)
                conteudo = leitor.pages[i].extract_text()
                if conteudo:
                    # Adiciona o texto ao acumulador com um cabeçalho para organização
                    texto += f"--- PÁGINA {i+1} ---\n{conteudo}\n\n"
        return texto
    except Exception as e:
        # Retorna a mensagem de erro técnica caso algo falhe na leitura 
        return f"Erro na leitura: {e}"

# O finalizador que grava o resultado no disco rígido
def salvar_arquivo(texto, caminho_original, sufixo):
    # os.path.splitext divide o caminho em (nome, extensão). Pegamos [0] (nome)
    # Novo nome trocando ,pdf por _sufixo.txt
    nome_txt = os.path.splitext(caminho_original)[0] + f"_{sufixo}.txt"

    #  Abre (ou cria) o arquivo TXT usando codificação UTF-8 para aceitar acentos
    with open(nome_txt, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n--- [OK] Sucesso! Arquivo salvo em: '{nome_txt}' ---")

# Quem coordena a ordem das ações
def executar_workflow():
    # 1. Tenta pegar o caminho do arquivo
    """Função principal que coordena as outras."""
    arquivo_pdf = obter_caminho_arquivo()
    if not arquivo_pdf: # Se o caminho for inválido, encerra aqui
        return

    # 2.Abre o PDF apenas para pegar o total de páginas inicialmente
    with open(arquivo_pdf, 'rb') as f:
        total = len(PyPDF2.PdfReader(f).pages)

    # 3. Define quais páginas serão lidas
    paginas, sufixo = definir_paginas(total)

    # 4. Chama a extração de texto propriamente dita
    resultado = extrair_texto(arquivo_pdf, paginas)

    # 5. Verifica se algo foi extraído antes de mostrar e salvar
    if resultado.strip():
        print("\n=== CONTEÚDO EXTRAÍDO ===\n")
        print(resultado)
        salvar_arquivo(resultado, arquivo_pdf, sufixo)
    else:
        print("--- [!] Nenhum texto encontrado. ---")

if __name__ == "__main__":
    executar_workflow()