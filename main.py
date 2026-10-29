# Interfejs graficzny aplikacji
import customtkinter as ctk
import threading
import logging
import tkinter as tk
import config
import sys
from tkinter import messagebox

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def zakoncz_z_bledem(tytul, tresc):
    # Ukryte okno, bo główne jeszcze nie istnieje
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(tytul, tresc)
    sys.exit(1)


# Sprawdzenie klucza przed importem ai_engine, który bez klucza kończy się błędem
if not config.GEMINI_API_KEY:
    zakoncz_z_bledem(
        "Brak klucza API",
        "Nie znaleziono klucza GEMINI_API_KEY.\n\n"
        "Upewnij się, że plik .env leży obok main.exe (albo w katalogu projektu) "
        "i zawiera linię GEMINI_API_KEY=twój_klucz."
    )

import ai_engine
import database
import walidacja
import formatowanie

try:
    database.stworz_tabele()
except database.DatabaseError as e:
    zakoncz_z_bledem(
        "Błąd połączenia z bazą danych",
        f"Nie można połączyć się z bazą danych MySQL.\n\n"
        f"Szczegóły błędu:\n{e}\n\n"
        f"Upewnij się, że:\n"
        f"1. Twój lokalny serwer MySQL (np. XAMPP) jest WŁĄCZONY.\n"
        f"2. Baza danych o nazwie '{config.DB_NAME}' została utworzona w phpMyAdmin.\n"
        f"3. Dane połączenia w pliku .env są poprawne."
    )
except Exception as e:
    # Inny błąd niż brak połączenia z bazą
    zakoncz_z_bledem("Nieoczekiwany błąd", f"Aplikacja nie mogła się uruchomić:\n{e}")

