import serial
import time

DC1 = '\x11'  # kommt vom Plotter -> leerer Puffer
DC3 = '\x13'  # kommt vom Plotter -> Puffer voll
DC4 = '\x14'  # kommt vom Plotter -> Fehlerstatus abfragen
ENQ = '\x05'  # geht an Plotter -> Statusbyte Abfrage

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
        self.uart = serial.Serial(port, baud, 
                bytesize=serial.EIGHTBITS,#SEVENBITS,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE)    
                # Plotter erwartet 7 Bits Daten und 1 Paritätsbit -> ungerade Parität
        #self.uart = serial.Serial(port, baud)
        self.uart.timeout = 0.1
        #self.status_byte = self.check_status()

    def __del__(self):
        self.uart.close()

    def set_mode(self, mode='7o1'):
        if mode == '7o1':
            self.uart.bytesize = serial.SEVENBITS

    def send_byte(self, cmd):
        for byte in cmd:
            self.uart.write(byte.encode())
            time.sleep(0.01)

    def read_byte(self):
        self.set_mode('7o1')
        ret = self.uart.readall()
        return ret

    def del_buffer(self):
        self.uart.reset_input_buffer()
        self.uart.reset_output_buffer()

    def check_status(self):
        ret = self.uart.read().decode()
        if ret == DC1:
            self.send_byte(ENQ)
        ret = self.uart.readall()
        return ret

    def read_hpgl(self, f_path):
        try:
            f = open(path, 'r')
            cmd_list = f.readline()
            f.close()
            #  .replace("IN", "DF")
            cmd_list = cmd_list.replace("PU", "PU;PA").replace("PD", "PD;PA")
            print(cmd_list)

            for cmd in cmd_list.split(';'):
                cmd= cmd + ';'
                self.send_byte(cmd)
                ret = self.read_byte()
                if ret == b'\x14':
                    print("Error! check ENQ")
                    ret = self.read_byte()
                    print(ret)
                if ret == b'\x08':
                    print("Fehler!!")
                    break
        except:
            raise

if __name__ == '__main__':
    plotter = K6418('/dev/ttyACM0')
    while True:
        try:
            cmd = input(">>> ")

            if cmd == "exit":
                exit()
            if cmd == "Flush":
                plotter.del_buffer()

            if cmd == "ENQ":
                plotter.send_byte(ENQ)
                print(plotter.read_byte())
                continue
            if cmd == "file":
                path = "/home/meister/Bilder/Zeichnung.hpgl"
                plotter.read_hpgl(path)
                continue

            plotter.send_byte(cmd)
            print(plotter.read_byte())

        except:
            plotter.send_byte(";IN;")
            exit()





