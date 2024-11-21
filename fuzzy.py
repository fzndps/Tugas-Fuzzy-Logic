# Import library yang dibutuhkan
import numpy as np

class FuzzyTsukamoto:
    
    def __init__(self):
        # Batasan untuk setiap variabel
        self.min_permintaan = 1000  # Minimal permintaan yang dapat diproses
        self.max_permintaan = 5000  # Maksimal permintaan yang dapat diproses
        self.min_stok = 100         # Minimal stok yang dapat diproses
        self.max_stok = 1000        # Maksimal stok yang dapat diproses
        self.min_produksi = 1000    # Minimal jumlah produksi
        self.max_produksi = 6000    # Maksimal jumlah produksi

    def fuzzy_permintaan_rendah(self, x):
        """Fungsi keanggotaan untuk permintaan rendah"""
        if x <= self.min_permintaan:
            return 1
        elif x >= self.max_permintaan:
            return 0
        else:
            return (self.max_permintaan - x) / (self.max_permintaan - self.min_permintaan)

    def fuzzy_permintaan_tinggi(self, x):
        """Fungsi keanggotaan untuk permintaan tinggi"""
        if x <= self.min_permintaan:
            return 0
        elif x >= self.max_permintaan:
            return 1
        else:
            return (x - self.min_permintaan) / (self.max_permintaan - self.min_permintaan)

    def fuzzy_stok_sedikit(self, x):
        """Fungsi keanggotaan untuk stok sedikit"""
        if x <= self.min_stok:
            return 1
        elif x >= self.max_stok:
            return 0
        else:
            return (self.max_stok - x) / (self.max_stok - self.min_stok)

    def fuzzy_stok_banyak(self, x):
        """Fungsi keanggotaan untuk stok banyak"""
        if x <= self.min_stok:
            return 0
        elif x >= self.max_stok:
            return 1
        else:
            return (x - self.min_stok) / (self.max_stok - self.min_stok)

    def fuzzy_produksi_berkurang(self, alpha):
        """Fungsi keanggotaan untuk produksi berkurang"""
        return self.max_produksi - alpha * (self.max_produksi - self.min_produksi)

    def fuzzy_produksi_bertambah(self, alpha):
        """Fungsi keanggotaan untuk produksi bertambah"""
        return self.min_produksi + alpha * (self.max_produksi - self.min_produksi)

    def inferensi(self, permintaan, stok):
        """
        Melakukan inferensi fuzzy menggunakan metode Tsukamoto
        
        Parameters:
        permintaan (float): Jumlah permintaan produk
        stok (float): Jumlah stok produk
        
        Returns:
        float: Jumlah produksi yang direkomendasikan
        """
        # Fuzzifikasi
        permintaan_rendah = self.fuzzy_permintaan_rendah(permintaan)
        permintaan_tinggi = self.fuzzy_permintaan_tinggi(permintaan)
        stok_sedikit = self.fuzzy_stok_sedikit(stok)
        stok_banyak = self.fuzzy_stok_banyak(stok)

        # Rule-rule fuzzy
        # R1: IF permintaan RENDAH AND stok BANYAK THEN produksi BERKURANG
        alpha_1 = min(permintaan_rendah, stok_banyak)
        z1 = self.fuzzy_produksi_berkurang(alpha_1)

        # R2: IF permintaan RENDAH AND stok SEDIKIT THEN produksi BERKURANG
        alpha_2 = min(permintaan_rendah, stok_sedikit)
        z2 = self.fuzzy_produksi_berkurang(alpha_2)

        # R3: IF permintaan TINGGI AND stok BANYAK THEN produksi BERKURANG
        alpha_3 = min(permintaan_tinggi, stok_banyak)
        z3 = self.fuzzy_produksi_berkurang(alpha_3)

        # R4: IF permintaan TINGGI AND stok SEDIKIT THEN produksi BERTAMBAH
        alpha_4 = min(permintaan_tinggi, stok_sedikit)
        z4 = self.fuzzy_produksi_bertambah(alpha_4)

        # Defuzzifikasi (weighted average)
        total_alpha = alpha_1 + alpha_2 + alpha_3 + alpha_4
        if total_alpha == 0:
            return (self.min_produksi + self.max_produksi) / 2

        z = (alpha_1 * z1 + alpha_2 * z2 + alpha_3 * z3 + alpha_4 * z4) / total_alpha
        return z

def validasi_input(prompt, min_val, max_val):
    """
    Fungsi untuk memvalidasi input dari pengguna
    """
    while True:
        try:
            nilai = float(input(prompt))
            if min_val <= nilai <= max_val:
                return nilai
            else:
                print(f"Nilai harus antara {min_val} dan {max_val}")
        except ValueError:
            print("Masukkan angka yang valid!")

def main():
    print("\n=== SISTEM FUZZY TSUKAMOTO PENENTUAN JUMLAH PRODUKSI ===")
    print("Batasan nilai:")
    print("- Permintaan: 1000-5000 unit")
    print("- Stok: 100-1000 unit")
    
    fuzzy = FuzzyTsukamoto()
    
    # Input dari pengguna dengan validasi
    permintaan = validasi_input("\nMasukkan jumlah permintaan (1000-5000): ", 
                               fuzzy.min_permintaan, 
                               fuzzy.max_permintaan)
    
    stok = validasi_input("Masukkan jumlah stok (100-1000): ", 
                         fuzzy.min_stok, 
                         fuzzy.max_stok)
    
    # Hitung hasil produksi
    hasil_produksi = fuzzy.inferensi(permintaan, stok)
    
    # Tampilkan hasil
    print("\n=== HASIL PERHITUNGAN ===")
    print(f"Permintaan: {permintaan:.0f} unit")
    print(f"Stok: {stok:.0f} unit")
    print(f"Jumlah Produksi yang Direkomendasikan: {hasil_produksi:.0f} unit")

if __name__ == "__main__":
    main()