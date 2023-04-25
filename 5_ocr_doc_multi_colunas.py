import pytesseract
import cv2

path = 'Arquivo\data\index_02.jpg'

image = cv2.imread(path)
base_image = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.treshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
dilate = cv2.dilate(thresh, kernal, iterations=1)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+h]
        #cv2.imwrite('Arquivo\temp\ocr_multicoluna\index_roi.png')
        cv2.rectangle(image, (x,y), (x+w, y+h), (36, 255, 12), 2)
        ocr_result = pytesseract.image_to_string(roi)

        #print(ocr_result)
        ocr_result = ocr_result.split('\n')
        results = []
        for item in ocr_result:
            results.append(item)

        entities = []
        for item in results:
            item = item.strip().replace('\n', '')
            item = item.split(' ')[0]
            if len(item) > 2 and item[0].isupper():
                if item[0] == 'A' and '-' not in item:
                    item = item.split('.')[0].replace(',' '').replace(';', '')
                    entities.append(item)
        #obtendo uma lista sem duplicados e ordenando
        entities = list(set(entities)).sort()

cv2.imwrite('Arquivo\temp\ocr_multicoluna\index_bbox_new.png', image)