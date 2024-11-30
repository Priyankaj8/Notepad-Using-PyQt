from PyQt6.QtWidgets import QApplication, QTextEdit,QMainWindow, QMenuBar, QMenu, QFileDialog, QInputDialog 
import sys
from PyQt6.QtGui import QAction, QTextCursor, QColor
from PyQt6.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.count = 0
        self.setWindowTitle("Notepad")
        self.setGeometry(0,0,300,200)

        self.current_file = None

        # Creating the text field
        self.edit_field =  QTextEdit(self)
        self.setCentralWidget(self.edit_field)

        # Creating a menubar
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        # Creating a file menu
        fileMenu = QMenu("File",self)
        menubar.addMenu(fileMenu)

        #Creating actions for file menu
        new_action = QAction("New",self)
        fileMenu.addAction(new_action)
        new_action.triggered.connect(self.new_file)

        open_action = QAction("Open",self)
        fileMenu.addAction(open_action)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save",self)
        fileMenu.addAction(save_action)
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction("Save As",self)
        fileMenu.addAction(save_as_action)
        save_as_action.triggered.connect(self.save_file_as)

        # Creating the Edit menu
        editMenu = QMenu("Edit",self)
        menubar.addMenu(editMenu)

        # Creating actions for the edit menu
        undo_action = QAction("Undo",self)
        editMenu.addAction(undo_action)
        # in-built undo,redo,cut,copy,paste method for QTextEdit class
        undo_action.triggered.connect(self.edit_field.undo) 

        redo_action = QAction("Redo",self)
        editMenu.addAction(redo_action)
        redo_action.triggered.connect(self.edit_field.redo)

        cut_action = QAction("Cut",self)
        editMenu.addAction(cut_action)
        cut_action.triggered.connect(self.edit_field.cut)

        copy_action = QAction("Copy",self)
        editMenu.addAction(copy_action)
        copy_action.triggered.connect(self.edit_field.copy)

        paste_action = QAction("Paste",self)
        editMenu.addAction(paste_action)
        paste_action.triggered.connect(self.edit_field.paste)

        find_action = QAction("Find",self)
        editMenu.addAction(find_action)
        find_action.triggered.connect(self.find_text)

    def new_file(self):
        self.edit_field.clear()
        self.current_file = None

    def open_file(self):
        file_path,_ = QFileDialog.getOpenFileName(self,"Open File","","All Files(*);;Python Files(*.py)")
        with open(file_path,"r") as file:
            text = file.read()
            self.edit_field.setText(text)

    def save_file_as(self):
        file_path , _ = QFileDialog.getSaveFileName(self,"Save File","","All Files(*);;Python File(*.py)")
        if file_path:
            with open(file_path,"w")as file:
                file.write(self.edit_field.toPlainText())
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            with open(self.current_file,"w")as file:
                file.write(self.edit_field.toPlainText())
        else:
            self.save_file_as()

    def find_text(self):
        search_text, ok = QInputDialog.getText(self,"Find text","Search for")
        if ok:
            all_words = []
            self.edit_field.moveCursor(QTextCursor.MoveOperation.Start)
            highlight_color = QColor(Qt.GlobalColor.yellow)

            while(self.edit_field.find(search_text)):
                # creating the selection for search_text
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(highlight_color)

                selection.cursor = self.edit_field.textCursor()
                all_words.append(selection)
            self.edit_field.setExtraSelections(all_words)
        

app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())