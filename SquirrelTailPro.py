#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mimetypes import MimeTypes
import sys
import re
import KeywordAndColoursDialog
import SearchKeywordsDialog
import json

LOG_TEXT_FONT = 12
SEARCH_RESULTS_FONT = 12
IGNORE_CASE = False
VERSION = "v1.0"
HIGHLIGHT_KEYWORDS = True


class Load_file_thread(QObject):
    # Thread class for loading files
    sig_step = pyqtSignal(int, str)
    sig_done = pyqtSignal(int)

    def __init__(self, id: int, fname):
        super(Load_file_thread, self).__init__()
        self.__id = id
        self.fname=fname

    def work(self):
        # Open log file, read a chunk of data and emit data back
        with open(self.fname, 'r', encoding="ISO-8859-1") as f:
            while True:
                chunk = f.read(1000000)
                if not chunk:
                    break
                self.sig_step.emit(self.__id, str(chunk))
                app.processEvents()

        self.sig_done.emit(self.__id)


class Highlight_lines_thread(QObject):
    # Thread class for highlighting lines with matching keywords
    sig_step = pyqtSignal(int, str, int)
    sig_done = pyqtSignal(int)

    def __init__(self, id: int, logFile, keywords):
        super(Highlight_lines_thread, self).__init__()
        self.__id = id
        self.logFile=logFile
        self.keywords=keywords

    def work(self):
        # Check each line for a match aginst the list of keywords.  If there is a match
        # emit the line and required highlight colour back else emit the line with no
        # highlight colour back
        self.block = self.logFile.begin()
        for i in range(0, self.logFile.blockCount()):
            linesOfText = str(self.block.text())
            if HIGHLIGHT_KEYWORDS:
                # Loop though the keywords in reverse order so the highest priority keyword is applied last
                for j in range(len(self.keywords)-1, -1, -1):
                    keyword = self.keywords[j][0]
                    colour = self.keywords[j][1]
                    if keyword != "":
                        if re.findall(keyword, linesOfText):
                            self.sig_step.emit(self.__id, colour, i)
            else:
                self.sig_step.emit(self.__id, "#FFFFFF", i)
            app.processEvents()
            self.block = self.block.next()

        self.sig_done.emit(self.__id)


class Search_thread(QObject):
    # Thread class for searching log file
    sig_step = pyqtSignal(int, str, str)
    sig_done = pyqtSignal(int)

    def __init__(self, id: int, doc, search_string):
        super(Search_thread, self).__init__()
        self.__id = id
        self.search_string=search_string
        self.doc=doc

    def work(self):
        block = self.doc.begin()
        line_number = 0

        for i in range(0, self.doc.blockCount()):
            # Format line numbers so lines line up
            line_number += 1
            if line_number <= 9:
                line_number_string = "    " + str(line_number) + ": "
            elif line_number <= 99:
                line_number_string = "   " + str(line_number) + ": "
            elif line_number <= 999:
                line_number_string = "  " + str(line_number) + ": "
            elif line_number <= 9999:
                line_number_string = " " + str(line_number) + ": "
            else:
                line_number_string = "" + str(line_number) + ": "

            lines_of_text = str(block.text())

            # Search line of text to see if it contains the search string and if it does
            # emit the line number and line of text
            if IGNORE_CASE == True:
                if re.findall(self.search_string, lines_of_text, re.IGNORECASE):
                    self.sig_step.emit(self.__id, line_number_string, lines_of_text)
            else:
                if re.findall(self.search_string, lines_of_text):
                    self.sig_step.emit(self.__id, line_number_string, lines_of_text)

            block = block.next()
        app.processEvents()

        self.sig_done.emit(self.__id)


