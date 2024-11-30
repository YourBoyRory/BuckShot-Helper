import sys
import random
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QLineEdit, QPushButton, QGridLayout

class NumberSelectorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        if random.randint(0, 9) == 0:
            self.setWindowTitle('BackShot Helper')
        else:
            self.setWindowTitle('BuckShot Helper')
        self.setGeometry(100, 100, 200, 200)  # Adjusted size to fit buttons
        self.setMaximumSize(500, 300)

        # Create the main layout
        main_layout = QVBoxLayout()
        self.removed_from_order = ""
        
        # Create Lives section
        lives_layout = QHBoxLayout()
        lives_label = QLabel('Lives:')
        self.lives_spinbox = QSpinBox()
        self.lives_spinbox.setRange(0, 10)  # Set range of lives between 0 and 10
        self.lives_spinbox.setValue(0)  # Default value for Lives
        self.lives_spinbox.valueChanged.connect(self.on_spinbox_value_changed)
        self.lives_spinbox.setMinimumHeight(40)
        self.lives_spinbox.setStyleSheet("font-size: 16px;")
        lives_layout.addWidget(lives_label)
        lives_layout.addWidget(self.lives_spinbox)
        self.last_lives_value = self.lives_spinbox.value()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
            
        # Create Blanks section
        blanks_layout = QHBoxLayout()
        blanks_label = QLabel('Blanks:')
        self.blanks_spinbox = QSpinBox()
        self.blanks_spinbox.setRange(0, 10)  # Set range of blanks between 0 and 10
        self.blanks_spinbox.setMinimumHeight(40)
        self.blanks_spinbox.setStyleSheet("font-size: 16px;")
        self.blanks_spinbox.setValue(0)  # Default value for Blanks
        self.blanks_spinbox.valueChanged.connect(self.on_spinbox_value_changed)
        blanks_layout.addWidget(blanks_label)
        blanks_layout.addWidget(self.blanks_spinbox)
        self.last_blanks_value = self.blanks_spinbox.value()

        # Create Button Grid (10 buttons side by side)
        button_layout = QGridLayout()
        self.buttons = []
        for i in range(10):
            button = QPushButton(" ")
            button.setDisabled(True)
            button.setMinimumWidth(40)
            button.clicked.connect(lambda _, i=i: self.on_button_click(i))
            self.buttons.append(button)
            button_layout.addWidget(button, 0, i)

        clear_button = QPushButton('Clear')
        clear_button.setStyleSheet("font-size: 16px;")
        clear_button.clicked.connect(self.clear)

        # Add layouts to the main layout
        main_layout.addLayout(lives_layout)
        main_layout.addLayout(blanks_layout)
        main_layout.addLayout(button_layout)  # Add the buttons grid
        main_layout.addWidget(clear_button)  # Add clear button

        # Set the main layout of the window
        self.setLayout(main_layout)

    def getAssetPath(self, file):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, 'assets', file)

    def clear(self):
        self.lives_spinbox.setValue(0)
        self.blanks_spinbox.setValue(0)

    def on_button_click(self, button_index):
        button = self.buttons[button_index]
        if button.text() == "#":
            self.set_button_letter(button, "L")
        elif button.text() == "L":
            self.set_button_letter(button, "B")
        else:
            self.set_button_letter(button, "#")
            
            
    def set_button_letter(self, button, letter):
        button.setText(letter)
        if letter == "L":
            button.setStyleSheet("color: #d47273; font-size: 16px;")
        elif letter == "B":
            button.setStyleSheet("color: #72a4d4; font-size: 16px;")
        else:
            button.setStyleSheet("color: grey; font-size: 16px;")
        
    def get_string_from_button(self):
        order=""
        for button in self.buttons:
            text = button.text()
            if text != " ":
                order += button.text()
        return order
        
    def set_buttons_from_string(self, order):
        #print(order)
        i = 0
        for button in self.buttons:
            if i < len(order) and len(order) != 0:
                button.setDisabled(False)
                self.set_button_letter(button, order[i])
            else:
                button.setDisabled(True)
                self.set_button_letter(button, " ")
            i+=1

    def convert_to_uppercase(self):
        text = self.text_box.text()
        if text == "":
            self.font.setLetterSpacing(QFont.PercentageSpacing, 100) 
        else:
            self.text_box.setText(text.upper()) 
            self.font.setLetterSpacing(QFont.PercentageSpacing, 150)  # Increase letter spacing by 150%
        self.text_box.setFont(self.font)
        
    def on_spinbox_value_changed(self):
        # Get the current values of Lives and Blanks
        lives_value = self.lives_spinbox.value()
        blanks_value = self.blanks_spinbox.value()
        possible_shells = 10 - (lives_value + blanks_value)
        if possible_shells == 0:
            self.lives_spinbox.setMaximum(lives_value)
            self.blanks_spinbox.setMaximum(blanks_value)
        else:
            self.lives_spinbox.setMaximum(10)
            self.blanks_spinbox.setMaximum(10)
        known_order = self.get_string_from_button()
        if abs(lives_value - self.last_lives_value) > 1:
            change_amount = abs(lives_value - self.last_lives_value)
        elif abs(blanks_value - self.last_blanks_value) > 1:
            change_amount = abs(blanks_value - self.last_blanks_value)
        else:
            change_amount =  1

        if lives_value < self.last_lives_value or blanks_value < self.last_blanks_value:
            for i in range(change_amount):
                self.removed_from_order = known_order[:1] + self.removed_from_order
                #print(self.removed_from_order)
                known_order = known_order[1:]
        else:
            for i in range(change_amount):
                if self.removed_from_order != "":
                    known_order = self.removed_from_order[:1] + known_order
                    self.removed_from_order = self.removed_from_order[1:]
                else:
                    known_order = '#' + known_order
            #print(self.removed_from_order)
        self.set_buttons_from_string(known_order)
        self.last_lives_value = self.lives_spinbox.value()
        self.last_blanks_value = self.blanks_spinbox.value()
        if lives_value == 0 and blanks_value == 0:
            print("New Round")
            self.removed_from_order = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NumberSelectorApp()
    window.show()
    sys.exit(app.exec_())


