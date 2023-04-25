import cv2
import pytesseract
from pytesseract import Output
import PIL
from PIL import ImageGrab
import os

## ===========================================================
## Salva um screenshot para ser usado como base do OCR
## ===========================================================

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'

if os.path.exists('imgs\screenshot.png'):
    os.remove('imgs\screenshot.png')


screenshot = ImageGrab.grab()
screenshot.save('imgs\screenshot.png')

## ===========================================================
## Tratamento da imagem para OCR
## ===========================================================

def extract_text_OCR(img):
    return pytesseract.image_to_string(img, lang='por')   

def gray_scale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def remove_noise(img):
    return cv2.medianBlur(img, 5)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BYNARY + cv2.THRESH_OTSU)[1]

## ===========================================================
## Aplica OCR com base na configuração de engine do tesseract
## ===========================================================

def first_config_tesseract(img):
    #config do tesseract
    myConfig = r'--psm 3 --oem 3'
    return pytesseract.image_to_sring(PIL.Image.open(img), config=myConfig)
    
def show_letters_rect(img):
    myConfig = r'--psm 3 --oem 3' #config do OCR
    imgNumPy = cv2.imread(img)
    # define o atributo [.shape da matriz NumPy] como altura / largura e ignora o terceiro parametro (num canais de cor)
    height, width, _ = imgNumPy.shape
    boxes = pytesseract.image_to_boxes(imgNumPy, config=myConfig)
    for box in boxes.splitlines():
        box = box.split(" ")
        #height[eixo Y]: no openCV o eixo Y inicia na parte superior esquerda rect, e no tesseract na parte inferior esquerda
        # BGR (Blue, Green, Red) | Espessura = 2        
        img = cv2.rectangle(imgNumPy, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0,255,0), 2)
    cv2.imshow("img", imgNumPy)
    #delay em ms  (0 espera indefinidamente até que uma tecla seja pressionada)
    cv2.waitKey(0)

def show_words_rect(img):
    myConfig = r'--psm 3 --oem 3' #config do OCR
    imgNumPy = cv2.imread(img)
    # define o atributo [.shape da matriz NumPy] como altura / largura e ignora o terceiro valor
    height, width, _ = imgNumPy.shape

    data = pytesseract.image_to_data(img, config=myConfig, output_type=Output.DICT) 
    #print(data['text'])  #print(data.keys())
    print(data['text'][1])
    for i in range(len(data['text'])):
        #se a confianca da palavra atual for maior que...
        if float(data['conf'][i]) > 80:
            #extrai p/ variáveis os dados da palavra atual
            (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            #cria o rect na palavra reconhecida
            img = cv2.rectangle(imgNumPy, (x,y),(x+width, y+height),(0,255,0),2)            
            #coloca o texto reconhecido em baixo do rect
                #y+height+20 - o Y no openCV é calculado de cima para baixo.
            img = cv2.putText(img, data['text'][i], (x,y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)

    cv2.imshow("img", imgNumPy)
    #delay em ms  (0 espera indefinidamente até que uma tecla seja pressionada)
    cv2.waitKey(0)

show_words_rect('imgs\screenshot.png')