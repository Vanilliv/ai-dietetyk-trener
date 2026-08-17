#czyszczenie i formatowanie tekstu planu przed wyswietleniem w GUI
import re

NAGLOWEK_DNIA = re.compile(r'^\s*DZIE[NŃ]\s+\d+', re.IGNORECASE)
NAGLOWEK_POSILKU = re.compile(r'^\s*POSI[LŁ]EK\s+\d+', re.IGNORECASE)


def oczysc_markdown(tekst):
    """Usuwa pozostałości składni Markdown - pole tekstowe w GUI wyświetla czysty tekst, nie renderuje **, #, itp."""
    tekst = re.sub(r'\*\*(.+?)\*\*', r'\1', tekst)
    tekst = re.sub(r'__(.+?)__', r'\1', tekst)
    tekst = re.sub(r'~~(.+?)~~', r'\1', tekst)
    tekst = re.sub(r'^\s*#{1,6}\s*', '', tekst, flags=re.MULTILINE)
    tekst = re.sub(r'^\s*[*-]\s+', '', tekst, flags=re.MULTILINE)
    return tekst


def czy_naglowek(linia):
    """Sprawdza, czy dana linia to nagłówek dnia treningowego albo posiłku (do pogrubienia w GUI)."""
    return bool(NAGLOWEK_DNIA.match(linia) or NAGLOWEK_POSILKU.match(linia))
