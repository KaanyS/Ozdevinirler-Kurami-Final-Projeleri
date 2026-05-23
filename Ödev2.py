

import time

class TuringPlateRecognizer:
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.current_state = "q0"
        self.step_count = 0

    def prepare_tape(self, plate_input: str):
        """Girdiyi şeride yerleştirir ve sonuna boşluk (_) sembolü ekler."""
        # Kullanıcın girdiği ham stringi listeye çeviriyoruz
        # Giriş karakterlerinin sınırlandırılması simülatör durumlarında test edilecek
        self.tape = list(plate_input) + ["_"]  # Bant sonu belirteci
        self.head_position = 0
        self.current_state = "q0"
        self.step_count = 0

    def print_step(self, read_sym, direction):
        """Her adımda mevcut durum, okunan sembol, kafa hareketi ve bandı gösterir."""
        tape_str = "".join(self.tape)
        print(f"Adım: {self.step_count:<2} | Durum: {self.current_state:<3} | Okunan: '{read_sym}' | Hareket: {direction} | Bant: {tape_str}")
        pointer = " " * (self.head_position + 55) + "▲"
        print(pointer)

    def run_simulation(self):
        print("\n=== TURING MAKİNESİ PLAKA DOĞRULAMA BAŞLIYOR ===")
        print(f"Giriş Şeridi: {''.join(self.tape)}\n" + "-"*75)

        rakamlar = set("0123456789")
        buyuk_harfler = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Kabul veya Red durumuna geçene kadar tek hat üzerinde ilerle
        while self.current_state not in ["q7", "q_red"]:
            # Eğer kafa şerit sınırlarının dışına çıkarsa güvenlik önlemi
            if self.head_position >= len(self.tape):
                self.current_state = "q_red"
                break

            read_symbol = self.tape[self.head_position]
            direction = "S"  # S: Sağa Hareket (Right)
            next_state = "q_red" # Varsayılan olarak kural dışı her şey RED durumuna fırlatır

            # --- SAF TURING DURUM GEÇİŞLERİ (δ) ---

            # q0: 1. Karakter Kontrolü -> Rakam (N) olmalı
            if self.current_state == "q0":
                if read_symbol in rakamlar:
                    next_state = "q1"

            # q1: 2. Karakter Kontrolü -> Rakam (N) olmalı
            elif self.current_state == "q1":
                if read_symbol in rakamlar:
                    next_state = "q2"

            # q2: 3. Karakter Kontrolü -> Büyük Harf (L) olmalı
            elif self.current_state == "q2":
                if read_symbol in buyuk_harfler:
                    next_state = "q3"

            # q3: 4. Karakter Kontrolü -> Büyük Harf (L) olmalı
            elif self.current_state == "q3":
                if read_symbol in buyuk_harfler:
                    next_state = "q4"

            # q4: 5. Karakter Kontrolü -> Rakam (N) olmalı
            elif self.current_state == "q4":
                if read_symbol in rakamlar:
                    next_state = "q5"

            # q5: 6. Karakter Kontrolü -> Rakam (N) olmalı
            elif self.current_state == "q5":
                if read_symbol in rakamlar:
                    next_state = "q6"

            # q6: 7. Karakter Kontrolü -> Rakam (N) olmalı
            elif self.current_state == "q6":
                if read_symbol in rakamlar:
                    next_state = "q7"

            # Adımı ekrana bas
            self.print_step(read_symbol, direction)

            # Durumu ve kafa konumunu güncelle
            self.current_state = next_state
            self.head_position += 1
            self.step_count += 1
            time.sleep(0.01)

        # q7 durumuna ulaşıldığında son bir uzunluk/boşluk kontrolü (Fazlalık karakter kontrolü)
        if self.current_state == "q7":
            final_symbol = self.tape[self.head_position]
            if final_symbol == "_":
                self.print_step(final_symbol, "H")  # H: Hareketsiz (Stay)
                print("\n" + "="*45)
                print("SONUÇ: KABUL (Plaka formatı %100 geçerli)")
                print("="*45)
                return "KABUL"
            else:
                # 7 karakterden sonra hala karakter geliyorsa (Örn: 55AB1234) RED
                self.current_state = "q_red"
                self.print_step(final_symbol, "H")

        print("\n" + "="*45)
        print("SONUÇ: RED (Geçersiz format veya karakter)")
        print("="*45)
        return "RED"

# --- Program Giriş Test Alanı ---
if __name__ == "__main__":
    recognizer = TuringPlateRecognizer()
    print("=" * 60)
    print("  Turing Makinesi Araç Plaka Formatı Tanıyıcı Simülasyonu")
    print("=" * 60)

    plaka = input("Lütfen doğrulanacak plaka bilgisini giriniz: ").strip()
    recognizer.prepare_tape(plaka)
    recognizer.run_simulation()
