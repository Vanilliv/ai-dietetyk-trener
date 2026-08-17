#łączenie z modelem Gemini AI
import logging
from google import genai
from google.genai import errors as genai_errors
import config

logger = logging.getLogger(__name__)

if not config.GEMINI_API_KEY:
    raise ValueError("BŁĄD: Nie znaleziono klucza API. Upewnij się, że plik .env istnieje i zawiera GEMINI_API_KEY.")

client = genai.Client(api_key=config.GEMINI_API_KEY)

def zbuduj_prompt(typ, wiek, waga, wzrost, cel, uwagi, liczba_dni, priorytet_partia="Brak priorytetu", poziom_zaawansowania="Średnio zaawansowany", wykluczenia=""):
    """Składa treść zapytania do Gemini na podstawie danych klienta. Czysta funkcja - bez wywołań sieciowych, więc łatwo ją przetestować."""
    tekst_uwag = uwagi if uwagi.strip() else "Brak specjalnych uwag i przeciwwskazań."
    tekst_wykluczen = wykluczenia if wykluczenia.strip() else "Brak specyficznych wykluczeń lub nielubianych składników."

    return f"""
    Działaj jako utytułowany, doświadczony kulturysta oraz profesjonalny trener personalny i dietetyk kliniczny.
    Twój styl układania planów opiera się na złotej erze kulturystyki oraz nowoczesnej nauce o hipertrofii: stawiasz na maksymalną intensywność, perfekcyjną technikę (czucie mięśniowe) i odpowiednią regenerację, zamiast na "wklepywanie" dziesiątek pustych serii.

    Twój klient to osoba, która ma {wiek} lat, waży {waga} kg i ma {wzrost} cm wzrostu.
    Główny cel klienta to: {cel}.
    Poziom zaawansowania klienta (BARDZO WAŻNE): {poziom_zaawansowania}.
    Priorytetowa partia mięśniowa (dotyczy tylko Planu Treningowego): {priorytet_partia}.
    
    UWAGI SPECJALNE / PRZECIWWSKAZANIA (BARDZO WAŻNE): 
    {tekst_uwag}

    WYKLUCZENIA DIETETYCZNE / NIELUBIANE SKŁADNIKI (BARDZO WAŻNE DLA DIETY):
    {tekst_wykluczen}
    
    Zadanie: Wygeneruj szczegółowy {typ} (na {liczba_dni} dni w tygodniu) dostosowany pod poziom zaawansowania: {poziom_zaawansowania}.
    
    Rygorystyczne zasady dla Planu Treningowego pod kątem poziomu zaawansowania ({poziom_zaawansowania}):
    1. BEZWZGLĘDNIE dostosuj intensywność, objętość (liczbę serii) i dobór ćwiczeń do wybranego poziomu:
       - Dla "Początkujący": mniejsza objętość (np. 2-3 serie robocze, niższe RPE np. 6-8), prostsze i bezpieczniejsze ćwiczenia, nacisk na opanowanie poprawnego ruchu. Kategorycznie unikaj zaawansowanych metod intensyfikacji (drop-sety, superserie, powtórzenia oszukiwane).
       - Dla "Średnio zaawansowany": umiarkowana/standardowa objętość (np. 3-4 serie na ćwiczenie), RPE 7-9, solidne ćwiczenia wielostawowe i izolowane, okazjonalne wprowadzenie prostych superserii.
       - Dla "Zaawansowany": wysoka intensywność (RPE 8-10, w tym serie do upadku mięśniowego / RIR 0), zaawansowane techniki intensyfikacji (drop-sety, rest-pause, serie łączone), bardziej wymagające ćwiczenia i wyższa objętość.
    2. OBJĘTOŚĆ: Każdy dzień treningowy może zawierać maksymalnie od 5 do 7 ćwiczeń (optymalnie 6). Nie przekraczaj tej liczby pod żadnym pozorem! Kulturysta buduje mięśnie jakością serii, a nie ich ilością.
    3. INTENSYWNOŚĆ: Dla każdego ćwiczenia określ liczbę serii, powtórzeń oraz poziom RPE (skala intensywności 1-10) lub zapas powtórzeń (RIR) dostosowany do poziomu.
    4. PRIORYTET: Jeśli wybrano priorytetową partię mięśniową ({priorytet_partia}), zwiększ dla niej częstotliwość i łączną objętość w CAŁYM tygodniu - nie ogranicza się to do jednego dnia:
       - Przy 4 i więcej dniach treningowych zaplanuj trening tej partii CO NAJMNIEJ 2 RAZY w tygodniu (wyższa częstotliwość daje lepsze efekty hipertroficzne niż jedna bardzo obszerna sesja).
       - Przy 2-3 dniach treningowych i tak dodaj dla tej partii 1-2 ćwiczenia uzupełniające w innym dniu, w którym logicznie pasuje (np. przy priorytecie na klatkę - w dniu barków/tricepsa), zamiast całkowicie ją pomijać w pozostałych dniach.
       - W dniu głównie poświęconym priorytetowej partii jej ćwiczenia umieść na samym początku treningu, kiedy klient ma najwięcej siły.
       - Priorytetowa partia powinna mieć łącznie więcej serii w tygodniu niż pozostałe partie mięśniowe.
    
    Rygorystyczne zasady dla Planu Dietetycznego pod kątem poziomu zaawansowania ({poziom_zaawansowania}):
    1. BEZWZGLĘDNIE dostosuj złożoność dań, restrykcyjność oraz suplementację do wybranego poziomu:
       - Dla "Początkujący": Proste posiłki z powszechnie dostępnych składników, szybkie w przygotowaniu. Skup się na budowaniu zdrowych nawyków żywieniowych i regularności. Unikaj skomplikowanych gramatur i zaawansowanej suplementacji (tylko absolutne podstawy, np. witamina D3, kwasy omega-3).
       - Dla "Średnio zaawansowany": Dokładniejsze wyliczenie makroskładników (białka, węglowodany, tłuszcze), uwzględnienie czasu spożycia posiłków przed- i potreningowych oraz podstawowej suplementacji sportowej (np. kreatyna, odżywka białkowa, witaminy).
       - Dla "Zaawansowany": Precyzyjnie zoptymalizowana dieta. Zaawansowane protokoły okołotreningowe (np. węglowodany intra-workout w trakcie treningu, lekkostrawne posiłki przedtreningowe typu kleik ryżowy z izolatem), rotacja węglowodanami (carb cycling) jeśli cel tego wymaga, oraz zaawansowana suplementacja kulturystyczna.
    
    Zasady formatowania i bezpieczeństwa:
    - BEZWZGLĘDNIE dostosuj plan do uwag specjalnych oraz wykluczeń żywieniowych! 
    - Jeśli klient ma kontuzję, wyklucz ćwiczenia ją obciążające i zaproponuj bezpieczne zamienniki.
    - Jeśli klient ma alergię lub podał nielubiane składniki ({wykluczenia}), pod żadnym pozorem nie używaj tych składników w jadłospisie. Zastąp je innymi wartościowymi i smacznymi produktami.
    - FORMATOWANIE: Ćwiczenia w planie treningowym muszą być ZAWSZE PONUMEROWANE (1., 2., 3. itd.). Absolutnie nie używaj zwykłych kropek ani gwiazdek (*) do wylistowania ćwiczeń.
    - FORMATOWANIE: Między ćwiczeniami wstaw enter dla lepszej czytelności.
    - FORMATOWANIE: Posiłki w dietach również numerycznie (Posiłek 1, Posiłek 2).
    - FORMATOWANIE: NIE używaj składni Markdown (żadnych **, __, #, ~~, tabel) - tekst trafia do zwykłego pola tekstowego, które takiego formatowania nie renderuje, więc pisz czystym tekstem.
    - FORMATOWANIE: Każdy dzień treningowy zaczynaj w osobnej linii od nagłówka w formacie "DZIEŃ <numer>: <partia/rodzaj treningu>" (np. "DZIEŃ 1: Klatka piersiowa i triceps").
    - FORMATOWANIE: Każdy posiłek zaczynaj w osobnej linii od nagłówka w formacie "POSIŁEK <numer>: <nazwa posiłku>".
    - Nie pisz długich wstępów, przejdź od razu do konkretów w kulturystycznym, profesjonalnym stylu.
    """


