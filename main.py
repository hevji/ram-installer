import sys
import random
import time
import psutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox,
    QProgressBar, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Fake DDR type mapping based on real RAM (just for demo)
# In reality, detecting DDR type is platform-specific and requires WMI (Windows) or dmidecode (Linux)
RAM_DDR_FAKE = {
    4: "DDR3",
    8: "DDR4",
    16: "DDR4",
    32: "DDR5",
    64: "DDR5",
}

class RamInstallerThread(QThread):
    progress_update = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def run(self):
        progress = 0
        while progress < 100:
            time.sleep(random.uniform(0.02, 0.12))
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.8))
            progress += random.randint(1, 4)
            if progress > 100:
                progress = 100
            self.progress_update.emit(progress)
        self.progress_update.emit(100)
        self.finished_signal.emit()

class RamInstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAM Installer 3000 💾")
        self.setFixedSize(450, 270)
        self.center_window()
        self.user_ram = round(psutil.virtual_memory().total / (1024**3))  # in GB
        self.init_ui()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        self.label = QLabel(f"Detected RAM: {self.user_ram} GB")
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ram_label = QLabel("Select RAM amount to install:")
        self.layout.addWidget(self.ram_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.combo = QComboBox()
        self.combo.addItems(["4 GB", "8 GB", "16 GB", "32 GB", "64 GB", "Custom"])
        self.layout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ddr_label = QLabel("Select DDR type:")
        self.layout.addWidget(self.ddr_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ddr_combo = QComboBox()
        self.ddr_combo.addItems(["DDR3", "DDR4", "DDR5"])
        self.layout.addWidget(self.ddr_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.install_btn = QPushButton("Install RAM")
        self.layout.addWidget(self.install_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress.setFixedHeight(40)  # "thiccer" bar
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)

        self.install_btn.clicked.connect(self.confirm_install)

    def confirm_install(self):
        reply = QMessageBox.question(
            self, 'Confirm Installation',
            "Are you sure you want to install RAM?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.start_install()

    def start_install(self):
        # Determine amount
        amount_text = self.combo.currentText()
        if amount_text == "Custom":
            amount_gb = random.randint(1, 64)
        else:
            amount_gb = int(amount_text.split()[0])

        selected_ddr = self.ddr_combo.currentText()

        # Check against "fake DDR type" mapping
        real_ddr = RAM_DDR_FAKE.get(self.user_ram, "DDR4")
        if selected_ddr != real_ddr:
            QMessageBox.critical(
                self, "Installation Failed",
                f"Cannot install {amount_gb} GB: Wrong DDR type ({selected_ddr})! "
                f"Your system DDR: {real_ddr}"
            )
            return

        self.label.setText(f"Installing {amount_gb} GB ({selected_ddr})...")
        self.install_btn.setEnabled(False)
        self.combo.setEnabled(False)
        self.ddr_combo.setEnabled(False)

        # Start fake installation
        self.thread = RamInstallerThread()
        self.thread.progress_update.connect(self.update_progress)
        self.thread.finished_signal.connect(self.install_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress.setValue(value)

    def install_finished(self):
        self.label.setText("Installation complete!")
        reply = QMessageBox.question(
            self, 'Reboot Required',
            "RAM installation complete. Reboot now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Rebooting...", "System will now reboot! 💻")
            import os; os.system("shutdown /r /t 1")
        else:
            # Start fake uninstall process
            self.combo.hide()
            self.ddr_combo.hide()
            self.ddr_label.hide()
            self.install_btn.hide()
            self.progress.setValue(0)
            self.label.setText("Uninstalling RAM...")
            self.thread = RamInstallerThread()
            self.thread.progress_update.connect(self.update_progress)
            self.thread.finished_signal.connect(self.uninstall_finished)
            self.thread.start()

def uninstall_finished(self):
    self.progress.hide()  # removes the line
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.label.setText("RAM uninstalled successfully!")

    ok_btn = QPushButton("OK")
    ok_btn.setFixedWidth(80)
    self.layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignRight)
    ok_btn.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RamInstallerApp()
    window.show()
    sys.exit(app.exec())
