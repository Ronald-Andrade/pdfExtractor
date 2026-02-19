
# Importações de pastas para fazer a leitura do PDF
import PyPDF2
import os
import sys

print("--- Script iniciado com sucesso ---")

def processar_meu_pdf(nome_arquivo):
    # Verifica se o arquivo está na pasta
    if not os.path.exists(nome_arquivo):
        print(f"--- [!] ERRO: O arquivo '{nome_arquivo}' não existe nesta pasta! ---")
        return

    print(f"--- Arquivo '{nome_arquivo}' localizado. Tentando abrir... ---")

    try:
        with open(nome_arquivo, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            total_paginas = len(leitor.pages)
            print(f"--- PDF aberto! Total de páginas: {total_paginas} ---")

            texto_acumulado = ""

            for i in range(total_paginas):
                print(f"--- [4] Lendo página {i+1}... ---")
                pagina = leitor.pages[i]
                conteudo = pagina.extract_text()
                
                if conteudo:
                    texto_acumulado += conteudo + "\n"
            if texto_acumulado.strip():
                # Exibe no terminal
                print("\n=== CONTEÚDO EXTRAÍDO ===\n")
                print(texto_acumulado)

                # Salva em TXT (gera o nome automaticamente)
                nome_txt = os.path.splitext(nome_arquiv)
                else:
                    print(f"--- [!] Alerta: Página {i+1} parece não ter texto digital (pode ser uma imagem) ---")

            # Se conseguimos algum texto, vamos exibir e salvar
            if texto_acumulado.strip():
                print("\n=== CONTEÚDO EXTRAÍDO ===\n")
                print(texto_acumulado)
                
                # Salvar em TXT
                nome_txt = nome_arquivo.replace(".pdf", ".txt")
                with open(nome_txt, "w", encoding="utf-8") as f:
                    f.write(texto_acumulado)
                print(f"\n--- [5] Sucesso! Arquivo '{nome_txt}' criado! ---")
            else:
                print("--- [!] FIM: Nenhum texto foi encontrado no arquivo. ---")

    except Exception as e:
        print(f"--- [!] Ocorreu um erro técnico: {e} ---")

# EXECUÇÃO
if __name__ == "__main__":
    # Certifique-se de que o nome abaixo é IGUAL ao seu arquivo na pasta src
    meu_arquivo = "documento.pdf.pdf" 
    processar_meu_pdf(meu_arquivo)

#os.path.exists: Evita que o programa trave se você digitar o nome do arquivo errado.
#with open (...): Garante que o arquivo seja fechado corretamente após a leitura, economizando melhora.
#leitor.pages: É uma lista de contendo todas as páginas do documento.
#extract_text(): É o que transforma o dados do PDF em strings