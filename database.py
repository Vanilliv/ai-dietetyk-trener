# Obsługa bazy danych MySQL
import logging
import mysql.connector
import mysql.connector.plugins.caching_sha2_password
import mysql.connector.plugins.mysql_native_password
import config

logger = logging.getLogger(__name__)

# Wspólna nazwa błędów bazy, używana w main.py
DatabaseError = mysql.connector.Error

def polacz():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT,
        use_pure=True
    )

def stworz_tabele():
    conn = polacz()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Uzytkownicy (
            id INT AUTO_INCREMENT PRIMARY KEY,
            imie VARCHAR(100) NOT NULL,
            wiek INT,
            waga DOUBLE,
            wzrost DOUBLE,
            cel VARCHAR(255)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Plany (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_uzytkownika INT NULL,
            typ_planu VARCHAR(50),
            tresc_planu TEXT,
            data_stworzenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_uzytkownika) REFERENCES Uzytkownicy(id) ON DELETE SET NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Tabele bazy danych MySQL są gotowe.")

# Aplikacja nie ma logowania, więc klient rozpoznawany jest po imieniu.
# TODO: dwie osoby o tym samym imieniu dzielą jeden rekord, do zmiany przy kontach użytkowników
def znajdz_lub_stworz_uzytkownika(imie, wiek, waga, wzrost, cel):
    conn = polacz()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Uzytkownicy WHERE imie = %s ORDER BY id DESC LIMIT 1", (imie,))
    wynik = cursor.fetchone()

    if wynik:
        id_uzytkownika = wynik[0]
    else:
        cursor.execute(
            "INSERT INTO Uzytkownicy (imie, wiek, waga, wzrost, cel) VALUES (%s, %s, %s, %s, %s)",
            (imie, wiek, waga, wzrost, cel)
        )
        conn.commit()
        id_uzytkownika = cursor.lastrowid
        logger.info("Utworzono nowego użytkownika: %s (id=%s)", imie, id_uzytkownika)

    cursor.close()
    conn.close()
    return id_uzytkownika

def zapisz_plan(typ_planu, tresc_planu, id_uzytkownika=None):
    conn = polacz()
    cursor = conn.cursor()

    query = "INSERT INTO Plany (typ_planu, tresc_planu, id_uzytkownika) VALUES (%s, %s, %s)"
    cursor.execute(query, (typ_planu, tresc_planu, id_uzytkownika))

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Zapisano nowy %s w bazie MySQL.", typ_planu)

def pobierz_plany():
    conn = polacz()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Plany.id, Plany.typ_planu, Plany.tresc_planu, Plany.data_stworzenia, Uzytkownicy.imie
        FROM Plany
        LEFT JOIN Uzytkownicy ON Plany.id_uzytkownika = Uzytkownicy.id
        ORDER BY Plany.id DESC
    """)
    wyniki = cursor.fetchall()
    cursor.close()
    conn.close()

    return wyniki