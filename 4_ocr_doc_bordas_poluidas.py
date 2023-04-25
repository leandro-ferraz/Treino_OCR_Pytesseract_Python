import pytesseract
import cv2


## ========================================================= 
# Removendo as footnotes do texto
## =========================================================

## Tratando a imagem
path = 'Arquivo\data\sample_mgh.jpg'
image = cv2.imread(path)
im_h, im_w, im_d = image.shape
base_image = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#criando a estrutura retangular e dilatando a imagem
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
dilate = cv2.dilate(thresh, kernal, iterations=1)

## Desenhando o contorno do texto principal para extrair texto
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h<20 and w>250:
        roi = base_image[0:y+h, 0: x+im_w]
        cv2.rectangle(image, (x,y), (x+y, y+h), (36, 255, 12), 2)

cv2.imwrite('Arquivo/temp/ocr_bordasPoluidas/without_border.png', roi)

## ========================================================= 
# Extraindo o texto do maior retângulo encontrado
## ========================================================= 

## Tratando a imagem
path = 'Arquivo/temp/ocr_bordasPoluidas/without_border.png'
image = cv2.imread(path)
print(image.shape)
base_image = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
dilate = cv2.dilate(thresh, kernal, iterations=1)

## Desenhando o contorno do texto principal para extrair texto
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h>200 and w>250:
        roi = base_image[y:y+h, x: x+w]
        cv2.rectangle(image, (x,y), (x+y, y+h), (36, 255, 12), 2)

cv2.imwrite('Arquivo/temp/ocr_bordasPoluidas/sample_boxes.png', roi)

result = pytesseract.image_to_string(roi)
print(result)

#ocr_result = pytesseract.image_to_string(roi)
#print(ocr_result)