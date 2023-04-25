# Treino OCR com o pytesseract/python
Este projeto contém desde funções de pré-processamento de imagens e extração de textos com o pytesseract(OCR) , além de casos de uso.

## Introdução
Este projeto foi elaborado para servir como consulta à desenvolvedores python que desejam digitalizar documentos com o motor OCR tesseract. Contém funções úteis para manipulação de imagens e para aplicação de OCR - de forma que sejam obtidos textos com o máximo de precisão.

## Instalação

### Pré-requisitos
- Versão do python: 3.10.7
- Motor OCR: tesseract

### Bibliotecas utilizada no projeto
- cv2
- matplotlib (pyplot)
- numpy
- pytesseract
- PIL
- os

### Módulos 
Os módulos estão organizados forma independentes. Os três primeiros são módulos de consulta e, a partir do quarto, serão abordados casos de uso.

1. <u>1_funcoes_padrao_pre_processamento</u>: contém funções padrões para o pré-processamento de imagens para OCR.
2. <u>2_lib_processamento_img_para_OCR</u>: contém uma classe com vários métodos para o pré-processamento de imagens para OCR
3. <u>3_funcoes_padrao_OCR</u>: contém um pré-processamento básico de imagem e algumas extrações de texto configurando a engine do tesseract.
4. <u>4_ocr_doc_bordas_poluidas</u>: contém um caso de uso de extração de textos relevantes em um documento com bordas poluídas e rodapé desnecessário.
5. <u>5_ocr_doc_multi_colunas</u>: contém um caso de uso de extração de textos relevantes em um documento que possui três colunas.

## Uso
Cada arquivo pode ser executado de forma independente. Os três primeiros módulos servirão como consulta em relação às possibilidades do OCR, e a partir do quarto serão abordados casos de uso.

### Exemplos de uso

- Módulo 1: 
    - "noise_removal('\path\img.png')"
- Módulo 2: MetricasFaturamento()
    - "img = Processamento_img_para_OCR().manipulacoes_iniciais(diretorio_img='\path\img.png')"
    - "img = Processamento_img_para_OCR().inverter_cores_img(img)"
- Módulo 3: 
    - "show_words_rect('imgs\screenshot.png')"
- Módulo 4:
    - apenas compilar
- Módulo 5:
    - apenas compilar

## Contribuições

Se você tiver alguma contribuição, correção de bugs ou feedback, sinta-se à vontade para compartilhar. Agradeço qualquer ajuda para melhorar este projeto.

## Autor

- Leandro de Sousa Ferraz