import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.animation as anim

"""
Obliczenia naukowe
Projekt 1.: Automaty komorkowe
Maciej Dzikowski
"""

# korzystam z modulu argparse
parser = argparse.ArgumentParser(description='Automaty komorkowe')
parser.add_argument('M', help='macierz poczatkowa')
parser.add_argument('S', help='macierz wag')
parser.add_argument('E', help='wektor reguł ewolucji')
parser.add_argument('k', type=int, help='liczba krokow symulacji do wykonania')
args = parser.parse_args()

def ak(Mp, Sp, Ep, k):
    """
    Funkcja odpowiadajaca za dzialanie calego automatu komorkowego.
    Mp - plik z macierza poczatkowa
    Sp - plik z macierza wag
    Ep - plik z wektorem regul ewolucji
    k - liczba krokow symulacji
    """

    # wczytuje macierze z plikow
    M = np.load(Mp)
    S = np.load(Sp)
    E = np.load(Ep)

    """
    Aby uniknac bledow, gdy macierz poczatkowa ma jeden wiersz, sprawdzam
    jej rozmiar, a nastepnie postepuje zgodnie z otrzymanym wynikiem,
    aby stworzyc ramke z '0'.
    """
    t = list(M.shape)  # zmienna pomocnicza

    if len(t) == 1:
        m = 1  # ilosc wierszy
        n = M.shape[0]  # ilosc kolumn
        l = []  # lista pomocnicza
        # dodaje gorny bok ramki
        l.append([0 for i in range(n)])
        l.append(list(M))
        M = np.array(l, dtype='int8')  # odtwarzam macierz

    else:
        m = M.shape[0]  # ilosc kolumn
        n = M.shape[1]  # ilosc wierszy
        M = np.insert(M, 0, [0], axis=0)  # dodaje gorny bok ramki

    M = np.insert(M, 0, [0], axis=1)  # dodaje lewy bok ramki
    M = np.insert(M, n + 1, [0], axis=1)  # dodaje prawy bok ramki
    M = np.insert(M, m + 1, [0], axis=0)  # dodaje dolny bok ramki

    """
    Tworze macierz pomocnicza 'N', aby nie nadpisywac przy kazdym kroku
    macierzy M, i przechodze do petli przeprowadzajacej symulacje.
    """
    N = np.zeros((m + 2, n + 2), dtype='int8')

    while k != 0:
        for i in range(m + 2):
            for j in range(n + 1):
                if i >= 1 and i <= m and j >= 1 and j <= n:
                    N[i, j] = E[np.sum(M[i - 1:i + 2, j - 1:j + 2] * S)]
        M = np.copy(N)  # zastepuje stara macierz M macierza po calym kroku
        k -= 1

    np.save('matrix.npy', M)  # zapisuje macierz do pliku
    plt.imsave('matrix.png', M)  # zapisuje macierz do obrazu

if __name__ == '__main__':
    ak(args.M, args.S, args.E, args.k)