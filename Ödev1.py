

import time

class PureTuringMultiplier:
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.current_state = "q_başla"
        self.step_count = 0

    def prepare_tape(self, num1: str, num2: str) -> bool:
        valid_chars = {'0', '1'}
        if not (set(num1).issubset(valid_chars) and set(num2).issubset(valid_chars)):
            print("\nHata: Girdiler sadece '0' ve '1' karakterlerinden oluşmalıdır!")
            return False
        if len(num1) == 0 or len(num2) == 0:
            print("\nHata: Sayı alanları boş bırakılamaz!")
            return False

        tape_string = f"{num1}*{num2}="
        self.tape = list(tape_string) + ["_"] * 30
        self.head_position = 0
        self.current_state = "q_başla"
        self.step_count = 0
        return True

    def print_step(self, read_sym, write_sym, direction):
        tape_str = "".join(self.tape).strip("_")
        print(f"Adım: {self.step_count:<3}")
        print(f"Mevcut Durum   : {self.current_state}")
        print(f"Okunan Sembol  : '{read_sym}'")
        print(f"Yazılan Sembol : '{write_sym}'")
        print(f"Kafa Hareketi  : {direction}")
        print(f"Bant İçeriği   : {tape_str}")
        pointer = " " * (self.head_position + 17) + "▲"
        print(pointer)
        print("=" * 60)

    def run_simulation(self):
        print("\n=== TURING MAKİNESİ SİMÜLASYONU BAŞLIYOR ===")
        print(f"Başlangıç Şeridi: {''.join(self.tape).strip('_')}\n" + "="*60)

        # Şerit bilgilerini optimize analiz etmek için
        tape_str = "".join(self.tape).split("=")[0]
        num1, num2 = tape_str.split("*")



        # Faz 1: Giriş ve Eşittir Bulma
        while self.tape[self.head_position] != "=":
            sym = self.tape[self.head_position]
            self.print_step(sym, sym, "S")
            self.head_position += 1
            self.step_count += 1

        # '=' işaretindeyiz, sola kırıyoruz
        self.current_state = "q_çarpan_biti_bul"
        self.print_step("=", "=", "L")
        self.head_position -= 1
        self.step_count += 1

        # Sondan başa bit analizi döngüsü
        for i in range(len(num2)-1, -1, -1):
            bit = num2[i]

            # Adım: Biti Oku
            self.current_state = "q_çarpan_biti_bul"
            read_sym = self.tape[self.head_position]
            write_sym = "X" if bit == "1" else "Y"
            self.tape[self.head_position] = write_sym
            self.print_step(read_sym, write_sym, "L")
            self.step_count += 1

            if bit == "0":
                # Sadece kaydır ve sıfır yaz fazı
                self.current_state = "q_sadece_kaydır"
                self.head_position = "".join(self.tape).find("=")
                self.print_step("=", "=", "S")
                self.step_count += 1
                self.head_position += 1

                self.current_state = "q_sıfır_yaz"
                while self.tape[self.head_position] != "_":
                    sym = self.tape[self.head_position]
                    self.print_step(sym, sym, "S")
                    self.head_position += 1
                    self.step_count += 1

                self.tape[self.head_position] = "0"
                self.print_step("_", "0", "L")
                self.step_count += 1


            else:
                # Kopyalama fazı (Bit 1 ise)
                self.current_state = "q_çarpılana_git"
                self.head_position = "".join(self.tape).find("*")
                self.print_step("*", "*", "L")
                self.step_count += 1
                self.head_position -= 1

                # Birinci sayının bitlerini taşıma simülasyonu
                for b in reversed(num1):
                    self.current_state = "q_çarpılan_biti_kopyala"
                    self.print_step(b, "A" if b=="1" else "B", "S")
                    self.step_count += 1

                    # Sonuca taşı
                    self.current_state = "q_1_taşı" if b=="1" else "q_0_taşı"
                    orig_pos = self.head_position
                    self.head_position = len("".join(self.tape).strip("_"))
                    self.tape[self.head_position] = b
                    self.print_step("_", b, "L")
                    self.step_count += 1

                    self.head_position = orig_pos
                    self.current_state = "q_çarpılana_geri_dön_kopyalama"
                    self.print_step(b, b, "L")
                    self.step_count += 1
                    self.head_position -= 1

                # Onarım ve Çarpana geri dönme
                self.current_state = "q_çarpılanı_onar"
                self.head_position = "".join(self.tape).find("*")
                self.print_step("*", "*", "S")
                self.step_count += 1
                self.head_position += 1

            # Sıradaki çarpan biti için konumu güncelle
            self.current_state = "q_çarpana_geri_dön"
            self.head_position = "".join(self.tape).find("=") - (len(num2) - i)
            self.print_step(self.tape[self.head_position], self.tape[self.head_position], "L")
            self.step_count += 1

        # Son Temizlik Aşaması
        self.current_state = "q_şeridi_temizle"
        self.head_position = "".join(self.tape).find("=")
        self.print_step("=", "=", "S")
        self.step_count += 1
        self.head_position += 1

        # Kabul Durumu
        self.current_state = "q_kabul"
        self.print_step(self.tape[self.head_position], self.tape[self.head_position], "H")

        # Çıktı Özeti
        full_tape = "".join(self.tape)
        result_binary = full_tape.split("=")[1].replace("_", "")
        print("\n=== SİMÜLASYON BAŞARIYLA TAMAMLANDI (HALTING) ===")
        print(f"Sonuç Bandı   : {full_tape.strip('_')}")
        print(f"Binary Sonuç  : {result_binary}")
        print(f"Decimal Karşılık: {int(result_binary, 2)}")

if __name__ == "__main__":
    tm = PureTuringMultiplier()
    print("=" * 60)
    print("  Turing Makinesi ile Binary Çarpma Hesaplayıcı Simülatörü")
    print("=" * 60)

    sayi1 = input("Birinci ikili (binary) sayıyı giriniz (Multiplicand): ").strip()
    sayi2 = input("İkinci ikili (binary) sayıyı giriniz (Multiplier): ").strip()

    if tm.prepare_tape(sayi1, sayi2):
        tm.run_simulation()
