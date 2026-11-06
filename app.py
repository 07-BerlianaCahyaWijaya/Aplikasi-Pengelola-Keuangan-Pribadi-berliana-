# Versi 1.0 - Aplikasi Pengelola Keuangan Pribadi Siap Rilis
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "keuangan.json"

def muat_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def simpan_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

class AplikasiKeuangan:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengelola Keuangan Pribadi")
        self.root.geometry("600x500")
        
        self.data = muat_data()
        
        # --- FRAME INPUT ---
        frame_input = ttk.LabelFrame(self.root, text=" Tambah Transaksi ")
        frame_input.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_input, text="Tipe:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_tipe = ttk.Combobox(frame_input, values=["Pemasukan", "Pengeluaran"], state="readonly")
        self.combo_tipe.current(0)
        self.combo_tipe.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Keterangan:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_ket = ttk.Entry(frame_input)
        self.entry_ket.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Jumlah (Rp):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_jumlah = ttk.Entry(frame_input)
        self.entry_jumlah.grid(row=1, column=1, padx=5, pady=5)
        
        btn_tambah = ttk.Button(frame_input, text="Simpan Transaksi", command=self.tambah_transaksi)
        btn_tambah.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # --- TABEL DATA ---
        frame_tabel = ttk.LabelFrame(self.root, text=" Catatan Keuangan ")
        frame_tabel.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("id", "tanggal", "tipe", "keterangan", "jumlah")
        self.tabel = ttk.Treeview(frame_tabel, columns=columns, show="headings")
        
        self.tabel.heading("id", text="ID")
        self.tabel.heading("tanggal", text="Tanggal")
        self.tabel.heading("tipe", text="Tipe")
        self.tabel.heading("keterangan", text="Keterangan")
        self.tabel.heading("jumlah", text="Jumlah (Rp)")
        
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("tanggal", width=130, anchor="center")
        self.tabel.column("tipe", width=90, anchor="center")
        self.tabel.column("keterangan", width=150)
        self.tabel.column("jumlah", width=100, anchor="e")
        
        self.tabel.pack(fill="both", expand=True, side="left", padx=5, pady=5)
        
        # --- FRAME SALDO & HAPUS ---
        frame_bawah = ttk.Frame(self.root)
        frame_bawah.pack(fill="x", padx=10, pady=5)
        
        self.lbl_saldo = ttk.Label(frame_bawah, text="Sisa Saldo: Rp 0", font=("Helvetica", 11, "bold"))
        self.lbl_saldo.pack(side="left", padx=5)
        
        btn_hapus = ttk.Button(frame_bawah, text="Hapus Transaksi Terpilih", command=self.hapus_transaksi)
        btn_hapus.pack(side="right", padx=5)
        
        self.perbarui_tabel()

    def perbarui_tabel(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
            
        total_pemasukan = 0
        total_pengeluaran = 0
        
        for item in self.data:
            jumlah_str = f"Rp {item['jumlah']:,.2f}"
            self.tabel.insert("", "end", values=(item["id"], item["tanggal"], item["tipe"], item["keterangan"], jumlah_str))
            
            if item["tipe"] == "Pemasukan":
                total_pemasukan += item["jumlah"]
            else:
                total_pengeluaran += item["jumlah"]
                
        saldo = total_pemasukan - total_pengeluaran
        self.lbl_saldo.config(text=f"Sisa Saldo: Rp {saldo:,.2f}")

    def tambah_transaksi(self):
        tipe = self.combo_tipe.get()
        keterangan = self.entry_ket.get().strip()
        jumlah_raw = self.entry_jumlah.get().strip()
        
        if not keterangan:
            messagebox.showwarning("Peringatan", "Keterangan tidak boleh kosong!")
            return
            
        try:
            jumlah = float(jumlah_raw)
            if jumlah <= 0:
                messagebox.showwarning("Peringatan", "Jumlah harus lebih besar dari 0!")
                return
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah harus berupa angka!")
            return
            
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        new_item = {
            "id": len(self.data) + 1,
            "tanggal": tanggal,
            "tipe": tipe,
            "keterangan": keterangan,
            "jumlah": jumlah
        }
        
        self.data.append(new_item)
        simpan_data(self.data)
        self.perbarui_tabel()
        
        self.entry_ket.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        messagebox.showinfo("Sukses", "Transaksi berhasil ditambahkan!")

    def hapus_transaksi(self):
        selected_item = self.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dihapus dari tabel!")
            return
            
        item_data = self.tabel.item(selected_item)
        target_id = item_data["values"][0]
        
        self.data = [item for item in self.data if item["id"] != target_id]
        
        for index, item in enumerate(self.data):
            item["id"] = index + 1
            
        simpan_data(self.data)
        self.perbarui_tabel()
        messagebox.showinfo("Sukses", "Transaksi berhasil dihapus!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiKeuangan(root)
    root.mainloop()
