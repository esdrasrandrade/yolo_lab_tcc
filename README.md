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

##Configuração do ambiente

1. Clonar o repositório
   git clone [https://github.com/esdrasrandrade/yolo_lab_tcc.git](https://github.com/esdrasrandrade/yolo_lab_tcc.git)
   cd yolo_lab_tcc
2. Criar e Ativar o Ambiente Virtual (venv)
   python -m venv venv
   source venv/bin/activate

3. Verificar a Conexão da Câmera
   Certifique-se de que o sensor é identificado pelo sistema:
   rpicam-hello --list-cameras
