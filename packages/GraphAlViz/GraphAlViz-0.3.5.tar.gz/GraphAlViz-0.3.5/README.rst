# GraphAlViz

Wizualizacja grafów.

## Struktura pliku grafu

    1. D=1          // informacja czy skierowany (1) czy nie skierowany (0) 
    2. V=13         // liczba wierzchołków
    3. E=34         // liczba krawędzi
    4. 1 2 5        // <nr wierzchołka> <nr wierzchołka> [<waga>] - lista krawędzi - dwójka lub trójki liczb, waga jest opcjonalna może jej nie być
       ...
    // po rozpoczęciu algorytmu rozmieszczania graf razem z rozmieszczeniem zostaje zapisany do tego samego pliku 
    5. #1 (x,y)     // lista współrzędnych rozmieszczeń wierzchołków - dopisana po poleceniu `load(nazwa_pliku)`
       ...

## Polecenia z biblioteki
`load(nazwa_pliku)` - zaczyna od czyszczenia grafu, otwiera, sprawdza strukturę 
pliku, rysuje i zapisuje graf (razem z rozmieszczeniem),
    `nazwa_pliku` plik z grafem (np. d1.g) w katalogu programu/bieżącym lub pełną ścieżka

`set_v_color(nr.wierzchołka, kolor)` - kolorowanie wierzchołka (kolory od 0 do 8, gdzie 0 - czarny, 1 - czerwony, 2 - zielony, 3 - niebieski, 4, - żółty, 5 - brązowy, 6 - fioletowy, 7 - inny)

`set_e_color(nr.wierzchołka_1, nr.wierzołka_2, kolor)` - kolorowanie krawędzi

`set_label_v(nr.wierzchołka, etykieta)` - etykieta obok numeru wierzchołka grafu, w nawiasach [], np. 7[15] - etykieta oznacza odwiedziny algorytmu dla danego wierzchołka

`set_label_e(nr.wierzchołka_1, nr.wierzołka_2, etykieta)` - etykieta nad krawędzią

## Wymagania

  - python z Tk (Tkinter)
  - networkx
  - matplotlib
