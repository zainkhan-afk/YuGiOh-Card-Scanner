from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from VideoThread import VideoThread
import difflib

from card_detector import CardDetector
from OCR import OCR
from InfoScraper import InfoScraper
from card import Card

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)


        self.thread = VideoThread()
        self.card_detecor = CardDetector()
        self.OCR = OCR()
        self.info_scraper = InfoScraper()

        self.all_cards = []
        self.current_card_results = None
        self.current_card = None

        self.sr = 0


        self.detect_pressed = False


        self.detectedCardsTableWidget = self.findChild(QtWidgets.QTableWidget, "detectedCardsTableWidget")


        self.cardInfoTextBrowser = self.findChild(QtWidgets.QTextBrowser, 'cardInfoTextBrowser')

        self.cardNameTextEdit = self.findChild(QtWidgets.QTextEdit, 'cardNameTextEdit') 
        self.cardRarityTextEdit = self.findChild(QtWidgets.QTextEdit, 'cardRarityTextEdit')

        self.detectCardButton = self.findChild(QtWidgets.QPushButton, 'detectCardButton') 
        self.detectCardButton.clicked.connect(self.DetectCardButtonPressed) 

        self.addCardToTableButton = self.findChild(QtWidgets.QPushButton, 'addCardToTableBtn')
        self.addCardToTableButton.clicked.connect(self.AddDataToTable) 

        self.fetchDataButton = self.findChild(QtWidgets.QPushButton, 'fetchDataBtn') 
        self.fetchDataButton.clicked.connect(self.get_data_from_database) 

        self.detectCardButton = self.findChild(QtWidgets.QPushButton, 'playPauseBtn') 
        self.detectCardButton.clicked.connect(self.thread.pause) 

        self.cardConditionComboBox = self.findChild(QtWidgets.QComboBox, 'cardConditionComboBox')
        self.cardLanguageComboBox = self.findChild(QtWidgets.QComboBox, 'cardLanguageComboBox')
        # self.cardRarityComboBox = self.findChild(QtWidgets.QComboBox, 'cardRarityComboBox')
        self.cardEditionComboBox = self.findChild(QtWidgets.QComboBox, 'cardEditionComboBox')
        self.cardSetComboBox = self.findChild(QtWidgets.QComboBox, 'cardSetComboBox')

        self.cardConditionComboBox.currentIndexChanged.connect(self.OnComboBoxChanged)
        self.cardLanguageComboBox.currentIndexChanged.connect(self.OnComboBoxChanged)
        # self.cardRarityComboBox.currentIndexChanged.connect(self.OnComboBoxChanged)
        self.cardEditionComboBox.currentIndexChanged.connect(self.OnComboBoxChanged)
        self.cardSetComboBox.currentIndexChanged.connect(self.OnComboBoxChanged)

        self.cameraInputLabel = self.findChild(QtWidgets.QLabel, 'mainImageLabel')
        self.cameraFrameW = self.cameraInputLabel.geometry().width()
        self.cameraFrameH = self.cameraInputLabel.geometry().height()


        self.detectedCardLabel = self.findChild(QtWidgets.QLabel, 'detectedImageLabel')
        self.detectedCardW = self.detectedCardLabel.geometry().width()
        self.detectedCardH = self.detectedCardLabel.geometry().height()

        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        self.show()

    def DetectCardButtonPressed(self):
        self.detect_pressed = not self.detect_pressed

    def AddDataToTable(self):
        rowPosition = self.detectedCardsTableWidget.rowCount()
        self.detectedCardsTableWidget.insertRow(rowPosition)

        self.detectedCardsTableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(self.sr)))
        self.detectedCardsTableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem('1'))
        self.detectedCardsTableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(self.current_card.card_set))
        self.detectedCardsTableWidget.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(self.current_card.name))
        self.detectedCardsTableWidget.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(self.current_card.rarity))
        self.detectedCardsTableWidget.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(self.current_card.language))
        self.detectedCardsTableWidget.setItem(rowPosition , 6, QtWidgets.QTableWidgetItem(str(self.current_card.ID)))

        self.sr += 1

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    def populate_card_data(self, card_data, detected_ID):
        self.cardSetComboBox.clear()

        all_possible_sets = self.current_card_results.results['card_sets'].keys()
        self.cardSetComboBox.addItems(all_possible_sets)

        if detected_ID != "":
            detected_card_set = difflib.get_close_matches(detected_ID, all_possible_sets, n = 1)
            self.cardSetComboBox.setCurrentText(detected_card_set[0])

        card_set = self.cardSetComboBox.currentText()
        rarity = self.current_card_results.get_card_set_param(card_set, 'set_rarity')
        self.cardRarityTextEdit.setPlainText(rarity)

    def get_data_from_database(self, detected_ID):
        card_name = self.cardNameTextEdit.toPlainText()
        self.current_card_results = self.info_scraper.search_database(card_name)

        if self.current_card_results is not None:
            self.populate_card_data(self.current_card_results, detected_ID)
            self.current_card = Card(ID = self.current_card_results.results['id'], 
                    card_set = self.cardSetComboBox.currentText(), 
                    name = self.current_card_results.results['name'], 
                    rarity = self.cardRarityTextEdit.toPlainText(), 
                    language = self.cardLanguageComboBox.currentText(), 
                    condition = self.cardConditionComboBox.currentText())

            self.show_card_details(self.current_card)

    def OnComboBoxChanged(self, val):
        if self.current_card is not None:
            card_set = self.cardSetComboBox.currentText()
            rarity = self.current_card_results.get_card_set_param(card_set, 'set_rarity')

            if rarity is None:
                return

            self.cardRarityTextEdit.setPlainText(rarity)

            self.current_card.card_set = self.cardSetComboBox.currentText() 
            self.current_card.rarity = self.cardRarityTextEdit.toPlainText()
            self.current_card.language = self.cardLanguageComboBox.currentText() 
            self.current_card.condition = self.cardConditionComboBox.currentText()
            self.show_card_details(self.current_card)

    def show_card_details(self, c):
        self.cardInfoTextBrowser.setText(str(c))

    @pyqtSlot(np.ndarray)
    def update_image(self, camera_frame):
        warped_imgs = self.card_detecor(camera_frame)

        if self.detect_pressed:
            detected_text, detected_ID = self.OCR(warped_imgs[1])
            self.cardNameTextEdit.setPlainText(detected_text)
            self.get_data_from_database(detected_ID)

            self.detect_pressed = False


        qt_camera_img = self.convert_cv_qt(camera_frame, self.cameraFrameW, self.cameraFrameH)
        self.cameraInputLabel.setPixmap(qt_camera_img)

        if warped_imgs is not None:
            qt_cropped_img = self.convert_cv_qt(warped_imgs[1], self.detectedCardW, self.detectedCardH)
            self.detectedCardLabel.setPixmap(qt_cropped_img)
    
    def convert_cv_qt(self, camera_frame, label_w, label_h):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        
        p = convert_to_Qt_format.scaledToHeight(label_h)
        return QPixmap.fromImage(p)
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()