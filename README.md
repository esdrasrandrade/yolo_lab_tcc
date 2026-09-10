# Passo a Passo para Executar a Coleta de dados
1. Ative o ambiente virtual (venv)

    source venv/bin/activate

2. Modifique a variável da classe e o caminho da pasta correspondente aonde as imagens do dataset vão ser armazenadas:
   
    ```nano ~/yolo_lab/coleta_fotos.py```
   
    Dentro do coleta_fotos.py defina qual classe vai capturar agora ('serrote', 'martelo', "parafuso"...) nessas linhas abaixo:
   
      CLASSE = "serrote" #Coloque o nome da classe aqui 

   Leia esse arquivo coleta_fotos.py, ele orienta como é a captura.

4. Execute o script para iniciar a captura:
Bash:
```python coleta_fotos.py```
