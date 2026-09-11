import os
import sys

# =========================================================
# CONFIGURAÇÃO: Digite o nome da classe que deseja organizar
# =========================================================
CLASSE = "parafuso"  # Altere aqui para "martelo", "parafuso", "estilete", etc.

# Caminho base das imagens no seu projeto
PASTA_IMAGENS = f"tcc_vita_dataset/images/{CLASSE}"


def padronizar_dataset(nome_classe, caminho_pasta):
    if not os.path.exists(caminho_pasta):
        print(f"❌ Erro: A pasta '{caminho_pasta}' não foi encontrada.")
        return

    # Filtra apenas extensões válidas de imagem
    extensoes_validas = (".jpg", ".jpeg", ".png")
    arquivos = [
        f
        for f in os.listdir(caminho_pasta)
        if f.lower().endswith(extensoes_validas)
    ]

    if not arquivos:
        print(f"⚠️ Nenhuma imagem encontrada na pasta '{caminho_pasta}'.")
        return

    # Ordena os arquivos para manter a sequência lógica original
    arquivos = sorted(arquivos)
    total = len(arquivos)

    print(f"\n=========================================")
    print(f"Organizando Classe: {nome_classe.upper()}")
    print(f"Diretório: {caminho_pasta}")
    print(f"Total de fotos encontradas: {total}")
    print(f"=========================================\n")

    # Passo 1: Renomeia tudo para um nome temporário neutro (evita conflitos de nomes existentes)
    print(" [1/2] Aplicando nomes temporários...")
    for idx, arq in enumerate(arquivos):
        ext = os.path.splitext(arq)[1]
        origem = os.path.join(caminho_pasta, arq)
        temp_nome = os.path.join(caminho_pasta, f"__temp_{idx:04d}__{ext}")
        os.rename(origem, temp_nome)

    # Passo 2: Aplica o nome final no padrão oficial (iniciando do 0000)
    print(" [2/2] Padronizando sequencial a partir do 0000...")
    arquivos_temp = sorted(
        [f for f in os.listdir(caminho_pasta) if f.startswith("__temp_")]
    )

    for idx, arq_temp in enumerate(arquivos_temp):
        origem = os.path.join(caminho_pasta, arq_temp)
        nome_final = f"{nome_classe}_{idx:04d}.jpg"
        destino = os.path.join(caminho_pasta, nome_final)
        os.rename(origem, destino)

    print(f"\n✓ Sucesso! {total} arquivos renomeados.")
    print(
        f"  Primeiro arquivo: {nome_classe}_0000.jpg"
    )
    print(
        f"  Último arquivo:   {nome_classe}_{total - 1:04d}.jpg"
    )
    print("-----------------------------------------\n")


if __name__ == "__main__":
    padronizar_dataset(CLASSE, PASTA_IMAGENS)
