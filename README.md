Passo a Passo para Executar a Coleta
1. Ative o ambiente virtual (venv)

Bash:
source venv/bin/activate

2. Modifique a variável da claasse e o caminho da pasta correspondente aonde as imagens do dataset vão ser armazenadas:
Bash:
nano ~/yolo_lab/coleta_fotos.py
# Defina qual classe vai capturar agora ('serrote', 'martelo', "parafuso"...)
CLASSE = "serrote"  
PASTA_DESTINO = f"tcc_vita_dataset/images/{NOME_DA_CLASSE _AQUI}"
TOTAL_AMOSTRAS = 400

Leia esse arquivo coleta_fotos.py, ele orienta como é a captura.

3. Execute o script para iniciar a captura:
Bash:
python coleta_fotos.py
