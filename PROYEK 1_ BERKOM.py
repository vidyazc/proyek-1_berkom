# Program : Rekomendasi Kantin ITB Jatinangor
# Spesifikasi : Menerima jam makan dan kantin tujuan
# Fakultas yang istirahat dianggap ke kantin terdekat dari gedung kelas terakhirnya
# Jika kantin tujuan ramai (>= 80%) atau penuh, tampilkan kantin lain urut dari yang paling sepi, terdekat, lalu kursi kosong terbanyak

# Kamus
# fakultas, mulai, selesai, gedung_akhir, mahasiswa : data fakultas
# gedung, kantin : list of string
# kursi, jarak : list of int
# persen_makan, waktu_input : float
# waktu, tujuan, terdekat, a, b, i, j, f, k, g : int
# pengunjung, kepadatan, kosong, urutan : list
# lebih_baik : boolean

# Algoritma :

# Data (simulasi)
fakultas = ["SITH", "SBM", "FTSL", "FSRD", "FTI", "FTTM",
            "STEI", "SAPPK", "FITB", "SF", "FTMD", "FMIPA"]
mulai = [660, 660, 690, 690, 720, 720, 720, 750, 780, 840, 810, 690]
selesai = [720, 720, 750, 750, 780, 780, 780, 810, 840, 900, 870, 750]

gedung = ["Gedung A", "Gedung B", "Gedung C", "Gedung D", "Gedung E",
          "GKU 1", "GKU 2", "GKU 3", "Lab Terpadu"]
gedung_akhir = [0, 1, 3, 8, 6, 7, 5, 4, 5, 6, 7, 2]

# jumlah mahasiswa per fakultas (data kelompok)
mahasiswa = [436, 476, 468, 513, 733, 491, 725, 269, 487, 223, 444, 532]
persen_makan = 0.4     # bagian mahasiswa yang ke kantin saat istirahat

kantin = ["Kantin GKU 2", "Kantin KOICA", "Kantin TB 1", "Kantin TB 2", "Kantin TB 3"]
kursi = [280, 18, 48, 102, 102]

# jarak (m): baris = gedung, kolom = kantin
jarak = [[250, 100, 180, 170, 160],
         [270, 110, 170, 160, 150],
         [250, 100, 190, 180, 170],
         [110, 190, 310, 290, 270],
         [100, 190, 310, 290, 270],
         [80, 250, 330, 310, 290],
         [0, 270, 350, 330, 310],
         [290, 80, 100, 190, 210],
         [70, 290, 370, 350, 330]]

# Input
waktu_input = float(input("Mau makan jam berapa (contoh 12.15)? "))
waktu = int(waktu_input) * 60 + round((waktu_input - int(waktu_input)) * 100)

print("Kantin:")
for k in range(len(kantin)):
    print(k + 1, ".", kantin[k])
tujuan = int(input("Nomor kantin tujuan? ")) - 1

# Hitung pengunjung tiap kantin (pola istirahat + kantin terdekat)
pengunjung = [0, 0, 0, 0, 0]
jml_jarak = [0, 0, 0, 0, 0]
total_orang = 0
for f in range(len(fakultas)):
    if mulai[f] <= waktu and waktu < selesai[f]:
        terdekat = 0
        for k in range(len(kantin)):
            if jarak[gedung_akhir[f]][k] < jarak[gedung_akhir[f]][terdekat]:
                terdekat = k
        orang = int(round(mahasiswa[f] * persen_makan))
        pengunjung[terdekat] = pengunjung[terdekat] + orang
        if terdekat == tujuan:
            total_orang = total_orang + orang
            for k in range(len(kantin)):
                jml_jarak[k] = jml_jarak[k] + orang * jarak[gedung_akhir[f]][k]

jarak_rata = [0, 0, 0, 0, 0]
if total_orang > 0:
    for k in range(len(kantin)):
        jarak_rata[k] = int(jml_jarak[k] / total_orang)

# Kepadatan dan kursi kosong
kepadatan = []
kosong = []
for k in range(len(kantin)):
    nilai = int(pengunjung[k] / kursi[k] * 100)
    if nilai > 100:
        nilai = 100
    kepadatan.append(nilai)
    sisa = kursi[k] - pengunjung[k]
    if sisa < 0:
        sisa = 0
    kosong.append(sisa)

# Output kondisi kantin tujuan
if kepadatan[tujuan] >= 80:
    kategori = "SANGAT RAMAI"
elif kepadatan[tujuan] >= 50:
    kategori = "SEDANG"
else:
    kategori = "SEPI"

print()
print(kantin[tujuan], "->", kepadatan[tujuan], "% kapasitas ->", kategori)

# Keputusan
if kepadatan[tujuan] < 80 and kosong[tujuan] > 0:
    print()
    print("Rekomendasi:")
    print("->", kantin[tujuan], "(masih nyaman dikunjungi)")
    print("-> Tingkat kepadatan", kepadatan[tujuan], "%")
else:
    # cari kantin alternatif (selain kantin tujuan)
    urutan = []
    for k in range(len(kantin)):
        if k != tujuan:
            urutan.append(k)

    # urutkan: kepadatan terendah, lalu jarak terdekat, lalu kursi kosong terbanyak
    for i in range(len(urutan)):
        for j in range(i + 1, len(urutan)):
            a = urutan[i]
            b = urutan[j]
            lebih_baik = False
            if kepadatan[b] < kepadatan[a]:
                lebih_baik = True
            elif kepadatan[b] == kepadatan[a]:
                if jarak_rata[b] < jarak_rata[a]:
                    lebih_baik = True
                elif jarak_rata[b] == jarak_rata[a] and kosong[b] > kosong[a]:
                    lebih_baik = True
            if lebih_baik:
                urutan[i] = b
                urutan[j] = a

    # rekomendasi = kantin urutan pertama
    k = urutan[0]
    print()
    print("Rekomendasi:")
    print("->", kantin[k])
    print("-> Tingkat kepadatan", kepadatan[k], "%")
    print("-> jarak rata-rata", jarak_rata[k], "m dari asal mahasiswa dan",
          kosong[k], "kursi kosong")

    # alternatif lain, sudah terurut
    print()
    print("Alternatif lain:")
    for i in range(1, len(urutan)):
        k = urutan[i]
        if kepadatan[k] >= 80:
            status = "SANGAT RAMAI"
        elif kepadatan[k] >= 50:
            status = "SEDANG"
        else:
            status = "SEPI"
        print(i, ".", kantin[k], "->", kepadatan[k], "% ->", status, "|",
              jarak_rata[k], "m |", kosong[k], "kursi kosong")