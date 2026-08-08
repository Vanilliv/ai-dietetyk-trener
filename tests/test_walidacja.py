import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import walidacja


class TestWalidujImie(unittest.TestCase):

    def test_puste_imie_rzuca_blad(self):
        with self.assertRaises(ValueError):
            walidacja.waliduj_imie("   ")

    def test_poprawne_imie_jest_przycinane(self):
        self.assertEqual(walidacja.waliduj_imie("  Jan  "), "Jan")


class TestWalidujDaneKlienta(unittest.TestCase):

    def test_poprawne_dane(self):
        wiek, waga, wzrost = walidacja.waliduj_dane_klienta("25", "80.5", "180")
        self.assertEqual(wiek, 25)
        self.assertEqual(waga, 80.5)
        self.assertEqual(wzrost, 180.0)

    def test_przecinek_zamiast_kropki(self):
        _, waga, wzrost = walidacja.waliduj_dane_klienta("25", "80,5", "180,5")
        self.assertEqual(waga, 80.5)
        self.assertEqual(wzrost, 180.5)

    def test_puste_pole_rzuca_blad(self):
        with self.assertRaises(ValueError):
            walidacja.waliduj_dane_klienta("", "80", "180")

    def test_tekst_zamiast_liczby_rzuca_blad(self):
        with self.assertRaises(ValueError):
            walidacja.waliduj_dane_klienta("abc", "80", "180")

    def test_wiek_poza_zakresem_rzuca_blad(self):
        with self.assertRaises(ValueError):
            walidacja.waliduj_dane_klienta("150", "80", "180")

    def test_ujemna_waga_rzuca_blad(self):
        with self.assertRaises(ValueError):
            walidacja.waliduj_dane_klienta("25", "-10", "180")


if __name__ == "__main__":
    unittest.main()
