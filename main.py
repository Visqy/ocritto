import shutil
import numpy as np
import fitz
import PIL
from PIL import Image
from os import listdir, path, mkdir
import re
import cv2
import pytesseract
from pytesseract import Output

#global variable
path_temp = r"./temp/"
path_pdf = r"./pdf/"
path_result = r"./result/"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'-c tessedit_char_whitelist=QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghhjklzxcvbnm --psm 6'

def createFolder(file, Path):
    name_file = path.split(file)[1]
    mapel, paket = name_file.split('.')[0].split('_')
    output_path = Path + mapel + '/' + paket + '/'
    pembahasan_path = output_path + 'pembahasan/'
    soal_path = output_path + 'soal/'
    if not path.exists(output_path):
        mkdir(output_path)
        mkdir(soal_path)
        mkdir(pembahasan_path)
    return pembahasan_path, soal_path, name_file, output_path

def createCombineImage(file):
    pdf = fitz.open(path_pdf + file)
    imgs = []
    for page_number in range(pdf.pageCount):
        page = pdf.loadPage(page_number)
        pix = page.get_pixmap(matrix = fitz.Matrix(2,2))
        mode ='RGB'
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        width, height = img.size
        imgs.append(img.crop((width*10/100,height*7/100,width*90/100,height*93/100)))
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs = np.vstack([np.asarray( i.resize(min_shape) ) for i in imgs ])
    cv_img = imgs[:, :, ::-1].copy()
    return cv_img

def scanImage(img):
    height, width, _ = img.shape
    d = pytesseract.image_to_data(img[0:height, int(width*40/100):int(width*60/100)], output_type=Output.DICT)
    list(d.keys())
    list_cord = [d['top'][i] for i in range(len(d['text'])) if float(d['conf'][i]) > 60 and re.match('Nomor', d['text'][i])]
    height, width, _ = img.shape
    for i in range(len(list_cord)):
        try:
            h = list_cord[i+1]
        except IndexError:
            h = height
        imgSplit = img[list_cord[i]:h, 0:width]
        d = pytesseract.image_to_data(imgSplit, output_type=Output.DICT)
        list(d.keys())
        #list_cord2 = [d['top'][i] for i in range(len(d['text'])) if float(d['conf'][i]) > 60 and re.match('Pembahasan', d['text'][i])]
        list_cord2 = []
        materi=[]
        for j in range(len(d['text'])): 
            if float(d['conf'][j]) > 60:
                if re.match('Pembahasan', d['text'][j]):
                    list_cord2.append(d['top'][j]) 
                elif re.match('Materi', d['text'][j]):
                    x, y = d['top'][j]-5, d['height'][j]+10
                    materi.append(pytesseract.image_to_string(imgSplit[x:x+y, int(width*13/100):width], config=custom_config).strip())
        #cv2.imshow('s', imgSplit[x:x+y, int(width*13/100):width])
        #cv2.waitKey(0)
        cv2.imwrite(pembahasan_path + f"pembahasan_soal_{i+1}_{materi[0]}.jpg", imgSplit)
        cv2.imwrite(soal_path + f"soal_{i+1}_{materi[0]}.jpg", imgSplit[0:list_cord2[0], 0:width])


for pdf_file in listdir(path_pdf):
    if pdf_file.endswith(".pdf"):
        pembahasan_path, soal_path, name_file, output_path = createFolder(pdf_file, path_result)
        img = createCombineImage(pdf_file)
        try:
            print('scanning ' + name_file)
            scanImage(img)
            print('done')
        except Exception:
            print('fail')
            shutil.rmtree(output_path, ignore_errors=True, onerror=None)
            continue
        