def generuj_plan(typ, wiek, waga, wzrost, cel, uwagi, liczba_dni, priorytet_partia="Brak priorytetu", poziom_zaawansowania="Średnio zaawansowany", wykluczenia=""):
    """Wysyła zbudowany prompt do Gemini i zwraca wygenerowany plan (albo komunikat o błędzie)."""
    prompt = zbuduj_prompt(typ, wiek, waga, wzrost, cel, uwagi, liczba_dni, priorytet_partia, poziom_zaawansowania, wykluczenia)

    logger.info("Generuję %s (%s dni) dla celu: %s", typ, liczba_dni, cel)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except genai_errors.APIError as e:
        logger.error("Błąd API Gemini: %s", e)
        return "Niestety, serwery Gemini AI zwróciły błąd (np. limit zapytań lub problem z kluczem API). Spróbuj ponownie za chwilę."
    except Exception as e:
        logger.error("Nieoczekiwany błąd podczas generowania planu: %s", e)
        return "Niestety, wystąpił nieoczekiwany problem z połączeniem z AI (sprawdź połączenie internetowe)."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("Testowanie zaktualizowanego silnika AI...\n")
    testowy_typ = "Plan Treningowy"
    testowy_wiek = 24
    testowa_waga = 85
    testowy_wzrost = 180
    testowy_cel = "Redukcja tkanki tłuszczowej"
    
    wynik = generuj_plan(testowy_typ, testowy_wiek, testowa_waga, testowy_wzrost, testowy_cel, "", "3")
    print("\nWynik AI:\n", wynik)