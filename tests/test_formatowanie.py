import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import formatowanie


class TestOczyscMarkdown(unittest.TestCase):

    def test_usuwa_pogrubienie(self):
        self.assertEqual(formatowanie.oczysc_markdown("**Dzień 1**"), "Dzień 1")

    def test_usuwa_naglowki_hash(self):
        self.assertEqual(formatowanie.oczysc_markdown("### Dzień 1"), "Dzień 1")

    def test_usuwa_wypunktowanie_gwiazdka(self):
        self.assertEqual(formatowanie.oczysc_markdown("* Przysiady"), "Przysiady")

    def test_nie_rusza_numerowanej_listy(self):
        self.assertEqual(formatowanie.oczysc_markdown("1. Przysiady"), "1. Przysiady")


class TestCzyNaglowek(unittest.TestCase):

    def test_wykrywa_dzien(self):
        self.assertTrue(formatowanie.czy_naglowek("DZIEŃ 1: Klatka piersiowa"))

    def test_wykrywa_posilek(self):
        self.assertTrue(formatowanie.czy_naglowek("POSIŁEK 2: Obiad"))

    def test_zwykla_linia_nie_jest_naglowkiem(self):
        self.assertFalse(formatowanie.czy_naglowek("1. Wyciskanie sztangi 4x8"))


if __name__ == "__main__":
    unittest.main()
