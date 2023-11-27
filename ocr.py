import requests
import time
import json
import os
from PIL import Image, ImageEnhance
import pytesseract

def ocr_space_file(filename, overlay=False, api_key='e61f4d4c3488957', language='eng'):
    """ OCR.space API request with local file.
        Python3.7 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()
def ocr_result(image_path):
    image = Image.open(image_path)
    enh_con = ImageEnhance.Contrast(image)
    contrast = 2.0
    image = enh_con.enhance(contrast)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image, lang='eng')

    # Process the text to extract word bounding boxes
    word_infos = []
    for line in text.split('\n'):
        words = line.split()
        for word in words:
            if not word:
                continue
            # Assuming that word_info["boundingBox"] should be in the format [topleft_x, topleft_y, topleft_x, bottomleft_y]
            bounding_box = [0, 0, 0, 0]
            word_info = {
                "text": word,
                "boundingBox": bounding_box
            }
            word_infos.append(word_info)

    return word_infos
#usage with whatever Path-example in google drive 
image_path = '/content/drive/MyDrive/data/evalset_fqa/vbar/bitmap'
image_names = os.listdir(image_path)
for name in ['495.jpg', '151.jpg']:
    image_file_path = os.path.join(image_path, name)
    result = ocr_result(image_file_path)
    print(result)
