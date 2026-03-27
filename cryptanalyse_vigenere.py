# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : ZEQO Ermal 21315866
# Etudiant.e 2 : FERROUKH Mohamed Nassim 21308499

import sys, getopt, string, math
import unicodedata
# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def calc_freq(nom_fichier: str) -> list[float]:
    """Calcule les fréquences des 26 lettres (A..Z) dans un fichier texte."""
    with open(nom_fichier, "r", encoding="latin-1") as f:
        raw = f.read().upper()
    txt = unicodedata.normalize("NFD", raw)
    counts = [0] * 26
    n = 0
    for c in txt:
        if 'A' <= c <= 'Z':
            counts[ord(c) - ord('A')] += 1
            n += 1

    if n == 0:
        return [0.0] * 26

    return [x / n for x in counts]

# Exo 1 : variable globale
freq_FR = calc_freq("germinal.txt")


def chiffre_cesar(message:str, n:int)->str:
    ''' 
    Retourne le message chiffre
    avec un decalage de n lettres
    '''
    message_chiffre:str=''
    position_A:int=ord('A') #65 en ASCII
    lettre_decalee:str

    #Chiffrement lettre par lettre du message
    lettre:str
    for lettre in message:
        lettre_decalee = chr( ((ord(lettre) - position_A + n)%26) + position_A )
        message_chiffre+= lettre_decalee
    
    return message_chiffre


def dechiffre_cesar(message:str, n:int)->str:
    ''' 
    Retourne le message dechiffre 
    avec un decalage de n lettres
    '''
    message_dechiffre:str=''
    position_A:int=ord('A') #65 en ASCII
    lettre_decalee:str

    #Dechiffrement lettre par lettre du message
    lettre:str
    for lettre in message:
        lettre_decalee = chr( ((ord(lettre)- position_A - n)%26) + position_A )
        message_dechiffre+= lettre_decalee
    
    return message_dechiffre


# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Chiffre un texte (A..Z) avec le chiffrement de Vigenère.

    Paramètres
    ----------
    txt : str
        Texte en majuscules, composé uniquement de lettres A..Z.
    key : list[int]
        Clé de Vigenère : liste d'entiers entre 0 et 25.
        La clé est répétée si txt est plus long.

    Retour
    ------
    str : le texte chiffré.
    """
    position_A = ord('A')
    res = ""

    for i, lettre in enumerate(txt):
        k = key[i % len(key)]
        x = ord(lettre) - position_A          # A->0, B->1, ..., Z->25
        y = (x + k) % 26                      # décalage modulo 26
        res += chr(y + position_A)            # retour vers une lettre

    return res

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Déchiffre un texte (A..Z) avec le chiffrement de Vigenère.

    Paramètres
    ----------
    txt : str
        Texte chiffré en majuscules (A..Z).
    key : list[int]
        Clé de Vigenère : liste d'entiers entre 0 et 25.

    Retour
    ------
    str : le texte déchiffré.
    """
    position_A = ord('A')
    res = ""

    for i, lettre in enumerate(txt):
        k = key[i % len(key)]
        y = ord(lettre) - position_A      # lettre chiffrée -> 0..25
        x = (y - k) % 26                 # on SOUSTRAIT la clé
        res += chr(x + position_A)       # retour vers lettre

    return res

