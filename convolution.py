import numpy as np


def matris_olustur(satir, sutun):
    matris = np.zeros((satir, sutun))
    for i in range(satir):
        for j in range(sutun):
            matris[i, j] = float(input(f"Matrisin elemanını girin [{i}][{j}]: "))
    return matris


def filtre_olustur(satir, sutun):
    filter_matrix = np.zeros((satir, sutun))
    for i in range(satir):
        for j in range(sutun):
            filter_matrix[i][j] = float(input(f"Filtre Matrisinin elemanını girin [{i}][{j}]: "))
    return filter_matrix


def giris_matrisleri(k, pad_d, satir, sutun):
    matrisler = []
    for _ in range(k):
        matris = matris_olustur(satir, sutun)
        pad_matris = np.pad(matris, pad_d, mode='constant')
        matrisler.append(pad_matris)
    return matrisler


def filtre_matrisleri(k, satir, sutun):
    filtre_matrisler = []
    for _ in range(k):
        filter_matris = filtre_olustur(satir, sutun)
        filtre_matrisler.append(filter_matris)
    return filtre_matrisler


def padding_degeri_hesapla(f):
    return (f - 1) // 2


def cikis_matrisi(k, b, n1, n2, f1, f2, s):
    p = padding_degeri_hesapla(f1)
    cikis_satir = ((n1 + 2 * p - f1) // s) + 1
    cikis_sutun = ((n2 + 2 * p - f2) // s) + 1
    cikis_matris = np.zeros((cikis_satir, cikis_sutun))
    girismatrisleri = giris_matrisleri(k, p, n1, n2)
    filtrematrisleri = filtre_matrisleri(k, f1, f2)

    for _ in range(len(girismatrisleri)):
        giris_matrisi = girismatrisleri[_]
        filtre_matrisi = filtrematrisleri[_]

        for i in range(0, cikis_satir):
            for j in range(0, cikis_sutun):
                # Filtre bölgesini seç
                bolum = giris_matrisi[i * s:i * s + f1, j * s:j * s + f2]

                # Filtre ile eleman eleman çarp
                carpimlar = bolum * filtre_matrisi

                # Çarpımları topla ve çıkış matrisine ata
                cikis_matris[i, j] += np.sum(carpimlar)

    # Bias ekleniyor
    cikis_matris += b

    return cikis_matris


kanal_sayisi = int(input("Görüntünün kanal sayısını giriniz: "))
g_satir = int(input("Giriş matrisi için satır sayısını girin: "))
g_sutun = int(input("Giriş matrisi için sütun sayısını girin: "))
f_satir = int(input("Filtre matrisi için satır sayısını girin: "))
f_sutun = int(input("Filtre matrisi için sütun sayısını girin: "))
bias = int(input("Filtrenin bias değerini giriniz: "))
kaydirma_adimi = int(input("Kaydırma Adımını Giriniz: "))
pad_deger = padding_degeri_hesapla(f_satir)

cikis_matrisi_sonucu = cikis_matrisi(kanal_sayisi, bias, g_satir, g_sutun, f_satir, f_sutun, kaydirma_adimi)

print("Çıkış Matrisi:")
print(cikis_matrisi_sonucu)
