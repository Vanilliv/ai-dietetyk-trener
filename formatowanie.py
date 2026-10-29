# Formatowanie tekstu planu przed wyświetleniem
import re

NAGLOWEK_DNIA = re.compile(r'^\s*DZIE[NŃ]\s+\d+', re.IGNORECASE)
NAGLOWEK_POSILKU = re.compile(r'^\s*POSI[LŁ]EK\s+\d+', re.IGNORECASE)


# Pole tekstowe nie obsługuje Markdown, więc znaki typu ** i # są usuwane
def oczysc_markdown(tekst):
    tekst = re.sub(r'\*\*(.+?)\*\*', r'\1', tekst)
    tekst = re.sub(r'__(.+?)__', r'\1', tekst)
    tekst = re.sub(r'~~(.+?)~~', r'\1', tekst)
    tekst = re.sub(r'^\s*#{1,6}\s*', '', tekst, flags=re.MULTILINE)
    tekst = re.sub(r'^\s*[*-]\s+', '', tekst, flags=re.MULTILINE)
    return tekst


# Nagłówki w stylu "DZIEŃ 1:" i "POSIŁEK 2:"
def czy_naglowek(linia):
    return bool(NAGLOWEK_DNIA.match(linia) or NAGLOWEK_POSILKU.match(linia))
