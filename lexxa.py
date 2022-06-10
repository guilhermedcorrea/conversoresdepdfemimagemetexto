from itertools import zip_longest
import os
import sys
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import cv2
import numpy as np
import re


class Lexxa:
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    def __init__(self):
        self.config= '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        self.tesseract_language = "por"

    def converter_imgpdf(self):
        caminho_pdf = 'C:\\Users\\Guilherme\\Downloads\\estoque LEXXA SC 03-06.pdf'
        imagens_files = 'C:\\Users\\Guilherme\\Desktop\\Python Jobs\\imagemmarcas\\imagem\\'
        images = convert_from_path(caminho_pdf, 200, poppler_path='C:\\Users\\Guilherme\\Desktop\Python Jobs\\tratamentodeimagens\\poppler-0.68.0\\bin')
        for i in range(len(images)):
            images[i].save(imagens_files+'lexxa'+ str(i) +'.jpg', 'JPEG')

    def ajuste_referencias(self, listas):
        lista_dicts = []
        for lista in listas:
            valor = str(lista).split(" ")
            remov_espacos = list(filter(lambda k: len(k.strip()) > 0, valor))
            cont = len(remov_espacos)
            if cont > 7:
                dict_values = {}
                try:
                    dict_values['SKU'] = remov_espacos[0].strip()
                except:
                    dict_values['SKU'] = 'valornaoencontrado'
                try:
                    saldo = str(remov_espacos[-1]).strip()
                    dict_values['SALDO'] = float(saldo)
                except:
                    dict_values['SALDO'] = float(0)

                dict_values['MARCA'] = str('Lexxa')


                lista_dicts.append(dict_values)

        return lista_dicts

    def reader_imagem(self):
        lista_dicts_saldos = []
        imgs = os.listdir('C:\\Users\\Guilherme\\Desktop\\Python Jobs\\imagemmarcas\\imagem\\')

        for im in imgs:

            if 'lexxa' in im:
                img = cv2.imread(f'C:\\Users\\Guilherme\\Desktop\\Python Jobs\\imagemmarcas\\imagem\\{im}')
                #imagemgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #Convertendo para rgb
                imagemgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convertendo para rgb
                texto = pytesseract.image_to_string(imagemgray, lang= self.tesseract_language,config=self.config)
                valor = texto.split("\n")
                dicts = self.ajuste_referencias(valor)

                lista_dicts_saldos.append(dicts)

       
        return lista_dicts_saldos
       
    def create_dicts(self):
        
        from serializer import Produto

        strings = self.reader_imagem()
        for string in strings:
            print(string)
            try:
                marca = string['MARCA']
            except:
                marca = 'Sense'
            try:
                sku = string['SKU']
            except:
                sku = 'valornaoencontrado'
            try:
                saldo = string['SALDO']
            except:
                saldo = float(0)
         
            serializer = Produto(sku, saldo, marca)
            print(serializer.__dict__)

lexxa = Lexxa()
#lexxa.converter_imgpdf()
lexxa.reader_imagem()
lexxa.create_dicts()

