import socket, threading

class Server:
    def __init__(self, port):
        self.port = port
        self._terbuka = 0

    def buka(self):
        if self._terbuka: return

        try:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.bind(('0.0.0.0', self.port))
        except:
            print('Tidak dapat menjalankan pada port tersebut')
            return

        self._klien = {}

        self._s.listen(100)
        print('berjalan pada port: '+str(self.port))

        threading.Thread(target=self._menerima_klien).start()

        self._terbuka = 1

    def _menerima_klien(self):
        while 1:
            try:
                c, addr = self._s.accept()
                data = c.recv(1024)
                channel = data.decode()
                if channel in self._klien:
                    self._klien[channel].append(c)
                else:
                    self._klien[channel] = [c]

                print(addr, 'terhubung ke channel', channel)
                
                threading.Thread(target=self._penanganan_klien, args=(c, addr, channel,)).start()
            except:
                print('Koneksi terputus')
                break

    def _penanganan_klien(self, c, addr, channel):
        while 1:
            try:
                data = c.recv(1024)
                for k in self._klien[channel]:
                    if k != self._s and k != c:
                        try:
                            k.send(data)
                        except:
                            pass
            except socket.error:
                c.close()
                self._klien[channel].remove(c)
                print(addr, 'terputus dari channel', channel)
                break

    def tutup(self):
        for x in self._klien:
            for y in self._klien[x]:
                y.close()
        self._s.close()
        self._terbuka = 0