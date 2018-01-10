#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SearchKeywordUI(QDialog):
    # Class for displaying pop-up list of keywords for the user to edit
    def __init__(self, parent):
        super(SearchKeywordUI, self).__init__(parent)
        self.setWindowTitle('Keywords')
        self.setFixedSize(250, 400)

        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()

        # Add frames to dialog screen
        dialog_frame = QFrame(self)
        dialog_frame = QVBoxLayout(dialog_frame)
        dialog_frame.addWidget(self.top_frame)
        dialog_frame.addWidget(self.middle_frame)
        dialog_frame.addWidget(self.bottom_frame)

        dialog_frame.setContentsMargins(0, 0, 0, 0)
        dialog_frame.setSpacing(0)

    def create_top_frame(self):
        # Create top frame for displaying title
        self.top_frame = QFrame()
        top_frame_layout = QVBoxLayout(self.top_frame)
        top_frame_layout.setSpacing(1)

        font = QFont()
        font.setFamily('Lucida')
        font.setFixedPitch(True)
        font.setPointSize(18)
        # font.setPixelSize(18*)

        title_label = QLabel()
        title_label.setText("    Search Keyword List")
        title_label.setStyleSheet("color: rgb(0,0,200);")
        title_label.setFont(font)
        top_frame_layout.addWidget(title_label)

    def create_middle_frame(self):
        # Create middle frame with a plain textedit widget and populate it with the
        # current list of search keywords from file

        self.middle_frame = QFrame()
        middle_frame_layout = QVBoxLayout(self.middle_frame)

        font = QFont()
        font.setFamily('Lucida')
        font.setFixedPitch(True)
        font.setPointSize(14)

        try:
            self.search_keywords_list = [line.rstrip('\n') for line in open('config/search_keywords.txt')]
        except:
            self.parent().statusBar.showMessage("Status: Could not open search keywords file")

        self.keyword_textedit = QPlainTextEdit()
        self.keyword_textedit.setFixedWidth(220)
        self.keyword_textedit.setFixedHeight(280)

        for i in self.search_keywords_list:
            self.keyword_textedit.insertPlainText(i + '\n')
        middle_frame_layout.addWidget(self.keyword_textedit)


    def create_bottom_frame(self):
        # Create bottom frame with Cancel and Save buttons

        self.bottom_frame = QFrame()
        bottom_frame_layout = QHBoxLayout(self.bottom_frame)
        bottom_frame_layout.setSpacing(1)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        bottom_frame_layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.save_and_accept)
        self.buttons.rejected.connect(self.reject)

    def save_and_accept(self):
        # Save search keywords to file and 'accept' dialog to exit
        try:
            with open('config/search_keywords.txt', 'w') as fp:
                fp.write(str(self.keyword_textedit.toPlainText()))
        except:
            self.parent().statusBar.showMessage("Status: No search line selected")
        self.accept()
