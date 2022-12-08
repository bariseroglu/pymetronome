from PyQt6.QtCore import QThread, pyqtSignal
from threading import Thread
from playsound import playsound
import datetime
import time

class Metronome(QThread):

    nextBeat = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initMetronome(60, '4/4', 'Kick')
        self.__run = False

    def run(self):
        self.__run = True
        current_time = datetime.datetime.now().microsecond / 1000
        signatureBeats = int(self.signature.split('/')[0])
        counter = 0
        while True:
            if not self.__run:
                break
            if current_time - self.tolerance < self.beatPoint % 1 * 1000 < current_time + self.tolerance:
                self.beatPoint += self.nextBeatPoint
                Thread(target=playsound, args=(self.sound,)).start()
                self.nextBeat.emit(counter)
                counter+=1
                if counter == signatureBeats: counter = 0
                time.sleep(0.1)
            current_time = datetime.datetime.now().microsecond / 1000

    def initMetronome(self, bpm, signature, soundOption):
        sound = {}
        sound['Kick'] = 'kick.mp3'
        sound['Click'] = 'click.mp3'
        self.sound = 'assets/sounds/' + sound[soundOption]
        self.tolerance = 0.01
        self.bpm = bpm
        div = 1
        signatureBeat = int(signature.split('/')[1])
        if signatureBeat == 4:
            div = 60
        else: div = 30
        self.beats = self.bpm/div
        self.nextBeatPoint = 1 / self.beats
        self.beatPoint = 0
        self.signature = signature

    def isRunning(self):
        return self.__run

    def stop(self):
        self.__run = False