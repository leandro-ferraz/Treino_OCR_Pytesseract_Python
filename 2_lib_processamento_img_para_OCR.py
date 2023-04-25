import cv2
import numpy as np
from matplotlib import pyplot as plt

class Processamento_img_para_OCR():
    def __init__(self) -> None:
        pass
    
    def manipulacoes_iniciais(self, diretorio_img, salvarNoTemp=False):
        img = self.abrir_img_cv2(diretorio_img)
        return img

    def inverter_cores_img(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)

        inverted_image = cv2.bitwise_not(img)

        if salvarNoTemp:
            cv2.imwrite('temp/inverted.jpg', inverted_image)
        return inverted_image

    def redimensionar_img(self, imagem=None, diretorio_img= None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)

        if salvarNoTemp:
            pass
        pass

    def afinar_fonte_img(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)
        
        if diretorio_img:
            img = self.abrir_img_cv2(diretorio_img)
        else:
            img = imagem

        img = cv2.bitwise_not(img)
        kernel = np.ones((2,2), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.bitwise_not(img)

        if salvarNoTemp:
            cv2.imwrite('temp/fonte_afinada.jpg', img)
        return (img)

    def engrossar_fonte_img(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)
        img = cv2.bitwise_not(img)
        kernel = np.ones((2,2), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.bitwise_not(img)

        if salvarNoTemp:
            cv2.imwrite('temp/fonte_engrossada.jpg', img)
        return (img)

    def corrigir_rotacao_img(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)

        def obter_imagem_rotacionada(img):
            def obter_angulo_inclinacao(img) -> float:
                #Tratando a imagem para obter o angulo
                newImage = img.copy()
                gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (9, 9), 0)
                thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                #Define uma matriz que é o retângulo do texto considerado
                    #Usa um kernel maior no X para juntar e expandir caracteres da linha
                    #Usa um kernel menor no Y para separar a diferença entre os blocos de texto
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
                #Expande os textos nos retângulos
                dilate = cv2.dilate(thresh, kernel, iterations=2)

                #Encontra os contornos
                contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key = cv2.contourArea, reverse = True)
                for c in contours:
                    rect = cv2.boundingRect(c)
                    x,y,w,h = rect
                    cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

                #Encontra o maior contorno e marca a caixa de área mínima
                largestContour = contours[0]
                print (len(contours))
                minAreaRect = cv2.minAreaRect(largestContour)
                cv2.imwrite("temp/boxes.jpg", newImage)
                #Determina o ângulo de distorção
                angle = minAreaRect[-1]
                if angle < -45:
                    angle = 90 + angle
                return -1.0 * angle

            def rotacionar_imagem(img, angle: float):
                # Rotacionar imagem em torno de seu centro de acordo com o ângulo de inclinação
                newImage = img.copy()
                (h, w) = newImage.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return newImage

            angle = obter_angulo_inclinacao(img)
            return rotacionar_imagem(img, -1.0 * angle)

        img_rotacao_corrigida = obter_imagem_rotacionada(img)

        if salvarNoTemp:
            cv2.imwrite('temp/img_rotacao_corrigida', img_rotacao_corrigida)
        return img_rotacao_corrigida

    def remover_bordas_auto(self, imagem=None, diretorio_img_binaria_sem_ruido=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img_binaria_sem_ruido)
        contornos, hierarquia = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_classificados = sorted(contornos, key=lambda x:cv2.contourArea(x))
        contornos_classificados_maior_area = contornos_classificados[-1]
        x, y, w, h = cv2.boundingRect(contornos_classificados_maior_area)
        img_recortada = img[y:y+h, x:x+w]

        if salvarNoTemp:
            cv2.imwrite('temp/img_borda_removida', img_recortada)
        return(img_recortada)

    def adicionar_bordas_auto(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)
        color = [255, 255, 255]
        top, bottom, left, right = [150]*4
        img_com_borda = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

        if salvarNoTemp:
            cv2.imwrite('temp/img_borda_adicionada', img_com_borda)
        return img_com_borda

    def converter_img_grayscale(self, imagem=None, diretorio_img=None, salvarNoTemp=False):
        img = imagem if imagem else self.abrir_img_cv2(diretorio_img)
        img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if salvarNoTemp:
            cv2.imwrite('temp/grayscale.jpg', img_grayscale)            
        return img_grayscale

    def binarizar_img(self,img_grayscale, salvarNoTemp=False):
        thresh, img_binarizada = cv2.threshold(img_grayscale, 200, 230, cv2.THRESH_BINARY)
        if salvarNoTemp:
            cv2.imwrite('temp/binarizada.jpg', img_binarizada)   
        return img_binarizada
    
    def remover_ruidos_img(self, img_binarizada, salvarNoTemp=False):
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img_binarizada, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.medianBlur(img, 3)

        if salvarNoTemp:
            cv2.imwrite('temp/no_noise.jpg', img)    

        return (img)

    def suavizar_img_filtro_gaussiano(self, img_grayscale, salvarNoTemp=False):
        blur = cv2.GaussianBlur(img_grayscale, (7,7), 0)
        #Possível aplicar treshold depois

    def abrir_img_cv2(self, diretorio_img):
        return cv2.imread(diretorio_img)

    def display_img_grayscale(self, diretorio_img):
        #carrega uma imagem em um arquivo JPG, exibe a imagem em escala de cinza sem cortar/bugar
        img = self.abrir_img_cv2(diretorio_img)

        dpi = 80
        im_data = plt.imread(img)

        height, width  = im_data.shape[:2]
        
        # What size does the figure need to be in inches to fit the image?
        figsize = width / float(dpi), height / float(dpi)

        # Create a figure of the right size with one axes that takes up the full figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])

        # Hide spines, ticks, etc.
        ax.axis('off')

        # Display the image.
        ax.imshow(im_data, cmap='gray')

        plt.show()