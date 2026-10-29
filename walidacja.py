# Walidacja danych z formularza

WIEK_MAX = 120
WAGA_MAX = 400
WZROST_MAX = 250


def waliduj_imie(imie_str):
    imie_str = imie_str.strip()
    if not imie_str:
        raise ValueError("Proszę podać imię klienta.")
    return imie_str


def waliduj_dane_klienta(wiek_str, waga_str, wzrost_str):
    wiek_str = wiek_str.strip()
    waga_str = waga_str.strip()
    wzrost_str = wzrost_str.strip()

    if not wiek_str or not waga_str or not wzrost_str:
        raise ValueError("Proszę wypełnić wszystkie pola liczbowe (Wiek, Waga, Wzrost)!")

    try:
        wiek = int(wiek_str)
        waga = float(waga_str.replace(',', '.'))
        wzrost = float(wzrost_str.replace(',', '.'))
    except ValueError:
        raise ValueError("Wiek, waga i wzrost muszą być poprawnymi liczbami!")

    if not (0 < wiek <= WIEK_MAX):
        raise ValueError(f"Wiek musi być w zakresie 1-{WIEK_MAX} lat.")
    if not (0 < waga <= WAGA_MAX):
        raise ValueError(f"Waga musi być w zakresie 1-{WAGA_MAX} kg.")
    if not (0 < wzrost <= WZROST_MAX):
        raise ValueError(f"Wzrost musi być w zakresie 1-{WZROST_MAX} cm.")

    return wiek, waga, wzrost
