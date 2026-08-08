import unittest
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


if __name__ == "__main__":
    unittest.main()
