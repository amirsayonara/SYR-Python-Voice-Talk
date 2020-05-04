import socket, threading, pyaudio

class Klien:
    def __init__(self, ip, port, nama_channel):
        self.ip = ip
        self.port = port
        self.channel = nama_channel
        self._tersambung = 0
        
    def sambungkan(self):
        if self._tersambung: return

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._s.connect((self.ip, self.port))
        except:
            print('Tidak dapat terhubung ke server')
            return
        
        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # penyiapan mic dan speaker
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Terhubung server")
        
        try:
            self._s.sendall(self.channel.encode())
            print('Terhubung ke channel', self.channel)
        except:
            self._s.close()
            print('Koneksi terputus')

        threading.Thread(target=self._menerima_data).start()
        threading.Thread(target=self._mengirim_data).start()

        self._tersambung = 1

    def _mengirim_data(self):
        self.mengirim = 1
        while 1:
            if self.mengirim:
                try:
                    data = self.recording_stream.read(1024)
                    self._s.sendall(data)
                except:
                    self._s.close()
                    self._tersambung = 0
                    print('Koneksi terputus')
                    break

    def _menerima_data(self):
        self.menerima = 1
        while 1:
            try:
                data = self._s.recv(1024)
                if self.menerima:
                    self.playing_stream.write(data)
            except:
                self._s.close()
                self._tersambung = 0
                print('Koneksi terputus')
                break

    def putuskan(self):
        self._tersambung = 0
        self._s.close()