# Analyse de fréquences
def freq(txt):
    """
    Calcule le nombre d'occurrences de chaque lettre (A..Z)
    dans un texte donné.

    Retourne une liste de 26 entiers.
    """
    hist = [0] * len(alphabet)   # 26 cases, toutes à 0

    for lettre in txt:
        if 'A' <= lettre <= 'Z':                 # on garde seulement les majuscules
            indice = ord(lettre) - ord('A')      # A->0, B->1, ..., Z->25
            hist[indice] += 1                    # on ajoute 1 occurrence

    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Renvoie l'indice (0..25) de la lettre la plus fréquente dans txt.
    En cas d'égalité, on renvoie la lettre la plus petite alphabétiquement.
    """
    hist = freq(txt)  # liste de 26 entiers

    indice_max = 0
    for i in range(1, len(hist)):
        if hist[i] > hist[indice_max]:
            indice_max = i

    return indice_max

# indice de coïncidence
def indice_coincidence(hist):
    """
    Calcule l'indice de coïncidence d'un texte
    à partir de son histogramme de fréquences.

    hist : liste de 26 entiers (occurrences des lettres)

    Retour : float
    """
    n = sum(hist)  # nombre total de lettres

    if n <= 1:
        return 0.0

    num = 0
    for ni in hist:
        num += ni * (ni - 1)

    den = n * (n - 1)

    return num / den

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Estime la longueur de la clé de Vigenère (<= 20) par l'indice de coïncidence.
    On teste k=1..20, on découpe en k colonnes, on calcule l'IC de chaque colonne,
    puis on prend la moyenne. On renvoie le premier k tel que moyenne > 0.06.
    """
    # Petit garde-fou : si texte trop court, on ne peut rien conclure
    if len(cipher) < 2:
        return 0

    meilleur_k = 0
    meilleur_score = -1.0

    for k in range(1, 21):  # clé supposée de longueur au plus 20
        colonnes = [""] * k

        # Découpage en colonnes : la lettre i va dans la colonne (i mod k)
        for i, c in enumerate(cipher):
            colonnes[i % k] += c

        # IC moyen des colonnes
        total_ic = 0.0
        for col in colonnes:
            total_ic += indice_coincidence(freq(col))
        ic_moyen = total_ic / k

        # On garde le meilleur au cas où aucun k ne dépasse 0.06
        if ic_moyen > meilleur_score:
            meilleur_score = ic_moyen
            meilleur_k = k

        # Critère demandé dans le sujet
        if ic_moyen > 0.06:
            return k

    # Si aucun k ne passe le seuil, on renvoie le meilleur candidat
    return meilleur_k
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Renvoie la clé (liste d'entiers) estimée en supposant que,
    dans chaque colonne, la lettre la plus fréquente correspond à E.
    """
    decalages = [0] * key_length
    indice_E = ord('E') - ord('A')  # 4

    # 1) construire les colonnes
    colonnes = [""] * key_length
    for i, c in enumerate(cipher):
        colonnes[i % key_length] += c

    # 2) pour chaque colonne, trouver la lettre la plus fréquente
    for j, col in enumerate(colonnes):
        if len(col) == 0:
            decalages[j] = 0
            continue

        idx_max = lettre_freq_max(col)              # index 0..25
        decalages[j] = (idx_max - indice_E) % 26    # k = (max - E) mod 26

    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Devine la longueur de clé (indice de coïncidence), 
    estime la clé en supposant que la lettre la plus fréquente correspond à 'E', 
    puis déchiffre le texte.
    """
    
    key_length = longueur_clef(cipher)
    key = clef_par_decalages(cipher, key_length)
    return dechiffre_vigenere(cipher, key)


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Calcule l’indice de coïncidence mutuelle entre deux histogrammes en décalant h2 de d (mod 26) ; 
    plus la valeur est grande, plus le décalage est probable.    
    """
    n1 = sum(h1)
    n2 = sum(h2)
    if n1 == 0 or n2 == 0:
        return 0.0

    s = 0
    for i in range(26):
        s += h1[i] * h2[(i + d) % 26]

    return s / (n1 * n2)

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Pour chaque colonne j, trouve le décalage d (0..25) qui maximise l’ICM avec la colonne 0 (référence). 
    Renvoie la liste des décalages, avec decalages[0]=0.
    """
    # Construire les colonnes
    colonnes = [""] * key_length
    for i, c in enumerate(cipher):
        if 'A' <= c <= 'Z':
            colonnes[i % key_length] += c

    # Histogramme de référence (colonne 0)
    h0 = freq(colonnes[0])

    decalages = [0] * key_length
    decalages[0] = 0

    # Pour chaque colonne j, chercher le d qui maximise l'ICM
    for j in range(1, key_length):
        hj = freq(colonnes[j])

        best_d = 0
        best_score = -1.0
        for d in range(26):
            score = indice_coincidence_mutuelle(h0, hj, d)
            if score > best_score:
                best_score = score
                best_d = d

        decalages[j] = best_d

    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    '''Estime la longueur de clé, calcule les décalages relatifs par ICM, aligne les colonnes puis déchiffre comme un César en supposant que la lettre la plus fréquente correspond à E.'''
    k = longueur_clef(cipher)
    if k <= 0:
        return ""

    # d[j] ≈ key[j] - key[0] (mod 26)
    d = tableau_decalages_ICM(cipher, k)

    # 1) Aligner toutes les colonnes sur la colonne 0 :
    #    on enlève d[j] à chaque lettre de la colonne j
    aligne = ""
    pos = 0
    
    for c in cipher:
        if 'A' <= c <= 'Z':
            j = pos % k
            aligne += dechiffre_cesar(c, d[j])
            pos += 1
        else:
            # normalement cipher est déjà filtré, mais on garde au cas où
            aligne += c

    # 2) Maintenant aligne est un César de décalage key[0]
    idx_max = lettre_freq_max(aligne)
    idx_E = ord('E') - ord('A')
    decal_cesar = (idx_max - idx_E) % 26

    # 3) Déchiffrement final
    return dechiffre_cesar(aligne, decal_cesar)

################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1, L2):
    """
    Calcule la corrélation linéaire de Pearson entre deux listes de même longueur.

    Retourne une valeur entre -1 et 1 (en pratique).
    Si la variance de L1 ou L2 est nulle, renvoie 0.0.
    """
    n = len(L1)
    if n == 0 or n != len(L2):
        return 0.0

    # moyennes
    m1 = sum(L1) / n
    m2 = sum(L2) / n

    num = 0.0
    s1 = 0.0
    s2 = 0.0

    for x, y in zip(L1, L2):
        dx = x - m1
        dy = y - m2
        num += dx * dy
        s1 += dx * dx
        s2 += dy * dy

    den = math.sqrt(s1) * math.sqrt(s2)
    if den == 0.0:
        return 0.0

    result = num / den

    # Correction des erreurs d'arrondi
    if abs(result - 1.0) < 1e-12:
        return 1.0
    if abs(result + 1.0) < 1e-12:
        return -1.0

    return result

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    colonnes = [""] * key_length
    for i, c in enumerate(cipher):
        colonnes[i % key_length] += c

    key = [0] * key_length
    somme_scores = 0.0

    for j, col in enumerate(colonnes):
        hist = freq(col)

        meilleur_score = -2.0
        meilleur_d = 0  # ici d = décalage "pour réaligner" (inverse)

        for d in range(26):
            # rotation "inverse" simule le déchiffrement de la colonne
            hist_corrige = [0] * 26
            for i2 in range(26):
                hist_corrige[i2] = hist[(i2 - d) % 26]

            sc = correlation(hist_corrige, freq_FR)
            if sc > meilleur_score:
                meilleur_score = sc
                meilleur_d = d

        # conversion vers la clé attendue par le TP : k = -d mod 26
        key[j] = (-meilleur_d) % 26
        somme_scores += meilleur_score

    return (somme_scores / key_length, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Cryptanalyse V3 par corrélations :
    - teste toutes les tailles de clé de 1 à 20
    - pour chaque taille k, calcule (score, key) avec clef_correlations
    - choisit la taille dont le score moyen est maximal
    - déchiffre avec dechiffre_vigenere
    """
    meilleur_score = -2.0
    meilleure_clef = [0]
    meilleure_taille = 1

    for k in range(1, 21):  # clé supposée de taille <= 20
        score_k, key_k = clef_correlations(cipher, k)
        if score_k > meilleur_score:
            meilleur_score = score_k
            meilleure_clef = key_k
            meilleure_taille = k

    # Déchiffrement final avec la meilleure clé trouvée
    return dechiffre_vigenere(cipher, meilleure_clef)


################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
