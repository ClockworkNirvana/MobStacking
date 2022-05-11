import sys
import csv

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)


# adds b string to QLabel a with \n seperator
def adder(a, b):
    if a.text():
        a.setText(a.text() + "\n" + b)
    else:
        a.setText(b)


# list to string with \n seperator
def l_2_s(x):
    a = ''
    for thing in x:
        a = f"{a}\n{thing}"
    a = a[1:]
    return a


# create list from 1 to n
def create_list(n):
    lst = []
    for i in range(n):
        lst.append(i + 1)
    return lst


class Dialog(QDialog):

    def __init__(self):
        super().__init__()

        # editor box for adding and removing layers
        self.editor_box = QGroupBox()
        self.editor_box.setFlat(True)
        editor_layout = QGridLayout()
        # import mobs data
        with open('mobs.csv') as data:
            reader = csv.reader(data)
            mobs = []
            for row in reader:
                for item in row:
                    mobs.append(item)
        # left side adding layers
        self.editor_mob_label = QLabel("Mob")
        self.mob_edit = QComboBox()
        self.mob_edit.addItems(mobs)
        self.num_label = QLabel("Number")
        self.num_edit = QLineEdit()

        editor_layout.addWidget(self.editor_mob_label, 0, 0)
        editor_layout.addWidget(self.mob_edit, 0, 1)
        editor_layout.addWidget(self.num_label, 1, 0)
        editor_layout.addWidget(self.num_edit, 1, 1)
        # right side removing layers
        self.editor_level_label = QLabel("level")
        self.level_edit = QComboBox()

        editor_layout.addWidget(self.editor_level_label, 0, 2, 2, 1)
        editor_layout.addWidget(self.level_edit, 0, 3, 2, 1)
        # add and remove buttons
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")

        editor_layout.addWidget(self.add_button, 2, 0, 1, 2)
        editor_layout.addWidget(self.remove_button, 2, 2, 1, 2)
        # box scaling and set layout
        editor_layout.setColumnStretch(1, 10)
        editor_layout.setColumnStretch(3, 10)

        self.editor_box.setLayout(editor_layout)

        # display box for saved layers
        self.display_box = QGroupBox()
        self.display_box.setFlat(True)
        display_layout = QGridLayout()
        # headers
        display_layout.addWidget(QLabel("Level"), 0, 0)
        display_layout.addWidget(QLabel("Mob"), 0, 1)
        display_layout.addWidget(QLabel("Height"), 0, 2)
        # for displaying saved data
        self.level_label = QLabel()
        self.mobs_label = QLabel()
        self.height_label = QLabel()
        self.level_label.setAlignment(Qt.AlignCenter)
        self.mobs_label.setAlignment(Qt.AlignCenter)
        self.height_label.setAlignment(Qt.AlignCenter)

        display_layout.addWidget(self.level_label, 1, 0)
        display_layout.addWidget(self.mobs_label, 1, 1)
        display_layout.addWidget(self.height_label, 1, 2)

        self.display_box.setLayout(display_layout)

        # generator box for generate button, output and copy to clipboard
        self.generate_box = QGroupBox()
        self.generate_box.setFlat(True)
        generate_layout = QGridLayout()

        self.generate_button = QPushButton("Generate")
        self.output = QLabel()
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setWordWrap(True)
        self.clipboard = QPushButton("Copy to Clipboard")

        generate_layout.addWidget(self.generate_button, 0, 0)
        generate_layout.addWidget(self.output, 1, 0)
        generate_layout.addWidget(self.clipboard, 2, 0)

        self.generate_box.setLayout(generate_layout)

        # Ok and Cancel buttons at bottom of page
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # on click event handlers
        self.add_button.clicked.connect(self.add_level)
        self.remove_button.clicked.connect(self.remove_level)
        self.generate_button.clicked.connect(self.generate)
        self.clipboard.clicked.connect(self.copy)

        # main layouts of dialog window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.editor_box)
        main_layout.addWidget(self.display_box)
        main_layout.addWidget(self.generate_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Mob Stack Editor")

    def add_level(self):
        # adds layer from editor into display
        # checks if value in the number box is an integer
        if self.num_edit.text().isdigit():
            # adds data in the editor boxes into the display box
            adder(self.mobs_label, self.mob_edit.currentText())
            adder(self.height_label, self.num_edit.text())
            # increment level value by 1
            if self.level_label.text():
                self.level_label.setText(self.level_label.text() + "\n" + str(int(self.level_label.text()[-1]) + 1))
            else:
                self.level_label.setText("1")
            # add 1 level to the removal QCombobox
            self.level_edit.addItem(self.level_label.text()[-1])
        # if value in number box is not integer, prompt a warning box
        else:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Error")
            error.setInformativeText("Value input into number of mobs is not an integer")
            error.setWindowTitle("Value Error")
            error.exec()

    def remove_level(self):
        # removes previously saved layer
        # level to be deleted
        deleted = int(self.level_edit.currentText()) - 1
        # change strings in storage to lists
        layer_mob = self.mobs_label.text().split("\n")
        layer_num = [int(x) for x in self.height_label.text().split("\n")]
        # set layer numbers down by 1 by creating a list with 1 fewer elements
        layer_index = create_list(len(self.level_label.text().split("\n")) - 1)
        # delete layers
        del layer_mob[deleted]
        del layer_num[deleted]
        # write edited data back to display box
        self.mobs_label.setText(l_2_s(layer_mob))
        self.height_label.setText(l_2_s(layer_num))
        self.level_label.setText(l_2_s(layer_index))
        # reset the removal QComboBox
        self.level_edit.clear()
        self.level_edit.addItems(self.level_label.text().split("\n"))

    def generate(self):
        # generates the command block command from saved layers
        # change strings in storage to lists
        layer_mob = self.mobs_label.text().split("\n")
        layer_num = [int(x) for x in self.height_label.text().split("\n")]
        layer_index = [int(x) - 1 for x in self.level_label.text().split("\n")]
        # beginning of command
        command = f"/summon {layer_mob[0]} ~ ~1 ~ {{"
        # decrease amount of 1st mob to spawn by 1
        layer_num[0] -= 1
        end = ""
        # for each layer add the passenger *arg to stack and save an extra } to put at the end of the command
        for layer in layer_index:
            i = 0
            while layer_num[layer] > i:
                command = f"{command}Passengers:[{{id:{layer_mob[layer]},"
                end = f"{end}}}]"
                i += 1
        # combine command with the ending brackets + 1 extra ending bracket
        command = f"{command}{end}}}"
        # set output field to the command
        self.output.setText(command)

    def copy(self):
        # copy text in output field to clipboard
        clipboard = QGuiApplication.clipboard()

        clipboard.setText(self.output.text())

# Just some Qt boiler plate
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec())
