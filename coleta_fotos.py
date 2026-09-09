import time
import os
import cv2

# Defina qual classe vai capturar agora ('serrote' ou 'martelo')
CLASSE = "serrote"  
PASTA_DESTINO = f"tcc_vita_dataset/images/{CLASSE}"
TOTAL_AMOSTRAS = 400

os.makedirs(PASTA_DESTINO, exist_ok=True)

# Inicializa captura via OpenCV (compatível com PiCam via GStreamer/v4l2)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a PiCam! Verifique a conexão do cabo flat.")
    exit()

print(f"=== INICIANDO COLETA DE {TOTAL_AMOSTRAS} FOTOS PARA: {CLASSE.upper()} ===")
print("Pressione 's' para salvar em burst (ou espaço para 1 foto). Pressione 'q' para sair.")

contador = len(os.listdir(PASTA_DESTINO))

while cap.isOpened() and contador < TOTAL_AMOSTRAS:
    ret, frame = cap.read()
    if not ret:
        break

    # Mostra o preview e o contador
    preview = frame.copy()
    cv2.putText(preview, f"Classe: {CLASSE} | Capturas: {contador}/{TOTAL_AMOSTRAS}", 
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Captura PiCam - V.I.T.A", preview)

    key = cv2.waitKey(1) & 0xFF

    # Se pressionar 's', tira uma sequência rápida de fotos
    if key == ord('s'):
        nome_arquivo = os.path.join(PASTA_DESTINO, f"{CLASSE}_{contador:04d}.jpg")
        cv2.imwrite(nome_arquivo, frame)
        print(f"Salvo: {nome_arquivo}")
        contador += 1
        time.sleep(0.3) # Intervalo entre fotos

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Coleta de {CLASSE} concluída! Total de imagens salvas: {contador}")
