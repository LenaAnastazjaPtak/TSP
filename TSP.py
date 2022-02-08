import random
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime


class ACO(object):
    def __init__(self, liczba_miast, wspolrzedne, nazwaPliku):
        self.nazwaPliku = nazwaPliku
        self.m = 30  # Liczba mrówek
        self.alpha = 1  # Współczynnik ważności feromonów
        self.beta = 5  # Ważny czynnik funkcji heurystycznej
        self.rho = 0.1  # Lotny czynnik feromonów
        self.Q = 1  # Stały współczynnik
        self.liczba_miast = liczba_miast  # Liczba miast
        self.wspolrzedne = wspolrzedne  # Współrzędne miast
        self.feromony = np.ones([liczba_miast,
                                 liczba_miast])  # Macierz feromonów wypełniona jedynkami o wymiarze liczba miast x liczba miast.
        self.kolonia_mrowek = [[0 for _ in range(liczba_miast)] for _ in
                               range(self.m)]  # Kolonia mrówek, czyli każda mrówka i jej skończona droga.
        self.iter = 1
        self.liczba_iteracji = 1000  # Liczba iteracji
        self.macierz_sasiedztwa = self.oblicz_macierz_sasiedztwa(liczba_miast,
                                                                 self.wspolrzedne)  # Oblicz macierz sąsiedztwa (odległości między miastami)
        self.Eta = 10. / self.macierz_sasiedztwa  # Funkcja heurystyczna (do wzoru na prawdopodobieństwo)
        self.sciezki = None  # Tablica dystansów zrobionych przez mrówki.
        self.iter_x = []
        self.iter_y = []

    def plotTSP(self, points, n, najlepszy_dystans):
        paths = [[x for x in range(self.liczba_miast - 1)]]
        paths[0].append(0)

        x = []
        y = []
        for i in paths[0]:
            x.append(points[i][0])
            y.append(points[i][1])

        if n == 3:
            f3 = plt.figure(3)
            title = f"Najlepsza droga {self.nazwaPliku}\n\nDługość drogi wynosi: {round(najlepszy_dystans, 2)}"
            plt.plot(x, y, 'b.')
            plt.plot(x[0], y[0], 'ro')
            plt.plot(x[len(x) - 1], y[len(x) - 1], 'ro')
        elif n == 2:
            f2 = plt.figure(2)
            title = f"Poczatkowa droga {self.nazwaPliku}\n\nDługość drogi wynosi: {round(najlepszy_dystans, 2)}"
            plt.plot(x, y, 'b.')
        else:
            f5 = plt.figure(5)
            title = f"1/10 iteracji {self.nazwaPliku}\n\nDługość drogi wynosi: {round(najlepszy_dystans, 2)}"
            plt.plot(x, y, 'b.')

        # plt.subplot(2, 2, n)
        plt.title(title)
        plt.grid(True)
        plt.xlabel('x', fontweight='bold')
        plt.ylabel('y', fontweight='bold')

        # Skala grota strzałki - konieczne zeby ladnie dzialalo
        a_scale = float(max(x)) / float(100)

        # Rysuj droge
        plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale, color='black',
                  length_includes_head=True)
        for i in range(0, len(x) - 1):
            plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale, color='black',
                      length_includes_head=True)

        # Ustaw osie X i Y na troche wieksze niz max X i Y
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)

    def czasDoKonca(self, iteracja, czas):
        sekundyDoKonca = czas * (iteracja - self.liczba_iteracji)
        return str(datetime.timedelta(seconds=sekundyDoKonca))

    # Wybór ruletki
    def losuj(self, p):
        x = np.random.rand()
        for i, t in enumerate(p):
            # Enumerate umożliwia  iterację po obiektach takich jak lista (u nas p)
            # przy jednoczesnej informacji, którą iterację wykonujemy.
            x -= t
            if x <= 0:
                break
        return i  # Zwraca indeks następnego miasta do odwiedzenia.

    # Stwórz kolonię mrówek
    def wez_mrowki(self, liczba_miast):
        for i in range(self.m):  # m - liczba mrówek.
            start = np.random.randint(liczba_miast - 1)  # Losuje liczbę w zakresie liczbie miast.
            self.kolonia_mrowek[i][0] = start  # Wierzchołek startowy.
            nieodwiedzone = list([x for x in range(liczba_miast) if x != start])  # Raczej lista miast do odwiedzenia.
            obecny = start
            j = 1
            while len(nieodwiedzone) != 0:
                P = []
                # Oblicz prawdopodobieństwo przejścia między miastami przez feromony
                for v in nieodwiedzone:
                    P.append(self.feromony[obecny][v] ** self.alpha * self.Eta[obecny][
                        v] ** self.beta)  # nasz wzór na prawdopodobieństwo
                P_suma = sum(P)
                # Bierzemy prawdopodobienstwo jednego wierzchołka  i dzielimy przez sumę prawdopodobieństw wszystkich wierzchołków
                P = [x / P_suma for x in P]
                # Ruletka wybiera miasto
                indeks = self.losuj(P)
                obecny = nieodwiedzone[indeks]
                self.kolonia_mrowek[i][j] = obecny
                # W macierzy "kolonia mrówek" wspolrzedna i to numer mrówki, a j to nr wierzcholka, do ktorego przeszła mrówka.
                # Tworzymy więc dla każdej mrówkę jej ścieżkę.
                nieodwiedzone.remove(obecny)
                j += 1

    # Oblicz odległość między różnymi miastami
    def oblicz_macierz_sasiedztwa(self, liczba_miast, wspolrzedne):  # liczba miast, tablica ze współrzędnymi.
        macierz_sasiedztwa = np.zeros(
            (liczba_miast, liczba_miast))  # Tworzy macierz liczba miast x liczba miast wypełnioną zerami.
        for i in range(liczba_miast):
            for j in range(liczba_miast):
                if i == j:
                    macierz_sasiedztwa[i][j] = np.inf
                    # zmiennoprzecinkowa reprezentacja (dodatniej) nieskończoności.
                    continue
                a = wspolrzedne[i]
                b = wspolrzedne[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                macierz_sasiedztwa[i][j] = tmp
        # print("\nMACIERZ SĄSIEDZTWA: \n", macierz_sasiedztwa)
        return macierz_sasiedztwa  # Zwraca macierz sąsiedztwa.

    # Oblicz długość ścieżki
    def oblicz_dlugosc_sciezki(self, droga, macierz_sasiedztwa):
        a = droga[0]
        b = droga[-1]
        wyn = macierz_sasiedztwa[a][b]  # Droga mrówki przy domykaniu ścieżki.
        for i in range(len(droga) - 1):
            a = droga[i]
            b = droga[i + 1]
            wyn += macierz_sasiedztwa[a][b]
        return wyn  # Zwraca dystans pokonany przez mrówkę.

    # Oblicz długość grupy
    def oblicz_sciezki(self, sciezki):  # sciezki to teraz kolonia mrówek.
        wyn = []
        for one in sciezki:  # dla każdej ścieżki mrówki:
            dlugosc = self.oblicz_dlugosc_sciezki(one, self.macierz_sasiedztwa)
            wyn.append(dlugosc)
        return wyn  # Tablica dystansów zrobionych przez mrówki.

    # Zaktualizuj feromon
    def aktualizuj_feromony(self):
        delta_feromony = np.zeros([self.liczba_miast, self.liczba_miast])  # Macierz feromonów
        sciezki = self.oblicz_sciezki(self.kolonia_mrowek)  # Tablica dystansów zrobionych przez mrówki.
        for i in range(self.m):  # m - liczba mrówek
            for j in range(self.liczba_miast - 1):
                a = self.kolonia_mrowek[i][j]
                b = self.kolonia_mrowek[i][j + 1]
                delta_feromony[a][b] = delta_feromony[a][b] + self.Q / sciezki[i]  # Zostawianie feromonów.
            a = self.kolonia_mrowek[i][0]
            b = self.kolonia_mrowek[i][-1]
            delta_feromony[a][b] = delta_feromony[a][b] + self.Q / sciezki[
                i]  # Domknięcie ścieżki z zostawianiem feromonu.
        self.feromony = (
                                    1 - self.rho) * self.feromony + delta_feromony  # Na początku paruje i dodaje te nowe zostawione feromony.
        # Wszystkie ścieżki parują tzn wszystkie wartości w tablicy feromonów mnożymy razy (1 - self.rho), czyli 0,9. I dodajemy wartość feromonow.

    def aco(self):
        najlepszy_dystans = math.inf  # Wartość najlepszej ścieżki ustawiamy na plus nieskończoność.
        najlepsza_sciezka = None  # Najlepsza ścieżka.
        for iteracja in range(self.liczba_iteracji):
            start = time.time()
            # Wygeneruj nową kolonię
            self.wez_mrowki(self.liczba_miast)  # out>>self.kolonia_mrowek, puszczamy mrówki i zapisujemy ich ścieżki.
            self.sciezki = self.oblicz_sciezki(self.kolonia_mrowek)  # Tablica dystansów.
            # Weź optymalny roztwór kolonii mrówek
            tmp_dlugosc = min(self.sciezki)  # Najmniejszy dystans.
            tmp_sciezka = self.kolonia_mrowek[self.sciezki.index(tmp_dlugosc)]  # I ścieżka miast od niego.

            # Zaktualizuj optymalne rozwiązanie
            if tmp_dlugosc < najlepszy_dystans:
                najlepszy_dystans = tmp_dlugosc
                najlepsza_sciezka = tmp_sciezka

            # Wizualizuj początkową ścieżkę  (wykresy)
            if iteracja == 0:
                init_show = self.wspolrzedne[tmp_sciezka]
                init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec sciezki
                x, y = init_show[:, 0], init_show[:, 1]
                self.plotTSP([(x[i], y[i]) for i in range(len(x))], 2, najlepszy_dystans)

            if iteracja == int(self.liczba_iteracji / 10):
                init_show = self.wspolrzedne[tmp_sciezka]
                init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec sciezki
                x, y = init_show[:, 0], init_show[:, 1]
                self.plotTSP([(x[i], y[i]) for i in range(len(x))], int(self.liczba_iteracji / 2), najlepszy_dystans)

            # Zaktualizuj feromon
            self.aktualizuj_feromony()

            # Zapisz wynik
            self.iter_x.append(iteracja)
            self.iter_y.append(najlepszy_dystans)

            end = time.time()
            print("Iteracja: ", iteracja, "     ", int(iteracja / self.liczba_iteracji * 100), "%   ",
                  "Czas do końca: ", self.czasDoKonca(iteracja, start - end))

        init_show = self.wspolrzedne[najlepsza_sciezka]
        init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec sciezki
        x, y = init_show[:, 0], init_show[:, 1]
        self.plotTSP([(x[i], y[i]) for i in range(len(x))], 3, najlepszy_dystans)

        print(f"Najlepszy wynik {self.nazwaPliku} to: {najlepszy_dystans}")

        print("Kolejność wierzchołków:")
        print(*najlepsza_sciezka, najlepsza_sciezka[0])

        print("\nWspółrzędne x i y:")
        print(*x)
        print(*y)

        return najlepszy_dystans, najlepsza_sciezka

    # Główna funkcja.
    def run(self):
        NAJ_dystans, NAJ_sciezka = self.aco()
        f4 = plt.figure(4)
        plt.title(f'Długość drogi w zależnosci od iteracji {self.nazwaPliku}')
        plt.plot(self.iter_x, self.iter_y, 'black', linewidth=3.0)
        plt.grid(True)
        plt.xlim(-50, max(self.iter_x) * 1.05)
        plt.ylim(min(self.iter_y) * 0.99, max(self.iter_y) * 1.01)
        plt.xlabel('Liczba Iteracji', fontweight='bold')
        plt.ylabel('Długość Drogi', fontweight='bold')
        return self.wspolrzedne[NAJ_sciezka], NAJ_dystans, NAJ_sciezka


# Czytaj dane
def wczytaj_dane(nazwaPliku):
    plik = open(nazwaPliku, "r")
    liczbaPunktow = int(plik.readline())
    macierz = []  # [[1,421,423], [2, 12, 982], ...]
    for i in plik:
        macierz.append(list(map(int, i.split())))

    return macierz, liczbaPunktow


# Otwarcie pliku
nazwaPliku = 'berlin52.txt'
wspolrzedne, liczbaPunktow = wczytaj_dane(nazwaPliku)
wspolrzedne = np.array(wspolrzedne)  # Z biblioteki numpy. Z tablicy [1, 2, 3] robi [1 2 3].
wspolrzedne = wspolrzedne[:, 1:]  # [[51 30 40] ...] --> [[30 40] ...]
pokaz_wspolrzedne = np.vstack(
    [wspolrzedne, wspolrzedne[0]])  # dodaje wierzcholek startowy na koniec --> .append([37, 89])

# wywołanie klasy ACO:
aco = ACO(liczba_miast=liczbaPunktow, wspolrzedne=wspolrzedne.copy(), nazwaPliku=nazwaPliku)
ostateczna_sciezka, ostateczny_wynik, naj_droga = aco.run()

# Wykres
f1 = plt.figure(1)
plt.title(f'Współrzędne miast {nazwaPliku}')
x, y = wspolrzedne[:, 0], wspolrzedne[:, 1]
plt.plot(x, y, '.', color='black')
plt.grid(True)
plt.xlim(0, max(x) * 1.1)
plt.ylim(0, max(y) * 1.1)
plt.xlabel('x', fontweight='bold')
plt.ylabel('y', fontweight='bold')

plt.show()