# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 2023

@author: tarmoboy
"""
import matplotlib.pyplot as plt
import numpy as np

def havaitse(p, kartta, havainto, virhe):
    """
    Päivittää todennäköisyydet kartan jokaiselle ruudulle ottaen huomioon 
    uusimman värihavainnon.

    Parametrit
    ----------
    p : list[list[float]] 
        Alkuperäiset todennäköisyydet jokaiselle kartan ruudulle.
    kartta : list[list[str]]
        Matriisi, joka sisältää jokaisen ruudun värin.
    havainto : str
        Uusin värihavainto.
    virhe : float
        Todennäköisyys väärälle havainnolle.

    Palauttaa
    ----------
    q : list[list[float]]
        Päivitetyt todennäköisyydet kullekin ruudulle.
    """
    # Rivien määrä
    rivit = len(kartta)
    # Sarakkeiden määrä
    sarakkeet = len(kartta[0])
    # Uuden todennäköisyysmatriisin alustaminen nolla-alkioilla
    q = [[0.0 for sarake in range(sarakkeet)] for rivi in range(rivit)]
    # Summan alustus
    summa = 0.0
    for i in range(rivit):
        for j in range(sarakkeet):
            # Tarkistetaan, täsmääkö tämä havainto tämän ruudun väriin
            if havainto == kartta[i][j]:
                # Jos täsmää, päivitetään todennäköisyys vähentäen virhe
                q[i][j] = p[i][j] * (1-virhe)
            else:
                # Jos ei täsmää, on todennäköisyys vain virheen suuruinen
                q[i][j] = p[i][j] * virhe
            # Todennäköisyyksien laskeminen yhteen normalisointia varten
            summa += q[i][j]
    # Jos todennäköisyyksien summa jostain syystä 0, palataan
    if summa == 0:
        return q
    # Todennäköisyyksien normalisointi
    for i in range(rivit):
        for j in range(sarakkeet):
            # Jaetaan kukin todennäköisyys kaikkien summalla
            q[i][j] /= summa
    return q

def liiku(p, liike):
    """
    Siirtää todennäköisyysjakaumaa liikkeen mukaisesti kartalla.
    
    Parametrit
    ----------
    p : list[list[float]]
        Matriisi, joka sisältää todennäköisyydet ajoneuvon sijainnille 
        jokaisessa kartan ruudussa.
    liike : list[int, int]
        Liikevektori, joka ilmaisee ajoneuvon liikkeen muutoksen y- ja 
        x-suunnassa.

    Palauttaa
    ----------
    q : list[list[float]]
        Päivitetty todennäköisyysjakauma ajoneuvon uusille mahdollisille 
        sijainneille.
    """
    # Rivien määrä
    rivit = len(p)
    # Sarakkeiden määrä
    sarakkeet = len(p[0])
    # Uuden todennäköisyysmatriisin alustaminen nolla-alkioilla
    q = [[0.0 for sarake in range(sarakkeet)] for rivi in range(rivit)]
    for i in range(rivit):
        for j in range(sarakkeet):
            # Todennäköisyysjakauma siirtyy liikkeen mukaisesti
            # Modulo siirtää yli menevät todennäköisyydet kartan ympäri
            q[i][j] = p[(i-liike[0]) % rivit][(j-liike[1]) % sarakkeet]
    return q

def posteriorijakauma(kartta, havainnot, liikkeet, virhe):
    """
    Määrittää posteriorijakauman annettujen havaintojen ja liikkeiden 
    perusteella.

    Parametrit
    ----------
    kartta : list[list[str]]
        Matriisi, joka sisältää kunkin ruudun värin.
    havainnot : list[str]
        Lista värihavainnoista, jotka ajoneuvo on tehnyt liikkeiden aikana.
    liikkeet : list[list[int]]
        Lista liikkeistä, jotka ajoneuvo on suorittanut. Jokainen liike on 
        vektorimuodossa [dx, dy].
    virhe : float
        Todennäköisyys, että värihavainto on virheellinen.

    Palauttaa
    ----------
    p : list[list[float]]
        Posteriorijakauma, joka edustaa todennäköisyyksiä ajoneuvon 
        sijainnille kartalla havaintojen ja liikkeiden jälkeen.
    """
    # Rivien määrä
    rivit = len(kartta)
    # Sarakkeiden määrä
    sarakkeet = len(kartta[0])
    # Priorijakauma ennen liikkeitä ja havaintoja, jaetaan siis 
    # todennäköisyys rivien ja sarakkeiden lukumäärillä
    p = 1.0 / rivit / sarakkeet
    # Määritetään, että aluksi joka ruudulla on sama todennäköisyys
    p = [[p for sarake in range(sarakkeet)] 
         for rivi in range(rivit)]
    # Päivitetään todennäköisyyksiä havaintojen lukumäärän perusteella
    for i in range(len(havainnot)):
        # Posteriorijakauma kullekin ruudulle
        # Oletetaan, että ensin liikutaan
        p = liiku(p, liikkeet[i])
        # Sitten havaitaan
        p = havaitse(p, kartta, havainnot[i], virhe)
    return p

def piirra_kartta(kartta, p=None):
    """
    Piirtää annetun kartan ja todennäköisyydet kartan sijainneille
    
    Parametrit
    ----------
    kartta : list[list[str]]
        Matriisi, joka sisältää jokaisen ruudun väriä vastaavan kirjaimen.
    p : list[list[float]], valinnainen
        Matriisi, joka sisältää jokaisen ruudun todennäköisyyden. Jos 'p'
        jätetään antamatta, ei todennäköisyyksiä piirretä.
    """
    # Käytettävät värit
    värikartta = {'R': 'tab:red', 'G': 'tab:green', 
                  'B': 'tab:blue', 'E': 'lightgrey'}
    # Rivien määrä
    rivit = len(kartta)
    # Sarakkeiden määrä
    sarakkeet = len(kartta[0])
    # Kuvan koko
    korkeus = 12
    leveys = korkeus * (sarakkeet / rivit) - 0.31
    plt.subplots(figsize=(leveys, korkeus))
    for i in range(rivit):
        # Joka riville puoliväliin viiva ruudukolle
        plt.gca().axhline(i-0.5, color='k', linewidth=1)
        for j in range(sarakkeet):
            # Joka sarakkeelle puoliväliin viiva ruudukolle
            plt.gca().axvline(j-0.5, color='k', linewidth=1)
            # Ruudukon väritys karttaan merkityillä väreillä
            plt.fill_between([j-0.5, j+0.5], [rivit-i-1.5, rivit-i-0.5][0], 
                             [rivit-i-1.5, rivit-i-0.5][1], 
                             color=värikartta[kartta[i][j]])
            # Todennäköisyyksien esittäminen ruuduille kolmella desimaalilla
            if p is not None:
                plt.text(j, rivit-i-1, f'{p[i][j]:.3f}', ha="center", 
                         va="center", color="k", fontsize=22)
    # x ja y ääriarvot
    plt.xlim(-0.5, sarakkeet-0.5)
    plt.ylim(-0.5, rivit-0.5)
    # Akselien tiheys ja fonttikoko
    plt.xticks(range(sarakkeet), fontsize=28)
    plt.yticks(range(rivit), fontsize=28)
    # y-akselin numeroiden kääntäminen
    plt.gca().set_yticklabels([str(rivit-1-y) for y in range(rivit)])
    # Akselit ja otsikko, ja kuvaajan näyttäminen
    plt.xlabel('Sarakkeet', fontsize=28)
    plt.ylabel('Rivit', fontsize=28)
    plt.title('Kartta', fontsize=32)
    plt.show()
    
def visualisoi_jakauma(p):
    """
    Visualisoi todennäköisyysjakauman käyttäen värikarttaa.

    Parametri
    ----------
    p : list[list[float]]
        Matriisi, joka sisältää todennäköisyydet jokaiselle ruudulle.
    """
    # Rivien määrä
    rivit = len(p)
    # Sarakkeiden määrä
    sarakkeet = len(p[0])
    # Kuvan koko
    korkeus = 12
    leveys = korkeus * (sarakkeet / rivit) + 2
    plt.figure(figsize=(leveys, korkeus))
    # Värikartan piirtäminen
    plt.imshow(p, cmap='coolwarm', interpolation='nearest', 
               vmin=0, vmax=1)
    # Todennäköisyys tekstinä kuhunkin ruutuun kolmella desimaalilla
    for i in range(rivit):
        for j in range(sarakkeet):
            plt.text(j, i, f'{p[i][j]:.3f}', ha="center", va="center", 
                     color="k", fontsize=22)
    # Väripalkki
    cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=28)
    # Akselit, otsikko ja kuvaajan näyttäminen
    plt.xticks(range(sarakkeet), fontsize=28)
    plt.yticks(range(rivit), fontsize=28)
    plt.xlabel('Sarakkeet', fontsize=28)
    plt.ylabel('Rivit', fontsize=28)
    plt.title('Todennäköisyysjakauma', fontsize=32)
    plt.show()
    
def kaanna_liikkeet(liikkeet):
    """
    Kääntää annetun liikesarjan 90, 180 ja 270 asteella.
    
    Parametrit
    ----------
    liikkeet : list[list[int]]
        Lista liikkeistä, jotka ajoneuvo on suorittanut. Jokainen liike on 
        vektorimuodossa [dx, dy].

    Palauttaa
    -------
    liikkeet90 : list[list[int]]
        Alkuperäiset liikkeet käännettynä 90 asteella.
    liikkeet180 : list[list[int]]
        Alkuperäiset liikkeet käännettynä 180 asteella.
    liikkeet270 : list[list[int]]
        Alkuperäiset liikkeet käännettynä 270 asteella.
    """
    # Listojen alustus
    liikkeet90 = []
    liikkeet180 = []
    liikkeet270 = []
    for x, y in liikkeet:
        # 90 asteen kierto
        liikkeet90.append([-y,x])
        # 180 asteen kierto
        liikkeet180.append([-x,-y])
        # 270 asteen kierto
        liikkeet270.append([y,-x])
    return liikkeet90, liikkeet180, liikkeet270

def yhdista_jakaumat(jakaumat):
    """
    Yhdistää useita todennäköisyysjakaumia ja normalisoi lopputuloksen.

    Parametrit
    ----------
    jakaumat : list[list[list[float]]]
        Lista todennäköisyysjakaumista.

    Palauttaa
    ----------
    yhdistetty_jakauma : list[list[float]]
        Yhdistetty ja normalisoitu todennäköisyysjakauma.
    """
    # Rivien määrä
    rivit = len(jakaumat[0])
    # Sarakkeiden määrä
    sarakkeet = len(jakaumat[0][0])
    # Alustetaan yhdistetty jakauma ensimmäisellä jakaumalla
    yhdistetty_jakauma = jakaumat[0]
    # Yhdistetään loput jakaumat tähän
    for jakauma in jakaumat[1:]:
        for i in range(rivit):
            for j in range(sarakkeet):
                yhdistetty_jakauma[i][j] += jakauma[i][j]
    # Lasketaan summa normalisointia varten
    summa = sum(sum(rivi) for rivi in yhdistetty_jakauma)
    # Jos summa on 0, palautetaan yhdistetty jakauma sellaisenaan
    if summa == 0:
        return yhdistetty_jakauma
    # Normalisoidaan jakauma
    for i in range(rivit):
        for j in range(sarakkeet):
            yhdistetty_jakauma[i][j] /= summa
    return yhdistetty_jakauma

def satunnainen_kartta(rivit, sarakkeet):
    """
    Luo satunnaisesti generoidun kartan annettujen rivien ja sarakkeiden
    lukumäärien perusteella. Kartan sijainneille on värinä joko punainen 
    'R', vihreä 'G' tai sininen 'B', tai ei väriä ollenkaan 'E'.
    
    Parametrit
    ----------
    rivit : int
        Kartan rivien lukumäärä.
    sarakkeet : int
        Kartan sarakkeiden lukumäärä.

    Palauttaa
    -------
    2D numpy.ndarray
        Kaksiulotteinen taulukko, joka edustaa karttaa. Jokainen taulukon 
        alkio on merkkijono, joka edustaa tietyn ruudun väriä.
    """
    varit = ['R', 'G', 'B', 'E']
    return np.random.choice(varit, (rivit, sarakkeet))

# Muuttujien alustus
# Kartta: 'R' punainen, 'G' vihreä, 'B' sininen, 'E' tyhjä
kartta = [['R', 'G', 'E', 'R', 'G', 'G', 'G', 'R', 'G', 'G'],
          ['G', 'G', 'E', 'R', 'E', 'B', 'G', 'B', 'G', 'G'],
          ['R', 'E', 'R', 'G', 'E', 'E', 'E', 'G', 'B', 'G'],
          ['G', 'B', 'G', 'R', 'R', 'B', 'B', 'R', 'B', 'G'],
          ['G', 'E', 'B', 'E', 'B', 'G', 'G', 'E', 'R', 'B'],
          ['R', 'B', 'G', 'R', 'R', 'R', 'B', 'R', 'B', 'E'],
          ['E', 'B', 'B', 'G', 'E', 'R', 'R', 'E', 'E', 'B'],
          ['E', 'E', 'R', 'G', 'E', 'E', 'R', 'G', 'G', 'E'],
          ['E', 'R', 'G', 'E', 'B', 'B', 'R', 'R', 'R', 'B'],
          ['R', 'E', 'G', 'E', 'E', 'R', 'E', 'B', 'B', 'G']]
# Havainnot: mitä kartan värejä auto havaitsee
havainnot = ['G','E','E','B','B','G','B','G','G','G']
# Liikkeet: mihin auto liikkuu. Aluksi auto on paikallaan, kun ensimmäinen
# havainto saadaan. Ensimmäinen koordinaatti on y muutos, 
# toinen x muutos.
# [1,0] -> liike alaspäin
# [-1,0] -> liike ylös
# [0,1] -> liike oikealle
# [0,-1] -> liike vasemmalle
liikkeet = [[0,0],[1,0],[1,0],[0,1],[-1,0],[-1,0],[1,0],[-1,0],[0,1],[0,-1]]
# Todennäköisyys, että liikkeen jälkeen tehty havainto onkin väärä
virhe = 0.001

# Funktioiden kutsuminen
posteriori = posteriorijakauma(kartta, havainnot, liikkeet, virhe)
#piirra_kartta(kartta, posteriori)
piirra_kartta(kartta)
visualisoi_jakauma(posteriori)

# Kierretyt liikesarjat
#liikkeet90, liikkeet180, liikkeet270 = kaanna_liikkeet(liikkeet)
#posteriori90 = posteriorijakauma(kartta, havainnot, liikkeet90, virhe)
#posteriori180 = posteriorijakauma(kartta, havainnot, liikkeet180, virhe)
#posteriori270 = posteriorijakauma(kartta, havainnot, liikkeet270, virhe)
#piirra_kartta(kartta)
#visualisoi_jakauma(posteriori)
#visualisoi_jakauma(posteriori90)
#visualisoi_jakauma(posteriori180)
#visualisoi_jakauma(posteriori270)
#yhdistetty_jakauma = yhdista_jakaumat([posteriori, posteriori90, 
#                                       posteriori180, posteriori270])
#visualisoi_jakauma(yhdistetty_jakauma)

# 5x6-kartta ja esimerkkiliikkeet
#kartta = [['G', 'G', 'R', 'E', 'B', 'E'],
#          ['G', 'B', 'E', 'B', 'R', 'E'],
#          ['R', 'B', 'B', 'B', 'G', 'G'],
#          ['R', 'G', 'B', 'B', 'E', 'R'],
#          ['G', 'G', 'G', 'E', 'E', 'B']]
#havainnot = ['E','B','E','B']
#liikkeet = [[0,0],[0,-1],[0,1],[1,0]]
#posteriori = posteriorijakauma(kartta, havainnot, liikkeet, virhe)
#piirra_kartta(kartta)
#visualisoi_jakauma(posteriori)

# 3x4-kartta ja esimerkkiliikkeet
#kartta = [['G', 'G', 'R', 'E'],
#          ['B', 'E', 'G', 'B'],
#          ['E', 'B', 'R', 'E']]
#havainnot = ['E','B','E']
#liikkeet = [[0,0],[0,-1],[0,1]]
#posteriori = posteriorijakauma(kartta, havainnot, liikkeet, virhe)
#piirra_kartta(kartta)
#visualisoi_jakauma(posteriori)

# Satunnaisen kartan generoiminen, käyttämällä samaa seediä saat
# joka ajolla saman kartan
#seed = 6125 # käytetty 3x4- ja 5x6-karttoihin
#seed = 1434 # käytetty 10x10-karttaan
#np.random.seed(seed)
#kartta = satunnainen_kartta(10, 10)
#print(kartta)
#posteriori = posteriorijakauma(kartta, havainnot, liikkeet, virhe)
#piirra_kartta(kartta)
#visualisoi_jakauma(posteriori)
