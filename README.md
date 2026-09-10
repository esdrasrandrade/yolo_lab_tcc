# Guia de Coleta de Dados e Streaming para o Dataset V.I.T.A.

Este repositório contém as rotinas para captura, visualização em tempo real e estruturação das amostras de imagem do projeto V.I.T.A. (Visão Inteligente de Triagem Automática). O fluxo utiliza a Raspberry Pi Camera (PiCam) integrada a um servidor HTTP leve para transmissão de vídeo (*streaming*) via navegador, permitindo o enquadramento adequado das peças antes da gravação dos dados.

---

## Estrutura do Repositório

```text
yolo_lab/
├── coleta_fotos.py          # Script de captura via terminal
├── stream_e_coleta.py       # Script principal (Streaming HTTP + Captura em alta resolução)
├── tcc_vita_dataset/        # Diretório raiz para armazenamento das imagens
│   └── images/              # Subpastas divididas por classe (ex: serrote, martelo, etc.)
└── requirements.txt         # Dependências do ambiente Python


Requisitos Prévios
1. Hardware: Raspberry Pi 5 com Raspberry Pi Camera Module (OV5647 ou superior) conectada e reconhecida.

2. Sistema Operacional: Raspberry Pi OS (Bookworm) 64-bits.

3. Rede: A Raspberry Pi e o computador do operador devem estar conectados à mesma rede local.

```

# Configuração do ambiente

1. Clonar o repositório
   git clone [https://github.com/esdrasrandrade/yolo_lab_tcc.git](https://github.com/esdrasrandrade/yolo_lab_tcc.git)
   cd yolo_lab_tcc
2. Criar e Ativar o Ambiente Virtual (venv)
   python -m venv venv
   source venv/bin/activate

3. Verificar a Conexão da Câmera
   Certifique-se de que o sensor é identificado pelo sistema:
   
   ```rpicam-hello --list-cameras```
   
# Instruções de Uso
## 1. Configurar a Classe Alvo
Antes de executar a captura, edite o arquivo stream_e_coleta.py para indicar a classe de objeto que será fotografada:

   ```nano stream_e_coleta.py```

Altere o valor da variável CLASSE para o nome exato da classe correspondente (serrote, martelo, estilete ou parafuso):

```CLASSE = "serrote"  # Altere para a classe que será coletada no momento```

Salve e feche o arquivo (Ctrl + O, Enter, Ctrl + X).

## 2. Executar o Script de Streaming e Coleta
Com o ambiente virtual ativo, inicie a aplicação:

   ````python stream_e_coleta.py````
   
## 3. Visualizar o Feed de Vídeo no Navegador
Antes de seguir, verifique o endereço IP local da sua Raspberry Pi através do comando ```hostname -I``` no terminal. Abra um navegador no computador (Chrome, Firefox ou Edge) e acesse a URL:

   ````http://<IP_DA_RASPBERRY_PI>:8080````
   
Utilize a transmissão em tempo real para ajustar o enquadramento, foco, distância e iluminação da peça sobre a esteira/bancada.

## 4. Atalhos de Controle pelo Terminal
Retorne à janela do terminal SSH para operar a captura de imagens através dos comandos:

s + ENTER: Captura e salva uma imagem em alta resolução ($1280 \times 720$) na pasta da classe ativa.

d + ENTER: Apaga a última foto gravada durante a sessão (útil em caso de borrões ou desalinhamento).

e + ENTER: Finaliza a execução do programa e salva o progresso atual.

# Exportação e Unificação do Lote
Ao concluir a coleta do seu lote de amostras (meta de 400 imagens por classe), siga os passos abaixo para compactar e disponibilizar os arquivos para unificação:
1. Compactar o Lote na Raspberry Pi:
   zip -r lote_imagens.zip tcc_vita_dataset/
2. Baixar o Arquivo para o Computador Local (via PowerShell/Terminal do Windows):
   scp usuario@<IP_DA_RASPBERRY_PI>:~/yolo_lab/lote_imagens.zip C:\Caminho\De\Destino\

Pronto, após todo esse procedimento, as capturas estarão salvas e no jeito de ser compartilhado.
   
