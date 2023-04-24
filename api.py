from flask import Flask, request
from card_detector import CardDetector
from OCR import OCR
from InfoScraper import InfoScraper
from card import Card
import base64
import cv2
import difflib



class CardReader:
    def __init__(self):       
        pass
        self.card_detecor = CardDetector()
        self.OCR = OCR()
        self.info_scraper = InfoScraper()


    def detect_card(self, img):
        warped_imgs = self.card_detecor(img)
        card_name, detected_ID = self.OCR(warped_imgs[1])

        print("Name", card_name)
        print("ID", detected_ID)
        
        current_card_results = self.info_scraper.search_database(card_name)

        if current_card_results is None:
            return {"Success" : False}
        
        all_possible_sets = current_card_results.results['card_sets'].keys()
        detected_card_set = ""
        rarity = ""
        if detected_ID != "":
            detected_card_set = difflib.get_close_matches(detected_ID, all_possible_sets, n = 1)[0]
            rarity = current_card_results.get_card_set_param(detected_card_set, 'set_rarity')


        return current_card_results.results

CR = CardReader()




app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST', 'GET'])
def get_card():
    input_data = request.get_json()
    b64_img = input_data["image"]

    decoded = base64.b64decode(b64_img)

    with open("rec.png", "wb") as f:
        f.write(decoded)

    img = cv2.imread("rec.png")

    resp = CR.detect_card(img)

    
    return resp

app.run()