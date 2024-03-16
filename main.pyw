import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

color_1 = "color: white; border: 1px solid teal"
style_1 = f"background: #222222; {color_1};"
style_2 = f"background: #666666; {color_1};"
background_1 = "background-color: #111111;"

class ButtonHoverEventFilter(QObject):
    def __init__(self, button):
        super().__init__(button)
        self.button = button
        self.original_style = button.styleSheet()

    def eventFilter(self, obj, event):
        if obj == self.button:
            if event.type() == QEvent.Enter:
                self.button.setStyleSheet(style_1)
            elif event.type() == QEvent.Leave:
                self.button.setStyleSheet(self.original_style)
            elif event.type() == QEvent.MouseButtonPress:
                self.button.setStyleSheet(style_2)
            elif event.type() == QEvent.MouseButtonRelease:
                self.button.setStyleSheet(self.original_style)
        return super().eventFilter(obj, event)

class StyledButton(QPushButton):
    def __init__(self, title, highlightable=True):
        super().__init__(title)
        self.setMinimumHeight(25)
        self.highlightable = highlightable
        self.original_style = ""
        self.setStylesheet()
        self.installEventFilter(ButtonHoverEventFilter(self))

    def setStylesheet(self):
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setColorAt(0, QColor(70, 70, 70))
        gradient.setColorAt(1, QColor(128, 0, 0))
        gradient_stops = gradient.stops()
        gradient_str = "qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0,"
        for stop in gradient_stops:
            color = stop[1].darker(200).name()
            pos = 1 - stop[0]
            gradient_str += f" stop: {pos} {color},"
        gradient_str = gradient_str.rstrip(",") + ")"
        self.original_style = f"QPushButton {{background: {gradient_str}; color: white; border: 1px solid black; border-radius: 5px;}}"
        self.setStyleSheet(self.original_style)

