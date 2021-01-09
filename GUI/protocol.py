import serial

DC1 = 0x11  # kommt vom Plotter -> leerer Puffer
DC3 = 0x13  # kommt vom Plotter -> Puffer voll
DC4 = 0x14  # kommt vom Plotter -> Fehlerstatus abfragen
ENQ = 0x05  # geht an Plotter -> Statusbyte Abfrage

IN = 'IN'   # Plotterinitialisierung
DF = 'DF'   # Plotter auf Standardwerte zurücksetzen
OI = 'OI'   # Plotter schickt Version und Namen zurück
NR = 'NR'   # Plotvorgang abgeschlossen

"""
Statusbyte aufbau:
    0 => 1 - falsches Kommando

    1 => 1 - Parameter außerhalb vom Zahlenbereich

    2 => 1 - Parameter außerhab der Fenstergröße

    3 => 1 - Paritätsfehler

    4 => 0 - immer 0

    5 => 0 - Puffer aufnahmefähig
      => 1 - Puffer voll

    6 => 0 - Plotter im offline-Modus
      => 1 - Plotter arbeitet Programm ab

    7 => Paritätsbit
"""

class K6418():
    
    def __init__(self, port, baud=9600):
        self.uart = serial.Serial(port, baud, parity=PARITY_ODD)    # Plotter erwartet 7 Bits Daten und 1 Paritätsbit -> ungerade Parität
        self.uart.timeout = 2
        self.status_byte = self.check_status()

    def __del__(self):
        self.uart.close()

    def send_byte(self, byte):
        self.uart.write(byte)

    def check_status(self):
        self.send_byte(ENQ)
        ret = self.uart.read()
