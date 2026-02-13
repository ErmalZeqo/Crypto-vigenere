# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : ZEQO Ermal 21315866
# Etudiant.e 2 : FERROKH Mohamed Nassim 21308499

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
    Documentation à écrire
    """
    return txt

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Documentation à écrire
    """
    return txt

# Analyse de fréquences
def freq(txt):
    """
    Documentation à écrire
    """
    hist=[0.0]*len(alphabet)
    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Documentation à écrire
    """
    return 0

# indice de coïncidence
def indice_coincidence(hist):
    """
    Documentation à écrire
    """
    return 0.0

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Documentation à écrire
    """
    return 0
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Documentation à écrire
    """
    decalages=[0]*key_length
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
