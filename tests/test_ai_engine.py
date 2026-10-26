import unittest
from unittest import mock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ai_engine


class TestBudowaPromptu(unittest.TestCase):

    def test_dane_klienta_sa_w_promptcie(self):
        prompt = ai_engine.zbuduj_prompt(
            "Plan Treningowy", 25, 80.5, 180, "Budowa masy mięśniowej",
            "", "3", "Brak priorytetu", "Początkujący", ""
        )
        self.assertIn("25 lat", prompt)
        self.assertIn("80.5 kg", prompt)
        self.assertIn("180 cm", prompt)

    def test_brak_uwag_wstawia_domyslny_tekst(self):
        prompt = ai_engine.zbuduj_prompt(
            "Plan Treningowy", 25, 80, 180, "Redukcja tkanki tłuszczowej",
            "", "3", "Brak priorytetu", "Średnio zaawansowany", ""
        )
        self.assertIn("Brak specjalnych uwag i przeciwwskazań.", prompt)

    def test_wykluczenia_trafiaja_do_promptu(self):
        prompt = ai_engine.zbuduj_prompt(
            "Plan Dietetyczny", 30, 70, 170, "Redukcja tkanki tłuszczowej",
            "", "4", "Brak priorytetu", "Zaawansowany", "brokuły, cebula"
        )
        self.assertIn("brokuły, cebula", prompt)

    def test_poziom_zaawansowania_wplywa_na_prompt(self):
        prompt = ai_engine.zbuduj_prompt(
            "Plan Treningowy", 25, 80, 180, "Budowa masy mięśniowej",
            "", "3", "Brak priorytetu", "Zaawansowany", ""
        )
        self.assertIn("Zaawansowany", prompt)


# Klient Gemini podmieniony na atrapę, żeby testy nie łączyły się z API
class TestGenerowaniePlanu(unittest.TestCase):

    def test_zwraca_tekst_odpowiedzi(self):
        with mock.patch.object(ai_engine, "client") as klient:
            klient.models.generate_content.return_value.text = "DZIEŃ 1: Klatka"
            wynik = ai_engine.generuj_plan("Plan Treningowy", 25, 80, 180, "Utrzymanie wagi", "", "3")
        self.assertEqual(wynik, "DZIEŃ 1: Klatka")

    def test_brak_polaczenia_rzuca_blad_ai(self):
        with mock.patch.object(ai_engine, "client") as klient:
            klient.models.generate_content.side_effect = ConnectionError("brak sieci")
            with self.assertRaises(ai_engine.BladAI):
                ai_engine.generuj_plan("Plan Treningowy", 25, 80, 180, "Utrzymanie wagi", "", "3")

    def test_pusta_odpowiedz_rzuca_blad_ai(self):
        with mock.patch.object(ai_engine, "client") as klient:
            klient.models.generate_content.return_value.text = None
            with self.assertRaises(ai_engine.BladAI):
                ai_engine.generuj_plan("Plan Treningowy", 25, 80, 180, "Utrzymanie wagi", "", "3")


if __name__ == "__main__":
    unittest.main()
