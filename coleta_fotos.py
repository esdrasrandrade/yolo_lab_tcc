import os
import subprocess
import sys

CLASSE = "serrote"
PASTA_DESTINO = f"tcc_vita_dataset/images/{CLASSE}"
TOTAL_AMOSTRAS = 400

os.makedirs(PASTA_DESTINO, exist_ok=True)


def obter_proximo_indice():
    arquivos = [
        f
        for f in os.listdir(PASTA_DESTINO)
        if f.startswith(CLASSE) and f.endswith(".jpg")
    ]
    if not arquivos:
        return 0
    indices = []
    for f in arquivos:
        try:
            idx = int(f.replace(f"{CLASSE}_", "").replace(".jpg", ""))
            indices.append(idx)
        except ValueError:
            pass
    return max(indices) + 1 if indices else 0


proximo_indice = obter_proximo_indice()
ultima_foto_salva = None

print(f"=== COLETA DE DATASET V.I.T.A ===")
print(f"Classe ativa: {CLASSE.upper()}")
print(f"Diretório: {PASTA_DESTINO}")
print(f"Fotos já armazenadas: {proximo_indice}/{TOTAL_AMOSTRAS}")
print("-" * 40)
print("Comandos:")
print("  s + ENTER -> Capturar e salvar foto")
print("  d + ENTER -> Deletar a última foto capturada")
print("  e + ENTER -> Sair e salvar progresso")
print("-" * 40)

while proximo_indice < TOTAL_AMOSTRAS:
    comando = (
        input(f"[{proximo_indice}/{TOTAL_AMOSTRAS}] Digite 's', 'd' ou 'e': ")
        .strip()
        .lower()
    )

    if comando == "s":
        nome_arquivo = os.path.join(
            PASTA_DESTINO, f"{CLASSE}_{proximo_indice:04d}.jpg"
        )
        cmd = [
            "rpicam-still",
            "-o",
            nome_arquivo,
            "-t",
            "200",
            "--width",
            "1280",
            "--height",
            "720",
            "-n",
        ]
        res = subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        if res.returncode == 0 and os.path.exists(nome_arquivo):
            print(f"✓ Foto salva: {nome_arquivo}")
            ultima_foto_salva = nome_arquivo
            proximo_indice += 1
        else:
            print(
                "❌ Erro ao capturar imagem pela PiCam. Verifique a conexão."
            )

    elif comando == "d":
        if ultima_foto_salva and os.path.exists(ultima_foto_salva):
            os.remove(ultima_foto_salva)
            print(f"🗑 Foto deletada: {ultima_foto_salva}")
            proximo_indice -= 1
            ultima_foto_salva = None
        else:
            print("⚠️ Nenhuma foto recente para deletar nesta sessão.")

    elif comando == "e":
        print("\nSaindo... Progresso salvo com sucesso!")
        sys.exit(0)

    else:
        print("Comando inválido. Use 's' para salvar, 'd' para deletar ou 'e' para sair.")

print(f"\nColeta da classe {CLASSE} finalizada! Total: {proximo_indice} fotos.")
