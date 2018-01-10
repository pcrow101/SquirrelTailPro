#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json

class KeywordAndColoursUI(QDialog):
    def __init__(self, parent):
        super(KeywordAndColoursUI, self).__init__(parent)
        self.setWindowTitle('Highlighting')
        self.setFixedSize(340, 520)
        self.new_keywords = []

        try:
            with open('config/keywordsToHighlight.json', 'r') as json_file:
                self.keywords = json.load(json_file)
        except:
            self.parent().statusBar.showMessage("Status: Could not open file with keywords to highlight")

        # load words into list
        for (keyword, colour) in self.keywords:
            tmpwords = []
            tmpwords.append(keyword)
            tmpwords.append(colour)
            self.new_keywords.append(tmpwords)

        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()

        # Add frames to dialog screen
        aFrame = QFrame(self)
        aFramelayout = QVBoxLayout(aFrame)
        aFramelayout.addWidget(self.topFrame)
        aFramelayout.addWidget(self.middleFrame)
        aFramelayout.addWidget(self.bottomFrame)

    def create_top_frame(self):
        # Create top frame for displaying title
        self.topFrame = QFrame()
        topFrameLayout = QVBoxLayout(self.topFrame)
        topFrameLayout.setSpacing(1)

        font = QFont()
        font.setFamily('Lucida')
        font.setFixedPitch(True)
        font.setPointSize(18)

        title_label = QLabel()
        title_label.setText("Configure Keywords and Colours")
        title_label.setStyleSheet("color: rgb(0,0,200);")
        title_label.setFont(font)
        topFrameLayout.addWidget(title_label)

    def create_middle_frame(self):
        # Create middle frame with the list of keywords and their highlight colours
        self.middleFrame = QFrame()
        middleFrameLayout = QGridLayout(self.middleFrame)
        middleFrameLayout.setSpacing(4)
        font = QFont()
        font.setFamily('Lucida')
        font.setFixedPitch(True)
        font.setPointSize(14)

        # First row just cointains column headings
        yPos = 0
        priority_title_label = QLabel()
        priority_title_label.setText("Pty")
        priority_title_label.setFont(font)
        keyword_title_label = QLabel()
        keyword_title_label.setText("          Keyword")
        keyword_title_label.setFont(font)
        colour_title_label = QLabel()
        colour_title_label.setText("   Colour")
        colour_title_label.setFont(font)
        middleFrameLayout.addWidget(priority_title_label, yPos, 0)
        middleFrameLayout.addWidget(keyword_title_label, yPos, 1)
        middleFrameLayout.addWidget(colour_title_label, yPos, 2)

        yPos += 1
        kwordlist = self.new_keywords[0]
        priority_label_1 = QLabel()
        priority_label_1.setText(str(yPos))
        priority_label_1.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_1 = QLineEdit()
        self.keywork_line_edit_1.setText(str(kwordlist[0]))
        self.keywork_line_edit_1.setFixedWidth(150)
        self.colour_line_edit_1 = QLineEdit()
        self.colour_line_edit_1.setText(str(kwordlist[1]))
        self.colour_line_edit_1.setFixedWidth(65)
        select_colour_button_1 = QToolButton()
        select_colour_button_1.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_1.clicked.connect(self.on_click_colour_picker_button_1)
        middleFrameLayout.addWidget(priority_label_1, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_1, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_1, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_1, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[1]
        priority_label_2 = QLabel()
        priority_label_2.setText(str(yPos))
        self.keywork_line_edit_2 = QLineEdit()
        self.keywork_line_edit_2.setText(str(kwordlist[0]))
        self.keywork_line_edit_2.setFixedWidth(150)
        self.colour_line_edit_2 = QLineEdit()
        self.colour_line_edit_2.setText(str(kwordlist[1]))
        self.colour_line_edit_2.setFixedWidth(65)
        select_colour_button_2 = QToolButton()
        select_colour_button_2.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_2.clicked.connect(self.on_click_colourPickerButton2)
        middleFrameLayout.addWidget(priority_label_2, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_2, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_2, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_2, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[2]
        priority_label_3 = QLabel()
        priority_label_3.setText(str(yPos))
        self.keywork_line_edit_3 = QLineEdit()
        self.keywork_line_edit_3.setText(str(kwordlist[0]))
        self.keywork_line_edit_3.setFixedWidth(150)
        self.colour_line_edit_3 = QLineEdit()
        self.colour_line_edit_3.setText(str(kwordlist[1]))
        self.colour_line_edit_3.setFixedWidth(65)
        select_colour_button_3 = QToolButton()
        select_colour_button_3.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_3.clicked.connect(self.on_click_colourPickerButton3)
        middleFrameLayout.addWidget(priority_label_3, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_3, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_3, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_3, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[3]
        priority_label_4 = QLabel()
        priority_label_4.setText(str(yPos))
        priority_label_4.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_4 = QLineEdit()
        self.keywork_line_edit_4.setText(str(kwordlist[0]))
        self.keywork_line_edit_4.setFixedWidth(150)
        self.colour_line_edit_4 = QLineEdit()
        self.colour_line_edit_4.setText(str(kwordlist[1]))
        self.colour_line_edit_4.setFixedWidth(65)
        select_colour_button_4 = QToolButton()
        select_colour_button_4.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_4.clicked.connect(self.on_click_colourPickerButton4)
        middleFrameLayout.addWidget(priority_label_4, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_4, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_4, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_4, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[4]
        priority_label_5 = QLabel()
        priority_label_5.setText(str(yPos))
        priority_label_5.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_5 = QLineEdit()
        self.keywork_line_edit_5.setText(str(kwordlist[0]))
        self.keywork_line_edit_5.setFixedWidth(150)
        self.colour_line_edit_5 = QLineEdit()
        self.colour_line_edit_5.setText(str(kwordlist[1]))
        self.colour_line_edit_5.setFixedWidth(65)
        select_colour_button_5 = QToolButton()
        select_colour_button_5.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_5.clicked.connect(self.on_click_colourPickerButton5)
        middleFrameLayout.addWidget(priority_label_5, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_5, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_5, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_5, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[5]
        priority_label_6 = QLabel()
        priority_label_6.setText(str(yPos))
        priority_label_6.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_6 = QLineEdit()
        self.keywork_line_edit_6.setText(str(kwordlist[0]))
        self.keywork_line_edit_6.setFixedWidth(150)
        self.colour_line_edit_6 = QLineEdit()
        self.colour_line_edit_6.setText(str(kwordlist[1]))
        self.colour_line_edit_6.setFixedWidth(65)
        select_colour_button_6= QToolButton()
        select_colour_button_6.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_6.clicked.connect(self.on_click_colourPickerButton6)
        middleFrameLayout.addWidget(priority_label_6, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_6, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_6, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_6, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[6]
        priority_label_7 = QLabel()
        priority_label_7.setText(str(yPos))
        priority_label_7.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_7 = QLineEdit()
        self.keywork_line_edit_7.setText(str(kwordlist[0]))
        self.keywork_line_edit_7.setFixedWidth(150)
        self.colour_line_edit_7 = QLineEdit()
        self.colour_line_edit_7.setText(str(kwordlist[1]))
        self.colour_line_edit_7.setFixedWidth(65)
        select_colour_button_7 = QToolButton()
        select_colour_button_7.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_7.clicked.connect(self.on_click_colourPickerButton7)
        middleFrameLayout.addWidget(priority_label_7, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_7, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_7, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_7, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[7]
        priority_label_8 = QLabel()
        priority_label_8.setText(str(yPos))
        priority_label_8.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_8 = QLineEdit()
        self.keywork_line_edit_8.setText(str(kwordlist[0]))
        self.keywork_line_edit_8.setFixedWidth(150)
        self.colour_line_edit_8 = QLineEdit()
        self.colour_line_edit_8.setText(str(kwordlist[1]))
        self.colour_line_edit_8.setFixedWidth(65)
        select_colour_button_8 = QToolButton()
        select_colour_button_8.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_8.clicked.connect(self.on_click_colourPickerButton8)
        middleFrameLayout.addWidget(priority_label_8, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_8, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_8, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_8, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[8]
        priority_label_9 = QLabel()
        priority_label_9.setText(str(yPos))
        priority_label_9.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_9 = QLineEdit()
        self.keywork_line_edit_9.setText(str(kwordlist[0]))
        self.keywork_line_edit_9.setFixedWidth(150)
        self.colour_line_edit_9 = QLineEdit()
        self.colour_line_edit_9.setText(str(kwordlist[1]))
        self.colour_line_edit_9.setFixedWidth(65)
        select_colour_button_9 = QToolButton()
        select_colour_button_9.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_9.clicked.connect(self.on_click_colourPickerButton9)
        middleFrameLayout.addWidget(priority_label_9, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_9, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_9, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_9, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[9]
        priority_label_10 = QLabel()
        priority_label_10.setText(str(yPos))
        priority_label_10.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_10 = QLineEdit()
        self.keywork_line_edit_10.setText(str(kwordlist[0]))
        self.keywork_line_edit_10.setFixedWidth(150)
        self.colour_line_edit_10 = QLineEdit()
        self.colour_line_edit_10.setText(str(kwordlist[1]))
        self.colour_line_edit_10.setFixedWidth(65)
        select_colour_button_10 = QToolButton()
        select_colour_button_10.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_10.clicked.connect(self.on_click_colourPickerButton10)
        middleFrameLayout.addWidget(priority_label_10, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_10, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_10, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_10, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[10]
        priority_label_11 = QLabel()
        priority_label_11.setText(str(yPos))
        priority_label_11.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_11 = QLineEdit()
        self.keywork_line_edit_11.setText(str(kwordlist[0]))
        self.keywork_line_edit_11.setFixedWidth(150)
        self.colour_line_edit_11 = QLineEdit()
        self.colour_line_edit_11.setText(str(kwordlist[1]))
        self.colour_line_edit_11.setFixedWidth(65)
        select_colour_button_11 = QToolButton()
        select_colour_button_11.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_11.clicked.connect(self.on_click_colourPickerButton11)
        middleFrameLayout.addWidget(priority_label_11, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_11, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_11, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_11, yPos, 3)

        yPos += 1
        kwordlist = self.new_keywords[11]
        priority_label_12 = QLabel()
        priority_label_12.setText(str(yPos))
        priority_label_12.setStyleSheet("QLineEdit { background-color : black; color : gray; padding: 0; boarder-radius: 0px}")
        self.keywork_line_edit_12 = QLineEdit()
        self.keywork_line_edit_12.setText(str(kwordlist[0]))
        self.keywork_line_edit_12.setFixedWidth(150)
        self.colour_line_edit_12 = QLineEdit()
        self.colour_line_edit_12.setText(str(kwordlist[1]))
        self.colour_line_edit_12.setFixedWidth(65)
        select_colour_button_12 = QToolButton()
        select_colour_button_12.setIcon(QIcon('icons/colourPicker.png'))
        select_colour_button_12.clicked.connect(self.on_click_colourPickerButton12)
        middleFrameLayout.addWidget(priority_label_12, yPos, 0)
        middleFrameLayout.addWidget(self.keywork_line_edit_12, yPos, 1)
        middleFrameLayout.addWidget(self.colour_line_edit_12, yPos, 2)
        middleFrameLayout.addWidget(select_colour_button_12, yPos, 3)

    def create_bottom_frame(self):
        # Setup bottom frame
        self.bottomFrame = QFrame()
        bottomFrameLayout = QHBoxLayout(self.bottomFrame)
        bottomFrameLayout.setSpacing(1)
        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        bottomFrameLayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.save_and_accept)
        self.buttons.rejected.connect(self.reject)

    def save_and_accept(self):
        self.new_keywords = []
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_1.text())
        tmpwords.append(self.colour_line_edit_1.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_2.text())
        tmpwords.append(self.colour_line_edit_2.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_3.text())
        tmpwords.append(self.colour_line_edit_3.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_4.text())
        tmpwords.append(self.colour_line_edit_4.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_5.text())
        tmpwords.append(self.colour_line_edit_5.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_6.text())
        tmpwords.append(self.colour_line_edit_6.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_7.text())
        tmpwords.append(self.colour_line_edit_7.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_8.text())
        tmpwords.append(self.colour_line_edit_8.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_9.text())
        tmpwords.append(self.colour_line_edit_9.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_10.text())
        tmpwords.append(self.colour_line_edit_10.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_11.text())
        tmpwords.append(self.colour_line_edit_11.text())
        self.new_keywords.append(tmpwords)
        tmpwords = []
        tmpwords.append(self.keywork_line_edit_12.text())
        tmpwords.append(self.colour_line_edit_12.text())
        self.new_keywords.append(tmpwords)

        # need to check one exists
        try:
            with open('config/keywordsToHighlight.json', 'w') as outfile:
                json.dump(self.new_keywords, outfile, indent=3)
        except:
            print("Could not save list of keywords to highlight")

        self.accept()

    def on_click_colour_picker_button_1(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_1.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_1.setText(str(colour.name()).upper())

    def on_click_colourPickerButton2(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_2.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_2.setText(str(colour.name()).upper())

    def on_click_colourPickerButton3(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_3.text()), None, str("Keyword Colour Picker"))
        self.colour_line_edit_3.setText(str(colour.name()).upper())

    def on_click_colourPickerButton4(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_4.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_4.setText(str(colour.name()).upper())

    def on_click_colourPickerButton5(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_5.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_5.setText(str(colour.name()).upper())

    def on_click_colourPickerButton6(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_6.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_6.setText(str(colour.name()).upper())

    def on_click_colourPickerButton7(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_7.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_7.setText(str(colour.name()).upper())

    def on_click_colourPickerButton8(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_8.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_8.setText(str(colour.name()).upper())

    def on_click_colourPickerButton9(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_9.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_9.setText(str(colour.name()).upper())

    def on_click_colourPickerButton10(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_10.text()), None, str("Keyword Colour Picker") )
        self.colour_line_edit_10.setText(str(colour.name()).upper())

    def on_click_colourPickerButton11(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_11.text()), None, str("Keyword Colour Picker"))
        self.colour_line_edit_11.setText(str(colour.name()).upper())

    def on_click_colourPickerButton12(self):
        colour = QColorDialog.getColor(QColor(self.colour_line_edit_12.text()), None, str("Keyword Colour Picker"))
        self.colour_line_edit_12.setText(str(colour.name()).upper())
