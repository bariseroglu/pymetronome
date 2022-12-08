import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import uic
import time
import random
from metronome import Metronome

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        self.setWindowTitle('PyMetronome')
        self.setFixedSize(640, 600)
        self.bpm.setText('60')
        self.bpmSlider.setValue(60)
        self.bpmSlider.valueChanged.connect(self.valueChanged)
        self.bpmSlider.sliderReleased.connect(self.sliderReleased)
        self.metronomeStatus = False
        self.play.clicked.connect(self.changeMetronomeStatus)
        self.randomBpm.clicked.connect(self.setRandomBpm)
        self.timeSignatureComboBox.addItems(['1/4','2/4','3/4','4/4','5/4','7/4','5/8','6/8','7/8','9/8','12/8'])
        self.timeSignatureComboBox.setCurrentText('4/4')
        self.timeSignatureComboBox.currentTextChanged.connect(self.signatureChanged)
        self.soundComboBox.setCurrentText('4/4')
        self.soundComboBox.addItems(['Kick', 'Click'])
        self.soundComboBox.currentTextChanged.connect(self.soundChanged)
        self.metronome = Metronome()
        self.metronome.nextBeat.connect(self.nextBeat)
        self.signatureChanged('4/4')

    def valueChanged(self, value):
        self.bpm.setText(str(value))

    def sliderReleased(self):
        if self.metronome.isRunning():
            self.metronome.stop()
            time.sleep(0.1)
            self.metronome.initMetronome(self.bpmSlider.value(), self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())
            self.metronome.start()
        else:
            self.metronome.initMetronome(self.bpmSlider.value(), self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())

    def signatureChanged(self, value):
        beats = int(value.split('/')[0])
        for i in range(12):
            self.beats.itemAt(i).widget().setVisible(True)
        for i in range(beats, 12):
            self.beats.itemAt(i).widget().setVisible(False)
        if self.metronome.isRunning():
            self.metronome.stop()
            time.sleep(0.1)
            self.metronome.initMetronome(self.bpmSlider.value(), value, self.soundComboBox.currentText())
            self.metronome.start()
        else:
            self.metronome.initMetronome(self.bpmSlider.value(), value, self.soundComboBox.currentText())

    def changeMetronomeStatus(self):
        if self.metronomeStatus:
            self.play.setIcon(QIcon(QPixmap('assets/icons/play.png')))
            self.metronomeStatus = False
            self.metronome.stop()
        else:
            self.play.setIcon(QIcon(QPixmap('assets/icons/pause.png')))
            self.metronomeStatus = True
            self.metronome.start()

    def nextBeat(self, beat):
        for i in range(int(self.timeSignatureComboBox.currentText().split('/')[0])):
            self.beats.itemAt(i).widget().setPixmap(QPixmap('assets/icons/red.png'))
        self.beats.itemAt(beat).widget().setPixmap(QPixmap('assets/icons/green.png'))

    def setRandomBpm(self):
        bpm = random.randint(60, 240)
        if self.metronome.isRunning():
            self.metronome.stop()
            time.sleep(0.1)
            self.metronome.initMetronome(bpm, self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())
            self.metronome.start()
        else:
            self.metronome.initMetronome(bpm, self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())
        self.bpm.setText(str(bpm))
        self.bpmSlider.setValue(bpm)

    def soundChanged(self):
        if self.metronome.isRunning():
            self.metronome.stop()
            time.sleep(0.1)
            self.metronome.initMetronome(self.bpmSlider.value(), self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())
            self.metronome.start()
        else:
            self.metronome.initMetronome(self.bpmSlider.value(), self.timeSignatureComboBox.currentText(), self.soundComboBox.currentText())

    def closeEvent(self, event):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

