# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : ZEQO Ermal 21315866
# Etudiant.e 2 : FERROUKH Mohamed Nassim 21308499

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def calc_freq(nom_fichier: str) -> list[float]:
    """Calcule les fréquences des 26 lettres (A..Z) dans un fichier texte."""
    with open(nom_fichier, "r", encoding="latin-1") as f:
        txt = f.read().upper()

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


#Test de frequence_lettres
#print(freq_FR)

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

#Test de chiffre_cesar

'''
print("Test chiffre_cesar")
assert chiffre_cesar("ALICE",0) == "ALICE"
assert chiffre_cesar("ALICE",3) == "DOLFH"
print("Test chiffre_cesar : OK")
'''

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

#Test de dechiffre_cesar
'''
print("Test dechiffre_cesar")
assert dechiffre_cesar("ALICE",0) == "ALICE"
assert dechiffre_cesar("ALICE",23) == "DOLFH"
print("Test dechiffre_cesar : OK")
'''
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
    Documentation à écrire
    """
    return "TODO"


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Documentation à écrire
    """
    return 0.0

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Documentation à écrire
    """
    decalages=[0]*key_length
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Documentation à écrire
    """
    return 0.0

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Documentation à écrire
    """
    key=[0]*key_length
    score = 0.0
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


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
