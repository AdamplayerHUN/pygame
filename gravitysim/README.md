### Gravitáció szimulátor

* Ez egy gravitáció-szimulátor, amely különböző tömegű és átmérőjű égitestek egymásra ható erejét, illetve mozgását szimulálja
* A program lehetővé teszi a felhasználó beavatkozását a szimulációba, az irányítások a következők:
    * D: Pontokat rajzolnak az égitestek, a megtett pályájukat kirajzolva. Ez egy viszonylag erőforrásigényes, ezért a program egy idő után kitörli a pontokat
    * C: Pontok törlése, ha a szimuláció akadozna
    * R: Szimuláció visszaállítása alapkonfigurációba
    * P: Szimuláció szüneteltetése
    * T, G: Nagyítás/kicsinyítés
    * Kurzorok: kameramozgatás
    * Shift: kameramozgás gyorsítása
    * Új bolygó lehelyezésé:
        * E: Bolygó lehelyezése a kurzor helyére
        * A program tartalmaz egy húzás funkciót, amely a balklikk hosszan nyomvatartásával érhető el. Nyomd le a bal egérgombot, majd húzd el a kurzort valahova, majd a balklikk felengedésekor csúzliszerűen kilő egy bolygó a kurzor elhúzásának irányával ellentétes irányba. A húzás erőssége a képernyő jobb oldalán található lenyitható beállítások fülön érhető el.
        * A bolygóra vonatkozó beállítások a következők:
            * Mind a tömeget, az erősséget, és az átmérőt egy százalékos formában lehet megadni. A bolygóállás-alapkonfigurációban lévő "nap" beállításai a következők:
                * Tömeg: 50%
                * Átmérő: 40%
            * a "Föld" bolygó beállításai a következők:
                * Tömeg: 1%
                * Átmérő: 10%
            * a "Hold bolygó beállításai a következők:
                * Tömeg: 0,25%
                * Átmérő: 4%



## Changelog

* Version 1
    * Gravitáció
    * 3 alap bolygó hozzáadása
    * Lehetőség új bolygó létrehozására
    * Beállítások fül
    * Pontrajzolás

* Version 2:
    * Kameramozgatás
    * Új bolygó lehelyezése a kurzor helyére (E)
    * Fixek:
        * Bolygótömeg állíthatóság

* Version 2.1:
    * 3 Testes probléma üdvözlőként
    * Csillagok a háttérben
    * Fókuszálás a kurzorral, és gombokkal ( , ) ( . )
    * Tömeg finomállíthatóság
    * A bolygók a saját színükkel húznak pontokat
    * Új szín (szürke)
    * Fixek:
        * Bolygó kilövés*lehelyezés kódhiba kijavítása
        * Optimalizálás a pontokkal
        * Kirajzolás optimalizálás

* Version 3:
    * Teljes kijelzős mód
    * Reszponzív kezelőfelület
    * Gyorsabb kameramozgatás (shift)

* Version 4:
    * Zoom funkció (T, G)
    * Látható a beállítások fül bezáró területe
    * Az irányítás információk csak akkor láthatók, amikor az I gomb le van nyomva
    * Fixek:
        * Pause funkció nem glitchel
