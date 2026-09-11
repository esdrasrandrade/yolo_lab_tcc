import io
import os
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from picamera2 import Picamera2

CLASSE = "serrote"  # Altere para "martelo", "parafuso", etc.
PASTA_DESTINO = f"tcc_vita_dataset/images/{CLASSE}"
TOTAL_AMOSTRAS = 201

os.makedirs(PASTA_DESTINO, exist_ok=True)


def obter_arquivos_ordenados():
    arquivos = [
        f
        for f in os.listdir(PASTA_DESTINO)
        if f.startswith(CLASSE) and f.endswith(".jpg")
    ]
    return sorted(arquivos)


def obter_proximo_indice():
    arquivos = obter_arquivos_ordenados()
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

# Inicialização Nativa da Câmera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1280, 720)})
picam2.configure(config)
picam2.start()


class StreamingHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return

    def do_GET(self):
        # 1. Transmissão em Tempo Real
        if self.path == "/":
            self.send_response(200)
            self.send_header(
                "Content-type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                while True:
                    stream = io.BytesIO()
                    picam2.capture_file(stream, format="jpeg")
                    buf = stream.getvalue()

                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(buf)))
                    self.end_headers()
                    self.wfile.write(buf)
                    self.wfile.write(b"\r\n")
                    time.sleep(0.08)
            except Exception:
                pass

        # 2. Galeria de Fotos em /fotos (Com Pré-visualização das imagens)
        elif self.path == "/fotos":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            arquivos = obter_arquivos_ordenados()
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: sans-serif; padding: 20px; background-color: #f4f4f9; }}
                    h2 {{ color: #333; }}
                    .btn-reload {{ display: inline-block; padding: 8px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 20px; }}
                    .grid-container {{ display: flex; flex-wrap: wrap; gap: 20px; list-style: none; padding: 0; }}
                    .card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 320px; text-align: center; }}
                    .card img {{ width: 100%; height: auto; border-radius: 4px; display: block; margin-top: 8px; }}
                    .card a {{ font-weight: bold; color: #007bff; text-decoration: none; word-break: break-all; }}
                </style>
            </head>
            <body>
                <h2>Fotos Salvas - Classe: {CLASSE.upper()} ({len(arquivos)}/{TOTAL_AMOSTRAS})</h2>
                <a href="/fotos" class="btn-reload">🔄 Recarregar Galeria</a>
                <ol class="grid-container">
            """
            if not arquivos:
                html += "<li><i>Nenhuma foto salva até o momento.</i></li>"
            else:
                for arq in arquivos:
                    html += f"""
                    <li class="card">
                        <a href="/foto/{arq}" target="_blank">{arq}</a>
                        <a href="/foto/{arq}" target="_blank">
                            <img src="/foto/{arq}" alt="{arq}">
                        </a>
                    </li>
                    """
            html += "</ol></body></html>"
            self.wfile.write(html.encode("utf-8"))

        # 3. Exibição de foto individual
        elif self.path.startswith("/foto/"):
            nome_arq = self.path.replace("/foto/", "")
            caminho_completo = os.path.join(PASTA_DESTINO, nome_arq)
            if os.path.exists(caminho_completo):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open(caminho_completo, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Arquivo nao encontrado")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def iniciar_servidor_http():
    server = ThreadedHTTPServer(("0.0.0.0", 8080), StreamingHandler)
    server.serve_forever()


threading.Thread(target=iniciar_servidor_http, daemon=True).start()

print(f"=== STREAMING E COLETA TCC V.I.T.A ===")
print(f"Abra o Stream no navegador: http://100.78.71.106:8080")
print(f"Abra a Galeria no navegador: http://100.78.71.106:8080/fotos")
print(
    f"Classe ativa: {CLASSE.upper()} | Fotos: {proximo_indice}/{TOTAL_AMOSTRAS}"
)
print("-" * 40)
print("Comandos do Terminal:")
print("  s + ENTER     -> Capturar nova foto")
print("  d + ENTER     -> Deletar a última foto salva")
print("  d N + ENTER   -> Deletar foto específica (ex: d 0, d 9, d 12)")
print("  e + ENTER     -> Sair")
print("-" * 40)

try:
    while proximo_indice < TOTAL_AMOSTRAS:
        entrada = (
            input(
                f"[{proximo_indice}/{TOTAL_AMOSTRAS}] Digite 's', 'd [N]' ou 'e': "
            )
            .strip()
            .lower()
        )
        partes = entrada.split()

        if not partes:
            continue

        comando = partes[0]

        if comando == "s":
            nome_arquivo = os.path.join(
                PASTA_DESTINO, f"{CLASSE}_{proximo_indice:04d}.jpg"
            )
            picam2.capture_file(nome_arquivo)

            if os.path.exists(nome_arquivo):
                print(f"✓ Foto salva: {nome_arquivo}")
                proximo_indice = obter_proximo_indice()
            else:
                print("❌ Erro na captura.")

        elif comando == "d":
            if len(partes) > 1 and partes[1].isdigit():
                idx_alvo = int(partes[1])
                nome_alvo = f"{CLASSE}_{idx_alvo:04d}.jpg"
                caminho_alvo = os.path.join(PASTA_DESTINO, nome_alvo)

                if os.path.exists(caminho_alvo):
                    os.remove(caminho_alvo)
                    print(f"🗑 Foto deletada especificamente: {caminho_alvo}")
                    proximo_indice = obter_proximo_indice()
                else:
                    print(
                        f"⚠️ A foto '{nome_alvo}' não foi encontrada na pasta."
                    )

            else:
                arquivos = obter_arquivos_ordenados()
                if arquivos:
                    ultima_foto = os.path.join(PASTA_DESTINO, arquivos[-1])
                    if os.path.exists(ultima_foto):
                        os.remove(ultima_foto)
                        print(f"🗑 Última foto deletada: {ultima_foto}")
                        proximo_indice = obter_proximo_indice()
                else:
                    print("⚠️ Nenhuma foto encontrada na pasta para deletar.")

        elif comando == "e":
            print("\nEncerrando...")
            break
finally:
    picam2.stop()
