import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
import cv2  # Pustaka untuk mengambil foto dari kamera

# Nama file database dan folder foto
FILE_NAME = "absensi_guru_berfoto.csv"
FOLDER_FOTO = "foto_bukti_absen"

# Membuat file CSV dan folder foto jika belum ada
def inisialisasi_sistem():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Guru", "Jam Datang", "Tanggal", "Nama File Foto"])
            
    if not os.path.exists(FOLDER_FOTO):
        os.makedirs(FOLDER_FOTO)

def dapatkan_jam_sekarang():
    return datetime.now().strftime("%H:%M:%S")

def dapatkan_tanggal_sekarang():
    return datetime.now().strftime("%Y-%m-%d")

# Fungsi Utama: Ambil Foto dan Simpan Data
def ambil_foto_dan_absen():
    nama = entry_nama.get().strip()
    jam = entry_jam.get().strip()
    tanggal = dapatkan_tanggal_sekarang()
    
    if not nama or not jam:
        messagebox.showwarning("Peringatan", "Nama dan Jam Datang tidak boleh kosong!")
        return
    
    # 1. NYALAKAN KAMERA & AMBIL FOTO
    # Angka 0 berarti menggunakan kamera utama/webcam bawaan
    kamera = cv2.VideoCapture(0)
    
    if not kamera.isOpened():
        messagebox.showerror("Error", "Kamera tidak terdeteksi! Pastikan webcam aktif.")
        return
    
    # Beri jeda sebentar agar kamera menyesuaikan cahaya
    for i in range(10):
        ret, frame = kamera.read()
        
    if ret:
        # Format nama file foto: Nama_Tanggal_Jam.jpg (menghindari karakter ilegal untuk nama file)
        waktu_file = datetime.now().strftime("%H%M%S")
        nama_bersih = "".join(x for x in nama if x.isalnum() or x in "._- ")
        nama_file_foto = f"{nama_bersih}_{tanggal}_{waktu_file}.jpg"
        path_foto = os.path.join(FOLDER_FOTO, nama_file_foto)
        
        # Simpan gambar wajah guru
        cv2.imwrite(path_foto, frame)
    else:
        messagebox.showerror("Error", "Gagal mengambil gambar dari kamera.")
        kamera.release()
        return
        
    kamera.release() # Matikan kamera kembali
    
    # 2. SIMPAN DATA KE CSV
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([nama, jam, tanggal, nama_file_foto])
    
    messagebox.showinfo("Sukses", f"Absen berhasil!\nFoto bukti telah disimpan untuk {nama}.")
    
    # Reset input dan perbarui tabel
    entry_nama.delete(0, tk.END)
    entry_jam.delete(0, tk.END)
    entry_jam.insert(0, dapatkan_jam_sekarang())
    muat_data_tabel()

# Fungsi menampilkan data ke tabel aplikasi
def muat_data_tabel():
    for row in tabel.get_children():
        tabel.delete(row)
        
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # Lewati header
            for row in reader:
                tabel.insert("", tk.END, values=row)

# --- GUI INTERFACE ---
root = tk.Tk()
root.title("Aplikasi Absensi Guru + Bukti Foto")
root.geometry("650x480")
root.resizable(False, False)

# Jalankan inisialisasi awal
inisialisasi_sistem()

# Judul
label_judul = tk.Label(root, text="ABSENSI KEHADIRAN GURU", font=("Arial", 16, "bold"))
label_judul.pack(pady=15)

# Frame Input
frame_input = tk.LabelFrame(root, text=" Input Data Absen ", padx=10, pady=10)
frame_input.pack(pady=10, fill="x", padx=20)

# Input Nama
tk.Label(frame_input, text="Nama Guru:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
entry_nama = tk.Entry(frame_input, font=("Arial", 10), width=40)
entry_nama.grid(row=0, column=1, pady=5, padx=5)

# Input Jam Datang
tk.Label(frame_input, text="Jam Datang:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
entry_jam = tk.Entry(frame_input, font=("Arial", 10), width=40)
entry_jam.grid(row=1, column=1, pady=5, padx=5)
entry_jam.insert(0, dapatkan_jam_sekarang())

# Tombol Absen + Ambil Foto
btn_simpan = tk.Button(frame_input, text="AMBIL FOTO & ABSEN", command=ambil_foto_dan_absen, bg="#008CBA", fg="white", font=("Arial", 10, "bold"), padx=10)
btn_simpan.grid(row=2, column=0, columnspan=2, pady=10, sticky="e")

# Frame Tabel Riwayat
frame_tabel = tk.LabelFrame(root, text=" Riwayat Absen & Bukti Foto ", padx=10, pady=10)
frame_tabel.pack(pady=10, fill="both", expand=True, padx=20)

# Membuat Tabel
kolom = ("Nama Guru", "Jam Datang", "Tanggal", "Nama File Foto")
tabel = ttk.Treeview(frame_tabel, columns=kolom, show="headings", height=6)
tabel.heading("Nama Guru", text="Nama Guru")
tabel.heading("Jam Datang", text="Jam Datang")
tabel.heading("Tanggal", text="Tanggal")
tabel.heading("Nama File Foto", text="Nama File Foto")

tabel.column("Nama Guru", width=150)
tabel.column("Jam Datang", width=90, anchor="center")
tabel.column("Tanggal", width=100, anchor="center")
tabel.column("Nama File Foto", width=250)
tabel.pack(fill="both", expand=True)

muat_data_tabel()

root.mainloop()