# Ustawienia wyglądu GUI
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Aplikacja(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Trener i Dietetyk - Moja Wersja")
        self.geometry("1000x850")

        self.poziom_zaawansowania = "Średnio zaawansowany"

        # Formularz i wyniki, widoczne dopiero po wyborze poziomu
        self.ramka_glowna = ctk.CTkFrame(self, fg_color="transparent")

        # Lewy panel
        self.ramka_lewa = ctk.CTkFrame(self.ramka_glowna, width=320)
        self.ramka_lewa.pack(side="left", fill="both", expand=False, padx=20, pady=20)

        ctk.CTkLabel(self.ramka_lewa, text="Parametry Klienta", font=("Arial", 22, "bold")).pack(pady=15)

        self.ramka_poziom_info = ctk.CTkFrame(self.ramka_lewa, fg_color="#2B2B2B", corner_radius=8)
        self.ramka_poziom_info.pack(pady=10, padx=20, fill="x")
        
        self.etykieta_poziomu = ctk.CTkLabel(
            self.ramka_poziom_info, 
            text="Poziom: Średnio zaaw.", 
            font=("Arial", 12, "bold")
        )
        self.etykieta_poziomu.pack(side="left", padx=10, pady=5)

        self.przycisk_zmien_poziom = ctk.CTkButton(
            self.ramka_poziom_info,
            text="Zmień",
            width=50,
            height=20,
            fg_color="#4F4F4F",
            hover_color="#363636",
            font=("Arial", 11, "bold"),
            command=self.pokaz_ekran_wyboru
        )
        self.przycisk_zmien_poziom.pack(side="right", padx=10, pady=5)

        self.wejscie_imie = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Imię klienta")
        self.wejscie_imie.pack(pady=10, padx=20, fill="x")

        self.wejscie_wiek = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Wiek (np. 25)")
        self.wejscie_wiek.pack(pady=10, padx=20, fill="x")

        self.wejscie_waga = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Waga w kg (np. 80.5)")
        self.wejscie_waga.pack(pady=10, padx=20, fill="x")

        self.wejscie_wzrost = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Wzrost w cm (np. 180)")
        self.wejscie_wzrost.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.ramka_lewa, text="Uwagi prozdrowotne (Opcjonalnie):", font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        self.wejscie_uwagi = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Np. kontuzja kolana")
        self.wejscie_uwagi.pack(pady=(5, 10), padx=20, fill="x")

        ctk.CTkLabel(self.ramka_lewa, text="Czego nie lubisz w diecie (Opcjonalnie):",
                      font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        self.wejscie_wykluczenia = ctk.CTkEntry(self.ramka_lewa, placeholder_text="Np. pomidory, cebula, brokuły, nabiał")
        self.wejscie_wykluczenia.pack(pady=(5, 10), padx=20, fill="x")

        ctk.CTkLabel(self.ramka_lewa, text="Cel główny:", font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        cele = ["Budowa masy mięśniowej", "Redukcja tkanki tłuszczowej", "Utrzymanie wagi", "Poprawa kondycji"]
        self.wybor_celu = ctk.CTkComboBox(self.ramka_lewa, values=cele, state="readonly")
        self.wybor_celu.pack(pady=(5, 10), padx=20, fill="x")
        self.wybor_celu.set(cele[0])

        ctk.CTkLabel(self.ramka_lewa, text="Rodzaj planu:", font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        typy_planow = ["Plan Treningowy", "Plan Dietetyczny"]
        self.wybor_typu = ctk.CTkComboBox(self.ramka_lewa, values=typy_planow, state="readonly")
        self.wybor_typu.pack(pady=(5, 10), padx=20, fill="x")
        self.wybor_typu.set(typy_planow[0])

        ctk.CTkLabel(self.ramka_lewa, text="Liczba dni w tygodniu:", font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        opcje_dni = ["2", "3", "4", "5", "6", "7"]
        self.wybor_dni = ctk.CTkComboBox(self.ramka_lewa, values=opcje_dni, state="readonly")
        self.wybor_dni.pack(pady=(5, 20), padx=20, fill="x")
        self.wybor_dni.set("3")

        ctk.CTkLabel(self.ramka_lewa, text="Priorytetowa partia (tylko trening):", font=("Arial", 12)).pack(pady=(15, 0), padx=20, anchor="w")
        partie = ["Brak priorytetu", "Klatka piersiowa", "Plecy", "Nogi", "Barki", "Ramiona (Biceps/Triceps)", "Brzuch"]
        self.wybor_partii = ctk.CTkComboBox(self.ramka_lewa, values=partie, state="readonly")
        self.wybor_partii.pack(pady=(5, 20), padx=20, fill="x")
        self.wybor_partii.set("Brak priorytetu")

        self.przycisk_generuj = ctk.CTkButton(self.ramka_lewa, text="Generuj Plan z AI", font=("Arial", 16, "bold"), height=40, command=self.rozpocznij_generowanie)
        self.przycisk_generuj.pack(pady=25, padx=20, fill="x")

        self.przycisk_historia = ctk.CTkButton(self.ramka_lewa, text="Zobacz Historię Planów", fg_color="#4F4F4F", hover_color="#363636", command=self.pokaz_historie)
        self.przycisk_historia.pack(pady=5, padx=20, fill="x")

        # Prawy panel
        self.ramka_prawa = ctk.CTkFrame(self.ramka_glowna)
        self.ramka_prawa.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        ctk.CTkLabel(self.ramka_prawa, text="Wygenerowany Plan:", font=("Arial", 22, "bold")).pack(pady=10)

        self.pole_tekstowe = ctk.CTkTextbox(self.ramka_prawa, wrap="word", font=("Arial", 14), activate_scrollbars=True)
        self.pole_tekstowe.pack(fill="both", expand=True, padx=20, pady=20)
        self._skonfiguruj_tagi(self.pole_tekstowe)

        # Ekran startowy z wyborem poziomu zaawansowania
        self.ramka_wyboru_poziomu = ctk.CTkFrame(self, fg_color="transparent")
        
        self.kontener_wyboru = ctk.CTkFrame(self.ramka_wyboru_poziomu, fg_color="transparent")
        self.kontener_wyboru.pack(expand=True, fill="both")
        
        ctk.CTkLabel(
            self.kontener_wyboru, 
            text="Witaj w AI Trener i Dietetyk!", 
            font=("Arial", 32, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(100, 10))
        
        ctk.CTkLabel(
            self.kontener_wyboru, 
            text="Wybierz swój poziom zaawansowania, aby spersonalizować generowany plan:", 
            font=("Arial", 16),
            text_color="#A9A9A9"
        ).pack(pady=(0, 50))
        
        # Panel trzymający karty
        self.ramka_kart = ctk.CTkFrame(self.kontener_wyboru, fg_color="transparent")
        self.ramka_kart.pack(pady=20, padx=40, fill="x")
        
        self.stworz_karte_poziomu(
            self.ramka_kart, 
            tytul="Początkujący", 
            opis="Dopiero zaczynasz lub wracasz po długiej przerwie.\n\nSkupimy się na nauce prawidłowej techniki podstawowych ćwiczeń, adaptacji ścięgien i stawów oraz pełnym bezpieczeństwie.\n\nBez zaawansowanych metod intensyfikacji.",
            kolor="#1F6AA5",
            hover_kolor="#2980B9",
            poziom="Początkujący"
        )
        
        self.stworz_karte_poziomu(
            self.ramka_kart, 
            tytul="Średnio zaawansowany", 
            opis="Trenujesz systematycznie od kilku miesięcy i znasz poprawny ruch.\n\nZoptymalizujemy objętość i intensywność serii, skupimy się na progresywnym przeładowaniu oraz wprowadzimy podstawowe techniki intensyfikacji.",
            kolor="#2B8E5B",
            hover_kolor="#2ECC71",
            poziom="Średnio zaawansowany"
        )
        
        self.stworz_karte_poziomu(
            self.ramka_kart, 
            tytul="Zaawansowany", 
            opis="Masz wieloletni staż treningowy i potrafisz bezpiecznie trenować blisko upadku.\n\nWprowadzimy zaawansowane metody stymulacji hipertrofii (superserie, drop-sety, rest-pause) oraz wysoką objętość i intensywność.",
            kolor="#C0392B",
            hover_kolor="#E74C3C",
            poziom="Zaawansowany"
        )

        self.pokaz_ekran_wyboru()

    def stworz_karte_poziomu(self, rodzic, tytul, opis, kolor, hover_kolor, poziom):
        karta = ctk.CTkFrame(rodzic, width=280, height=420, corner_radius=15, border_width=2,
                              border_color="#3A3A3A", fg_color="#1E1E1E")
        karta.pack(side="left", padx=20, fill="both", expand=True)
        karta.pack_propagate(False)

        lbl_tytul = ctk.CTkLabel(karta, text=tytul, font=("Arial", 20, "bold"), text_color=kolor)
        lbl_tytul.pack(pady=(30, 20))

        lbl_opis = ctk.CTkLabel(
            karta, 
            text=opis, 
            font=("Arial", 13), 
            text_color="#D3D3D3", 
            wraplength=240, 
            justify="center"
        )
        lbl_opis.pack(pady=10, padx=15, fill="both", expand=True)

        btn_wybierz = ctk.CTkButton(
            karta, 
            text="Wybierz", 
            fg_color=kolor, 
            hover_color=hover_kolor,
            font=("Arial", 15, "bold"),
            height=45,
            command=lambda: self.wybierz_poziom(poziom)
        )
        btn_wybierz.pack(pady=(15, 30), padx=30, fill="x")

    def pokaz_ekran_wyboru(self):
        self.ramka_glowna.pack_forget()
        self.ramka_wyboru_poziomu.pack(fill="both", expand=True)

    def wybierz_poziom(self, poziom):
        self.poziom_zaawansowania = poziom
        skrot = poziom
        if poziom == "Średnio zaawansowany":
            skrot = "Średnio zaaw."
        
        self.etykieta_poziomu.configure(text=f"Poziom: {skrot}")
        self.ramka_wyboru_poziomu.pack_forget()
        self.ramka_glowna.pack(fill="both", expand=True)

    def rozpocznij_generowanie(self):
        typ = self.wybor_typu.get()
        cel = self.wybor_celu.get()
        uwagi_str = self.wejscie_uwagi.get().strip()
        wykluczenia_str = self.wejscie_wykluczenia.get().strip()
        liczba_dni = self.wybor_dni.get()
        priorytet_partia = self.wybor_partii.get()

        try:
            imie = walidacja.waliduj_imie(self.wejscie_imie.get())
            wiek, waga, wzrost = walidacja.waliduj_dane_klienta(
                self.wejscie_wiek.get(), self.wejscie_waga.get(), self.wejscie_wzrost.get()
            )
        except ValueError as e:
            self.pokaz_blad(f"BŁĄD: {e}")
            return

        self.przycisk_generuj.configure(state="disabled", text="Generowanie...")
        self.pole_tekstowe.delete("0.0", "end")
        self.pole_tekstowe.insert("0.0", "Łączenie z serwerami Google Gemini AI...")

        self.dane_do_wyslania = (typ, imie, wiek, waga, wzrost, cel, uwagi_str, liczba_dni, priorytet_partia, self.poziom_zaawansowania, wykluczenia_str)
        watek = threading.Thread(target=self.generuj_i_wyswietl)
        watek.start()

    def generuj_i_wyswietl(self):
        typ, imie, wiek, waga, wzrost, cel, uwagi, liczba_dni, priorytet_partia, poziom_zaawansowania, wykluczenia = self.dane_do_wyslania

        try:
            odpowiedz_ai = ai_engine.generuj_plan(typ, wiek, waga, wzrost, cel, uwagi, liczba_dni, priorytet_partia, poziom_zaawansowania, wykluczenia)

            try:
                id_uzytkownika = database.znajdz_lub_stworz_uzytkownika(imie, wiek, waga, wzrost, cel)
                database.zapisz_plan(typ, odpowiedz_ai, id_uzytkownika)
            except database.DatabaseError as e:
                logger.error("Błąd zapisu planu do bazy: %s", e)
                odpowiedz_ai += f"\n\n{'='*70}\n[UWAGA: Plan wygenerowano, ale NIE udało się go zapisać w bazie danych: {e}]"
        except ai_engine.BladAI as e:
            # Brak planu, więc bez zapisu do bazy
            odpowiedz_ai = str(e)
        except Exception as e:
            logger.error("Nieoczekiwany błąd podczas generowania planu: %s", e)
            odpowiedz_ai = f"Wystąpił nieoczekiwany błąd: {e}"

        self.pole_tekstowe.delete("0.0", "end")
        self._wstaw_z_formatowaniem(self.pole_tekstowe, odpowiedz_ai)
        self.przycisk_generuj.configure(state="normal", text="Generuj Plan z AI")

    def pokaz_blad(self, wiadomosc):
        self.pole_tekstowe.delete("0.0", "end")
        self.pole_tekstowe.insert("0.0", wiadomosc)

    def _skonfiguruj_tagi(self, textbox):
        textbox.tag_config("naglowek", foreground="#3B8ED0", underline=True, spacing1=12, spacing3=4)
        textbox.tag_config("wpis_naglowek", foreground="#A9A9A9", underline=True, spacing1=6, spacing3=4)

    def _wstaw_z_formatowaniem(self, textbox, tekst):
        tekst = formatowanie.oczysc_markdown(tekst)
        for linia in tekst.split("\n"):
            tag = "naglowek" if formatowanie.czy_naglowek(linia) else ""
            textbox.insert("end", linia + "\n", tag)

    def pokaz_historie(self):
        okno_historii = ctk.CTkToplevel(self)
        okno_historii.title("Historia Planów (MySQL)")
        okno_historii.geometry("750x550")
        okno_historii.attributes('-topmost', True) 

        ctk.CTkLabel(okno_historii, text="Plany zapisane w bazie MySQL:", font=("Arial", 20, "bold")).pack(pady=10)

        pole_historii = ctk.CTkTextbox(okno_historii, wrap="word", font=("Arial", 13))
        pole_historii.pack(fill="both", expand=True, padx=20, pady=20)
        self._skonfiguruj_tagi(pole_historii)

        try:
            plany = database.pobierz_plany()
        except database.DatabaseError as e:
            messagebox.showerror("Błąd bazy danych", f"Nie udało się pobrać historii planów:\n{e}")
            okno_historii.destroy()
            return

        if not plany:
            pole_historii.insert("0.0", "Baza danych MySQL jest pusta.")
        else:
            for plan in plany:
                id_planu, typ, tresc, data, imie = plan[0], plan[1], plan[2], plan[3], plan[4]
                imie_wyswietlane = imie if imie else "Nieznany klient"
                naglowek_wpisu = f"--- [DATA ZAPISU: {data}] {typ.upper()} dla: {imie_wyswietlane} (ID: {id_planu}) ---\n\n"
                pole_historii.insert("end", naglowek_wpisu, "wpis_naglowek")
                self._wstaw_z_formatowaniem(pole_historii, tresc)
                pole_historii.insert("end", f"\n{'='*70}\n\n")

if __name__ == "__main__":
    app = Aplikacja()
    app.mainloop()