from server import *
from klien import *

def main():
    # membuat server
    demo_server = Server(9009)
    demo_server.buka()

    # membuat klien 1 terhubung ke server (port=9009 dan membuka nama channel sembarang)
    demo_klien_1 = Klien('localhost', 9009, 'nama channel 1')
    demo_klien_1.sambungkan()

    # membuat klien 2 terhubung ke server (port=9009 dan nama channel sama dengan klien 1 [agar dapat berkomunikasi])
    demo_klien_2 = Klien('localhost', 9009, 'nama channel 1')
    demo_klien_2.sambungkan()

    '''
    Untuk memblokir pengiriman data (mic mute) dapat menggunakan perintah Klien.mengirim = 0 (1 untuk membuka blokir)
    Untuk memblokir penerimaan data (speaker mute) dapat menggunakan perintah Klien.menerima = 0 (1 untuk membuka blokir)
    '''

if __name__ == "__main__":
    main()