class GameLauncher(QWidget):
    def __init__(self, games, lan_username):
        super().__init__()
        self.games = games
        self.lan_username = lan_username
        self.settings = QSettings("Mythical", "Plutonium Launcher")
        self.initUI()

    def initUI(self):
        self.resize(self.settings.value("size", QSize(400, 200)))
        self.move(self.settings.value("pos", QPoint(100, 100)))

        with open('settings.json') as f:
            data = json.load(f)
            self.selected_game = data.get('selected_game', self.games[0])
            self.delay = data.get('delay', 1.0) 
            self.selected_index = data.get('selected_index', 0)

        layout = QVBoxLayout()

        for game in self.games:
            button_layout = QHBoxLayout()
            game_button = StyledButton(game["name"])
            game_button.clicked.connect(lambda _, arg=game["arg"], directory=game.get("directory", ""): self.launchGame(arg, directory))
            button_layout.addWidget(game_button)

            dir_button = StyledButton("..", highlightable=False)
            dir_button.setFixedSize(40, 25)
            dir_button.clicked.connect(lambda _, game=game: self.setGameDirectory(game))
            button_layout.addWidget(dir_button)

            layout.addLayout(button_layout)

        self.user_button = StyledButton(f'User: {self.lan_username}', highlightable=False)
        self.user_button.setObjectName("UserButton")
        self.user_button.clicked.connect(self.change_username)
        layout.addWidget(self.user_button)

        panel_layout = QHBoxLayout()

        self.game_label = QLabel("Select Game:")
        panel_layout.addWidget(self.game_label)

        self.game_combobox = QComboBox()
        panel_layout.addWidget(self.game_combobox)

        self.delay_label = QLabel("Delay:")
        panel_layout.addWidget(self.delay_label)

        self.delay_spinbox = QDoubleSpinBox()
        self.delay_spinbox.setSingleStep(0.1)
        self.delay_spinbox.setValue(float(self.delay))
        panel_layout.addWidget(self.delay_spinbox)

        self.auto_execute_checkbox = QCheckBox("Auto Execute")
        self.auto_execute_checkbox.setChecked(self.settings.value("auto_execute", True, type=bool))
        self.auto_execute_checkbox.stateChanged.connect(self.updateSettings)
        panel_layout.addWidget(self.auto_execute_checkbox)

        layout.addLayout(panel_layout)

        self.setLayout(layout)
        self.setWindowTitle('Plutonium Launcher')

        self.setWindowIcon(QIcon('assets/plutonium_icon.ico'))

        self.setStyleSheet("""
            QWidget {
                background-color: #4d0000;
                color: white;
            }
            QPushButton#UserButton {
                background-color: #8b0000;
                border: 1px solid #8b0000;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton#UserButton:hover {
                background-color: #a30000;
                border: 1px solid #a30000;
            }
            QPushButton {
                min-height: 25px;
            }
        """)

        self.populateGameComboBox()
        
        for index, game in enumerate(self.games):
            if game == self.selected_game:
                self.game_combobox.setCurrentIndex(index)
                break

        self.game_combobox.setCurrentIndex(self.selected_index)
        self.delay_spinbox.valueChanged.connect(self.updateDelay)
        self.game_combobox.currentIndexChanged.connect(self.updateSelectedGame)
        self.show()
        self.updateSettings()

    def updateSelectedGame(self, index):
        self.selected_index = index
        self.settings.setValue("selected_index", index)

        with open('settings.json', 'r+') as f:
            data = json.load(f)
            data["selected_index"] = index
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def updateDelay(self, value):
        self.delay = value
        self.settings.setValue("delay", value)

        with open('settings.json', 'r+') as f:
            data = json.load(f)
            data["delay"] = value
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def populateGameComboBox(self):
        for index, game in enumerate(self.games):
            self.game_combobox.addItem(game["name"], game)

    def updateSettings(self):
        self.settings.setValue("auto_execute", self.auto_execute_checkbox.isChecked())
        self.settings.setValue("delay", self.delay_spinbox.value())
        selected_game_index = self.game_combobox.currentIndex()
        selected_game_data = self.game_combobox.itemData(selected_game_index)

        with open('settings.json', 'r+') as f:
            data = json.load(f)
            data["auto_execute"] = self.auto_execute_checkbox.isChecked()
            data["delay"] = self.delay_spinbox.value()
            data["selected_game"] = selected_game_data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        if self.auto_execute_checkbox.isChecked():
            QTimer.singleShot(int(self.delay * 1000), self.launchSelectedGame)

    def launchSelectedGame(self):
        selected_game_data = self.game_combobox.currentData()
        if selected_game_data:
            arg = selected_game_data.get("arg")
            directory = selected_game_data.get("directory", "")
            self.launchGame(arg, directory)

    def launchGame(self, arg, directory):
        if not directory:
            selected_directory = QFileDialog.getExistingDirectory(self, f"Select Directory for {arg}", "")
            if selected_directory:
                for game in self.games:
                    if game["arg"] == arg:
                        game["directory"] = selected_directory
                        directory = selected_directory
                        break
                with open('settings.json', 'w') as f:
                    json.dump({'games': self.games, 'lan_username': self.lan_username}, f, indent=4)

        os.chdir(os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium'))
        cmd = [f'{os.getcwd()}/bin/plutonium-bootstrapper-win32.exe', arg, directory, '+name', self.lan_username, '-lan']
        subprocess.Popen(cmd)
        self.close()

    def setGameDirectory(self, game):
        selected_directory = QFileDialog.getExistingDirectory(self, f"Select Directory for {game['arg']}", "")
        if selected_directory:
            game["directory"] = selected_directory
            with open('settings.json', 'w') as f:
                json.dump({'games': self.games, 'lan_username': self.lan_username}, f, indent=4)

    def change_username(self):
        new_username, okPressed = QInputDialog.getText(self, "Change LAN Username", "Enter your new LAN Username:", QLineEdit.Normal, "")
        if okPressed and new_username != '':
            self.lan_username = new_username
            self.user_button.setText(f'User: {self.lan_username}')
            with open('settings.json', 'w') as f:
                json.dump({'games': self.games, 'lan_username': self.lan_username}, f, indent=4)

def main():
    with open('settings.json') as f:
        data = json.load(f)
        games_data = data['games']
        lan_username = data.get('lan_username', '')

    app = QApplication(sys.argv)
    if not lan_username:
        lan_username = prompt_lan_username()
        if not lan_username:
            print("LAN username not provided. Exiting.")
            sys.exit(1)
        with open('settings.json', 'w') as f:
            json.dump({'games': games_data, 'lan_username': lan_username}, f, indent=4)
    launcher = GameLauncher(games_data, lan_username)
    sys.exit(app.exec_())

def prompt_lan_username():
    username, okPressed = QInputDialog.getText(None, "Enter LAN Username", "Your LAN Username:", QLineEdit.Normal, "")
    if okPressed and username != '':
        return username
    return None

if __name__ == '__main__':
    main()
