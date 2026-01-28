import sys
import random
from PyQt6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

UPDATE_INTERVAL = 3000  # ms
SPEED_LIMIT = 70
MAX_POINTS = 30


class VariableMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Variable Monitor")
        self.setGeometry(200, 200, 800, 500)
        self.speed_data = []

        self.init_ui()
        self.init_timer()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # -------------------- VARIABLE DISPLAY --------------------
        grid = QtWidgets.QGridLayout()
        self.labels = {}
        variables = ["Speed", "Speed 2", "Latitude", "Longitude", "Altitude"]
        for i, var in enumerate(variables):
            grid.addWidget(QtWidgets.QLabel(f"{var}:"), i, 0)
            lbl = QtWidgets.QLabel("0")
            lbl.setStyleSheet("font-weight: bold; color: black;")
            grid.addWidget(lbl, i, 1)
            self.labels[var] = lbl

        var_frame = QtWidgets.QGroupBox("Variables")
        var_frame.setLayout(grid)

        # -------------------- CHECKBOXES --------------------
        chk_layout = QtWidgets.QVBoxLayout()
        self.chk1 = QtWidgets.QCheckBox("Enable GPS Logging")
        self.chk2 = QtWidgets.QCheckBox("Enable Auto Pilot")
        self.chk3 = QtWidgets.QCheckBox("Enable Alerts")
        for c in (self.chk1, self.chk2, self.chk3):
            chk_layout.addWidget(c)

        chk_frame = QtWidgets.QGroupBox("Controls")
        chk_frame.setLayout(chk_layout)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(var_frame)
        top_layout.addWidget(chk_frame)

        layout.addLayout(top_layout)

        # -------------------- DROPDOWN + BUTTON --------------------
        sound_layout = QtWidgets.QHBoxLayout()
        sound_layout.addWidget(QtWidgets.QLabel("Sound Bite:"))
        self.sound_combo = QtWidgets.QComboBox()
        self.sound_combo.addItems(
            ["Sound 1", "Sound 2", "Sound 3", "Sound 4", "Sound 5", "Sound 6"]
        )
        sound_layout.addWidget(self.sound_combo)
        self.play_btn = QtWidgets.QPushButton("Play")
        self.play_btn.clicked.connect(self.play_sound)
        sound_layout.addWidget(self.play_btn)

        sound_frame = QtWidgets.QGroupBox("Sound Settings")
        sound_frame.setLayout(sound_layout)
        layout.addWidget(sound_frame)

        # -------------------- GRAPH --------------------
        self.graph = pg.PlotWidget(title="Speed Over Time")
        self.graph.showGrid(x=True, y=True)
        self.graph.setYRange(0, 120)
        self.graph_curve = self.graph.plot(pen=pg.mkPen("y", width=2))
        layout.addWidget(self.graph)

        # -------------------- INDICATOR --------------------
        indicator_layout = QtWidgets.QHBoxLayout()
        indicator_layout.addWidget(QtWidgets.QLabel("Speed Limit Warning:"))
        self.light = QtWidgets.QLabel()
        self.light.setFixedSize(40, 20)
        self.light.setStyleSheet("background-color: green; border-radius: 5px;")
        indicator_layout.addWidget(self.light)
        layout.addLayout(indicator_layout)

        # -------------------- EXIT BUTTON --------------------
        exit_btn = QtWidgets.QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

    def init_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(UPDATE_INTERVAL)

    def play_sound(self):
        sound = self.sound_combo.currentText()
        QtWidgets.QMessageBox.information(
            self, "Sound", f"Playing {sound} (feature not yet implemented)"
        )

    def update_data(self):
        # Simulated data; replace this with serial/GPS reads
        speed = round(random.uniform(0, 100), 2)
        speed2 = round(random.uniform(0, 100), 2)
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        altitude = round(random.uniform(0, 5000), 2)

        # Update labels
        self.labels["Speed"].setText(f"{speed} km/h")
        self.labels["Speed 2"].setText(f"{speed2} km/h")
        self.labels["Latitude"].setText(str(latitude))
        self.labels["Longitude"].setText(str(longitude))
        self.labels["Altitude"].setText(f"{altitude} m")

        # Update speed history
        self.speed_data.append(speed)
        if len(self.speed_data) > MAX_POINTS:
            self.speed_data.pop(0)

        # Update graph
        self.graph_curve.setData(self.speed_data)

        # Update light
        color = "red" if speed > SPEED_LIMIT else "green"
        self.light.setStyleSheet(f"background-color: {color}; border-radius: 5px;")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = VariableMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