class SquirrelTailPro(QMainWindow):
    def __init__(self):
        super(SquirrelTailPro, self).__init__()
        self.enable_drag_drop = True
        self.init_ui()

    def init_ui(self):
        self.configure_menu_action()
        self.create_menus()
        self.create_tool_bar()
        self.create_status_bar()

        # Allow drag and drop
        self.setAcceptDrops(True)

        # Setup main_frame as central widget
        self.main_frame = main_frame(self)
        self.setCentralWidget(self.main_frame)

        # Configure main window geometory
        self.setGeometry(50, 50, 1300, 600)
        self.setWindowTitle('SquirrelTailPro ' + VERSION)
        self.show()

    def create_menus(self):
        # Set setNativeMenuBar to false so the menu on the Mac is in the app and
        # not at top of screen
        self.menuBar().setNativeMenuBar(False)
        self.file_menu = self.menuBar().addMenu('File')
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        self.file_menu = self.menuBar().addMenu('Edit')
        self.file_menu.addAction(self.copy_action)
        self.file_menu.addAction(self.paste_action)
        self.file_menu = self.menuBar().addMenu('Help')
        self.file_menu.addAction(self.about_action)

    def configure_menu_action(self):
        # Assign actions to menu and toolbar items
        self.open_file_action = QAction(QIcon('icons/openFile-icon2.png'), 'Open', self, shortcut="Ctrl+O", triggered=self.open_file)
        self.copy_action = QAction(QIcon('icons/copy-icon.png'), '&Copy', self, shortcut="Ctrl+C", triggered=self.copy)
        self.paste_action = QAction(QIcon('icons/paste-icon.png'), 'Paste', self, shortcut="Ctrl+V", triggered=self.paste)
        self.highlight_action = QAction(QIcon('icons/highlighter(on).png'), 'Highlight', self, triggered=self.highlight_text)
        self.colour_picker_action = QAction(QIcon('icons/Color-icon5.png'), 'Colour Picker', self, triggered=self.select_keyword_and_colours)
        self.search_keywords_action = QAction(QIcon('icons/keyword_search_4.png'), 'Search Keywords', self, triggered=self.search_keywords)
        self.font_bigger_action = QAction(QIcon('icons/fontBigger-icon.png'), 'Bigger Font', self, triggered=self.font_bigger)
        self.font_smaller_action = QAction(QIcon('icons/fontSmaller-icon.png'), 'Smaller Font', self, triggered=self.font_smaller)
        self.exit_action = QAction(QIcon('icons/close-icon.png'), 'Quit', self, shortcut="Ctrl+Q", triggered=self.quit)
        self.about_action = QAction(QIcon('icons/squirrel-icon-2.png'), 'About SquirrelTailPro', self, triggered=self.about)
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_tool_bar(self):
        # Setup toolbar and add items to it
        toolbar = self.addToolBar('')
        toolbar.addAction(self.open_file_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addAction(self.highlight_action)
        toolbar.addAction(self.colour_picker_action)
        toolbar.addAction(self.search_keywords_action)
        toolbar.addAction(self.font_bigger_action)
        toolbar.addAction(self.font_smaller_action)
        toolbar.addAction(self.exit_action)
        toolbar.addAction(self.about_action)

    def create_status_bar(self):
        # Setup status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Status: OK")

    def updateText(self, data):
        self.main_frame.log_text_edit.insertPlainText(data)

    def copy(self):
        # As there are two places the user may be copying from we need to first get the focused
        # widget and then copy text from the appropriate textedit widget
        focused_text_edit_widget = self.focusWidget().objectName()
        if focused_text_edit_widget == "search_results_textedit":
            self.main_frame.search_results_textedit.copy()
        else:
            self.main_frame.log_text_edit.copy()

    def paste(self):
        # The only place to paste data on the main window is the 'Search Text Box' so we
        # always paste the data there
        self.main_frame.search_text_box.paste()

    def font_bigger(self):
        # Increase the text size in the main log window
        global LOG_TEXT_FONT
        if LOG_TEXT_FONT < 20:
            LOG_TEXT_FONT = LOG_TEXT_FONT + 1
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(LOG_TEXT_FONT)
        self.main_frame.log_text_edit.setFont(font)

    def font_smaller(self):
        # Decrease the text size in the main log window
        global LOG_TEXT_FONT
        if LOG_TEXT_FONT > 4:
            LOG_TEXT_FONT = LOG_TEXT_FONT - 1
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(LOG_TEXT_FONT)
        self.main_frame.log_text_edit.setFont(font)

    def about(self):
        QMessageBox.about(self, "About SquirrelTailPro",
                                "SquirrelTailPro is a log viewer written\n"
                                "in Python3 and Qt5.  It is based on the\n"
                                "popular but Windows only BareTailPro\n"
                                "application.\n")

    def disable_gui_widgets(self):
        self.highlight_action.setDisabled(True)
        self.open_file_action.setDisabled(True)
        self.colour_picker_action.setDisabled(True)
        self.search_keywords_action.setDisabled(True)
        self.main_frame.search_button.setDisabled(True)

    def enable_gui_widgets(self):
        self.highlight_action.setEnabled(True)
        self.open_file_action.setEnabled(True)
        self.colour_picker_action.setEnabled(True)
        self.search_keywords_action.setEnabled(True)
        self.main_frame.search_button.setEnabled(True)

    def closeEvent(self, event):
        # Catch when the user selects the close icon and ask for conformation
        reply = QMessageBox.question(self, 'Message', "Are you sure?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def quit(self):
        # Main quit function called when user selects quit from menu or selects the quit icon
        reply = QMessageBox.question(self, 'Message', "Are you sure?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QCoreApplication.quit()
        else:
            self.statusBar.showMessage("Status: OK")

    def open_file(self):
        # Main function for opening files
        fname = QFileDialog.getOpenFileName(self, 'Open file', '')

        if fname[0]:
            self.main_frame.log_text_edit.setPlainText("")
            try:
                f = open(fname[0], 'r', encoding="ISO-8859-1")
                if fname[0]:
                    self.statusBar.showMessage("Status: Loading.")

                    # Disable buttons and drap&drop function while loading file
                    self.disable_gui_widgets()
                    self.enable_drag_drop = False

                    self.__threads = []
                    file_worker = Load_file_thread(1, fname[0])
                    thread = QThread()
                    thread.setObjectName('thread_')
                    self.__threads.append((thread, file_worker)) # Seem to need double brackets
                    file_worker.moveToThread(thread)

                    # get progress messages from file worker:
                    file_worker.sig_step.connect(self.on_file_worker_step)
                    file_worker.sig_done.connect(self.on_file_worker_done)

                    thread.started.connect(file_worker.work)
                    thread.start()
            except:
                self.statusBar.showMessage("Status: Could not open file")

        # Set window title to name of log file
        self.setWindowTitle('SquirrelTailPro : ' + fname[0])

    def dragEnterEvent(self, event):
        if self.enable_drag_drop:
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                event.acceptProposedAction()
        else:
            self.statusBar.showMessage("Status: Busy with current file. Please try later.")

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        # get filename of file that wants to be dropped
        file_to_drop = urls[0].toLocalFile()

        # get mime type
        mime = MimeTypes()
        file_mime_type = mime.guess_type(file_to_drop)
        mime_type = str(file_mime_type[0])

        # check if it has a type
        if (mime_type != "None"):
            app_type = mime_type.split('/')
            type = app_type[0]
            sub_type = app_type[1]

            if ((type == 'text') | (sub_type == 'xml')):

                if (urls and urls[0].scheme() == 'file'):
                    # for some reason, this doubles up the intro slash
                    fname = "/" + str(urls[0].path())[1:]

                    # Clear old file contents from log_text_edit
                    self.main_frame.log_text_edit.setPlainText("")
                    if fname:
                        try:
                            f = open(fname, 'r', encoding="ISO-8859-1")
                            if fname[0]:
                                self.statusBar.showMessage("Status: Loading.")

                                # Disable buttons and drap&drop function while loading file
                                self.disable_gui_widgets()
                                self.enable_drag_drop = False

                                self.__threads = []
                                file_worker = Load_file_thread(1, fname)
                                thread = QThread()
                                thread.setObjectName('thread_')
                                self.__threads.append((thread, file_worker))  # Seem to need double brackets
                                file_worker.moveToThread(thread)

                                # get progress messages from file worker:
                                file_worker.sig_step.connect(self.on_file_worker_step)
                                file_worker.sig_done.connect(self.on_file_worker_done)

                                thread.started.connect(file_worker.work)
                                thread.start()  # this will emit 'started' and start thread's event loop
                        except:
                            self.statusBar.showMessage("Status: You do not have permission to read log file")

                    # Set window title to name of log file
                    self.setWindowTitle('SquirrelTailPro : ' + fname)
            else:
                self.statusBar.showMessage("Status: Error - Not a valid file type")
        else:
            self.statusBar.showMessage("Status: Error - Not a valid file type")

    def on_file_worker_step(self, worker_id: int, data: str):
        self.main_frame.log_text_edit.insertPlainText(str(data))
        self.statusBar.showMessage(self.statusBar.currentMessage() + ".")


    def on_file_worker_done(self, worker_id):
        self.statusBar.showMessage("Status: OK")
        for thread, file_worker in self.__threads:
            thread.quit()
            thread.wait()
        # Enable button and drag&drop function
        self.enable_gui_widgets()
        self.enable_drag_drop = True

        if HIGHLIGHT_KEYWORDS:
            self.highlight_lines_with_keywords()

    def highlight_lines_with_keywords(self):
        self.load_keywords()
        self.highlightKeywordLines()
        self.saveKeywords()

    def highlight_text(self):
        global HIGHLIGHT_KEYWORDS
        if HIGHLIGHT_KEYWORDS:
            HIGHLIGHT_KEYWORDS = False
            self.highlight_action.setIcon(QIcon('icons/highlighter(off).png'))
        else:
            HIGHLIGHT_KEYWORDS = True
            self.highlight_action.setIcon(QIcon('icons/highlighter(on).png'))

        self.highlight_lines_with_keywords()

    def highlightKeywordLines(self):
        global HIGHLIGHT_KEYWORDS
        self.logFile = self.main_frame.log_text_edit.document()
        self.format = QTextBlockFormat()

        if HIGHLIGHT_KEYWORDS:
            self.statusBar.showMessage("Status: Highlighting lines with matching keywords")
        else:
            self.statusBar.showMessage("Status: Removing Highlighting from lines")

        # Disable buttons and drap&drop function while highlighting
        self.disable_gui_widgets()
        self.enable_drag_drop = False

        self.__threads = []
        highlight_worker = Highlight_lines_thread(1, self.logFile, self.keywords)
        thread = QThread()
        thread.setObjectName('thread_')
        self.__threads.append((thread, highlight_worker))  # Seem to need double brackets
        highlight_worker.moveToThread(thread)

        # get progress messages from file highlight worker:
        highlight_worker.sig_step.connect(self.on_highlight_worker_step)
        highlight_worker.sig_done.connect(self.on_highlight_worker_done)

        thread.started.connect(highlight_worker.work)
        thread.start()  # this will emit 'started' and start thread's event loop

    def on_highlight_worker_step(self, worker_id: int, colour: str, i: int):
        self.format.setBackground(QColor(colour))
        lineOfText = QTextCursor(self.main_frame.log_text_edit.document().findBlockByNumber(i))
        lineOfText.setBlockFormat(self.format)

    def on_highlight_worker_done(self, worker_id):
        self.statusBar.showMessage("Status: OK")
        for thread, highlight_worker in self.__threads:
            thread.quit()
            thread.wait()
        # Enable button and drag&drop function now highlighting has completed
        self.enable_gui_widgets()
        self.enable_drag_drop = True

    def search_keywords(self):
        self.statusBar.showMessage("Status: Search Keywords")
        dlg = SearchKeywordsDialog.SearchKeywordUI(self)
        dlg.exec_()
        self.load_search_keywords()
        self.main_frame.populate_combobox_search_keywords()

    def load_keywords(self):
        try:
            with open('config/keywordsToHighlight.json', 'r') as json_file:
                self.keywords = json.load(json_file)
        except:
            self.statusBar.showMessage("Status: Could not open file containing Keywords to Highlight")

    def saveKeywords(self):
        try:
            with open('config/keywordsToHighlight.json', 'w') as outfile:
                json.dump(self.keywords, outfile, indent=3)
        except:
            self.statusBar.showMessage("Status: Error - Could not save keywords")

    def select_keyword_and_colours(self):
        dlg = KeywordAndColoursDialog.KeywordAndColoursUI(self)
        dlg.exec_()
        self.highlight_action.setIcon(QIcon('icons/highlighter(on).png'))
        self.highlight_lines_with_keywords()

    def load_search_keywords(self):
        self.search_keywords_list = []
        try:
            self.search_keywords_list = [line.rstrip('\n') for line in open('config/search_keywords.txt')]
        except:
            self.statusBar.showMessage("Status: Search Keywords file does not exist")


class main_frame(QWidget):
    def __init__(self, parent):
        super(main_frame, self).__init__(parent)
        # Setup frame for search bar.  This will search button, keyword search input, font size button etc.
        search_bar_frame = QFrame()
        search_bar_frame.setFrameShape(QFrame.StyledPanel)
        search_bar_frame.setFrameShadow(QFrame.Raised)

        # Create search button
        self.search_button = QToolButton()
        self.search_button.setText('Search')
        self.search_button.setStyleSheet("font-size:14px")
        self.search_button.clicked.connect(self.on_click_search_button)

        # Create search input text field
        self.search_text_box = QLineEdit()

        # Create and populate keyword combobox
        self.keyword_combobox = QComboBox(self)
        self.keyword_combobox.activated[str].connect(self.on_activated_keyword_combobox)
        self.populate_combobox_search_keywords()

        # Create checkbox
        self.ignore_case_checkbox = QCheckBox('ignore case ', self)
        self.ignore_case_checkbox.stateChanged.connect(self.change_title)

        # Create font size buttons
        search_frame_bigger_font_button = QToolButton()
        search_frame_bigger_font_button.setText('A+')
        search_frame_bigger_font_button.setStyleSheet("font-size:14px")
        search_frame_bigger_font_button.clicked.connect(self.on_click_bigger_font_button)
        search_frame_smaller_font_button = QToolButton()
        search_frame_smaller_font_button.setText('A-')
        search_frame_smaller_font_button.setStyleSheet("font-size:12px")
        search_frame_smaller_font_button.clicked.connect(self.on_click_smaller_font_button)

        # Add search button, keyword input field, keyword combobox and font size buttons to search bar frame
        search_bar_layout = QHBoxLayout(search_bar_frame)
        search_bar_layout.setContentsMargins(4, 5, 5, 0)
        search_bar_layout.setSpacing(3)
        search_bar_layout.addWidget(self.search_button)
        search_bar_layout.addWidget(self.search_text_box)
        search_bar_layout.addWidget(self.ignore_case_checkbox)
        search_bar_layout.addWidget(self.keyword_combobox)
        search_bar_layout.addWidget(search_frame_bigger_font_button)
        search_bar_layout.addWidget(search_frame_smaller_font_button)

        # Setup frame for search results
        self.search_results_textedit = QPlainTextEdit()
        self.search_results_textedit.setObjectName("search_results_textedit")

        self.search_results_textedit.setWordWrapMode(False)
        self.search_results_textedit.setReadOnly(True)
        self.search_results_textedit.setShortcutEnabled(True)
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(SEARCH_RESULTS_FONT)
        self.search_results_textedit.setFont(font)
        # Setup callback for when user select a line from the search results
        self.search_results_textedit.selectionChanged.connect(self.search_results_selection_changed)

        # Setup search frame and add the search frame bar and search results frame to it
        search_frame = QFrame()
        search_frame.setFrameShape(QFrame.NoFrame)
        search_frame_vertical_box_layout = QVBoxLayout(search_frame)
        search_frame_vertical_box_layout.setContentsMargins(0, 0, 0, 0)
        search_frame_vertical_box_layout.setSpacing(0)
        search_frame_vertical_box_layout.addWidget(search_bar_frame)
        search_frame_vertical_box_layout.addWidget(self.search_results_textedit)

        # Create the main logfile text view
        self.log_text_edit = QPlainTextEdit()
        self.log_text_edit.setObjectName("log_text_edit")
        self.log_text_edit.setWordWrapMode(False)
        self.log_text_edit.setReadOnly(True)
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.log_text_edit.setFont(font)

        self.load_splash_screen()

        # Create a vertical split view frame and add the main log view and search frames to it
        main_frame_vertical_splitter = QSplitter(Qt.Vertical)
        main_frame_vertical_splitter.addWidget(self.log_text_edit)
        main_frame_vertical_splitter.addWidget(search_frame)
        main_frame_vertical_splitter.setSizes([200, 100])

        # Add the vertical split frame as the center widget of the application window
        window_vertical_box_layout = QVBoxLayout(self)
        self.setLayout(window_vertical_box_layout)
        window_vertical_box_layout.addWidget(main_frame_vertical_splitter)
        window_vertical_box_layout.setContentsMargins(1, 0, 1, 0)
        window_vertical_box_layout.setSpacing(0)

    def change_title(self, state):
        global IGNORE_CASE
        if state == Qt.Checked:
            IGNORE_CASE = True
        else:
            IGNORE_CASE = False

    def populate_combobox_search_keywords(self):
        self.search_keywords_list = []
        try:
            self.search_keywords_list = [line.rstrip('\n') for line in open('config/search_Keywords.txt')]
            self.keyword_combobox.clear()
            for i in range(len(self.search_keywords_list)):
                self.keyword_combobox.addItem(self.search_keywords_list[i])
        except:
            print("config/search_Keywords.txt does not exist")

    def on_activated_keyword_combobox(self, text):
        # Add the selected keyword to the current search string, adding a '|' before any existing
        # values to preserve regex syntax
        if self.search_text_box.text() == "":
            self.search_text_box.setText(text)
        else:
            self.search_text_box.setText(self.search_text_box.text() + "|" + text)

    def on_click_search_button(self):
        global IGNORE_CASE
        self.parent().statusBar.showMessage("Status: Searching...")
        search_string = self.search_text_box.text()

        # If search string is a valid regex expression then search for string in log file
        try:
            re.compile(search_string)
            self.parent().disable_gui_widgets()

            # Clear current search results window
            self.search_results_textedit.setPlainText("")

            # Read the contents of the log file a block (line) at a time
            doc = self.log_text_edit.document()
            self.__threads = []
            search_worker = Search_thread(1, doc, search_string)
            thread = QThread()
            thread.setObjectName('thread_')
            self.__threads.append((thread, search_worker))  # Seem to need double brackets
            search_worker.moveToThread(thread)

            # get progress messages from file highlight worker:
            search_worker.sig_step.connect(self.on_search_worker_step)
            search_worker.sig_done.connect(self.on_search_worker_done)

            thread.started.connect(search_worker.work)
            thread.start()  # this will emit 'started' and start thread's event loop

            self.parent().statusBar.showMessage("Status: OK")

        except re.error:
            self.parent().statusBar.showMessage("Status: Search term in not valid regex")

    def on_search_worker_step(self, worker_id: int, line_number: str, result: str):
        self.search_results_textedit.insertPlainText(line_number + result + "\n")
        self.parent().statusBar.showMessage("Status: Searching...")

    def on_search_worker_done(self, worker_id):
        self.parent().statusBar.showMessage("Status: OK")
        for thread, highlight_worker in self.__threads:
            thread.quit()
            thread.wait()
        self.parent().enable_gui_widgets()

    def on_click_bigger_font_button(self):
        global SEARCH_RESULTS_FONT
        if SEARCH_RESULTS_FONT < 20:
            SEARCH_RESULTS_FONT = SEARCH_RESULTS_FONT + 1
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(SEARCH_RESULTS_FONT)
        self.search_results_textedit.setFont(font)

    def on_click_smaller_font_button(self):
        global SEARCH_RESULTS_FONT
        if SEARCH_RESULTS_FONT > 4:
            SEARCH_RESULTS_FONT = SEARCH_RESULTS_FONT - 1
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(SEARCH_RESULTS_FONT)
        self.search_results_textedit.setFont(font)

    def search_results_selection_changed(self):
        # Check if search button is enabled so we only allow the search results to be
        # selected once the search is completed
        if self.search_button.isEnabled():
            # Get the line of text for selected line
            text_cursor = self.search_results_textedit.textCursor()
            block_number_at_cursor = text_cursor.blockNumber()
            doc = self.search_results_textedit.document()
            block = doc.findBlockByNumber(block_number_at_cursor)
            block_of_text = block.text()

            if block_of_text != "":
                # If line of text is not empty, extract the real line number from start of line
                line_number = int(str(block_of_text).split(":")[0].strip())
                # Move the cursor in the main log view the the selected line
                self.log_text_edit.moveCursor(QTextCursor.End)
                cursor = QTextCursor(self.log_text_edit.document().findBlockByLineNumber(line_number-1))
                self.log_text_edit.setTextCursor(cursor)
            else:
                self.parent().statusBar.showMessage("Status: No search line selected")

    def load_splash_screen(self):
        try:
            f = open('config/splash_screen.txt', 'r', encoding="ISO-8859-1")
            with f:
                data = f.read()
                self.log_text_edit.insertPlainText(data)
        except:
            self.log_text_edit.insertPlainText("")

# Entry point for application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SquirrelTailPro()
    sys.exit(app.exec_())
