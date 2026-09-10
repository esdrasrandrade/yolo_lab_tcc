import io
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import time

CLASSE = "serrote"  # Altere para "martelo" quando necessário
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
frame_atual = None
lock = threading.Lock()


# Servidor Web para o Stream MJPEG
class StreamingHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header(
                "Content-type",
                "multipart/x-mixed-replace; boundary=FRAME",
            )
            self.end_headers()
            try:
                while True:
                    with lock:
                        if frame_atual is None:
                            time.sleep(0.05)
                            continue
                        buf = frame_atual

                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(buf)))
                    self.end_headers()
                    self.wfile.write(buf)
                    self.wfile.write(b"\r\n")
                    time.sleep(0.08)  # ~12 FPS no navegador
            except Exception:
                pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def iniciar_servidor_http():
    server = ThreadedHTTPServer(("0.0.0.0", 8080), StreamingHandler)
    server.serve_forever()


# Loop contínuo para atualizar a imagem visualizada
def capturar_frames():
    global frame_atual
    while True:
        # Pega uma amostra leve e rápida do sensor para a Web
        cmd = [
            "rpicam-still",
            "-o",
            "-",
            "-t",
            "1",
            "--width",
            "640",
            "--height",
            "480",
            "-n",
            "--quality",
            "50",
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if proc.returncode == 0:
            with lock:
                frame_atual = proc.stdout
        time.sleep(0.05)


# Inicializa as threads do servidor e do stream
threading.Thread(target=iniciar_servidor_http, daemon=True).start()
threading.Thread(target=capturar_frames, daemon=True).start()

print(f"=== STREAMING E COLETA TCC V.I.T.A ===")
print(f"Abra no navegador do PC: http://100.78.71.106:8080")
print(f"Classe ativa: {CLASSE.upper()} | Fotos: {proximo_indice}/{TOTAL_AMOSTRAS}")
print("-" * 40)
print("Comandos do Terminal:")
print("  s + ENTER -> Capturar foto em ALTA RESOLUÇÃO")
print("  d + ENTER -> Deletar última foto")
print("  e + ENTER -> Sair")
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
        # Captura a foto final em boa resolução (720p)
        cmd = [
            "rpicam-still",
            "-o",
            nome_arquivo,
            "-t",
            "100",
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
            print("❌ Erro na captura.")

    elif comando == "d":
        if ultima_foto_salva and os.path.exists(ultima_foto_salva):
            os.remove(ultima_foto_salva)
            print(f"🗑 Foto deletada: {ultima_foto_salva}")
            proximo_indice -= 1
            ultima_foto_salva = None

    elif comando == "e":
        print("\nEncerrando...")
        break
