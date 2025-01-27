"""Ce fichier définit des fonctions utiles pour le programme pendu.
On utilise les données du programme contenues dans donnees.py"""
import os
import pickle
from random import randrange
from donnees import *
import Pyro4


@Pyro4.expose
class Server():
    # Gestion des scores

    def recup_scores(self):

        """Cette fonction récupère les scores enregistrés si le fichier existe.
        Dans tous les cas, on renvoie un dictionnaire, soit l'objet dépicklé, soit un dictionnaire vide.
        On s'appuie sur nom_fichier_scores défini dans donnees.py"""

        if os.path.exists(nom_fichier_scores): # Le fichier existe
        # On le récupère
            fichier_scores = open(nom_fichier_scores, "rb")
            mon_depickler = pickle.Unpickler(fichier_scores)
            scores = mon_depickler.load()
            fichier_scores.close()
        else: # Le fichier n'existe pas
            scores = {}
        return scores

    def enregistrer_scores(self, scores):

        """Cette fonction se charge d'enregistrer les scores dans le fichier nom_fichier_scores.
        Elle reçoit en paramètre le dictionnaire des scores à enregistrer"""

        fichier_scores = open(nom_fichier_scores, "wb") # On écrase les anciens scores
        mon_pickler = pickle.Pickler(fichier_scores)
        mon_pickler.dump(scores)
        fichier_scores.close()

    # Fonctions gérant les éléments saisis par l'utilisateur

    def recup_nom_utilisateur(self, username):
        """Fonction chargée de récupérer le nom de l'utilisateur.
        Le nom de l'utilisateur doit être composé de 4 caractères minimum, chiffres et lettres exclusivement.
        Si ce nom n'est pas valide, on appelle récursivement la fonction pour en obtenir un nouveau"""
        
        

        # On met la première lettre en majuscule et les autres en minuscules
        nom_utilisateur = username.capitalize()

        if not nom_utilisateur.isalnum() or len(nom_utilisateur)<4:
            print("Ce nom est invalide.")
            
            # On appelle de nouveau la fonction pour avoir un autre nom
            return self.recup_nom_utilisateur()
        else:
            return nom_utilisateur

    def recup_lettre(self, saisi):

        """Cette fonction récupère une lettre saisie par l'utilisateur. Si la chaîne récupérée n'est pas une lettre,
        on appelle récursivement la fonction jusqu'à obtenir une lettre"""

        lettre = saisi.lower()
        if len(lettre)>1 or not lettre.isalpha():
            print("Vous n'avez pas saisi une lettre valide.")
            return self.recup_lettre()
        else:
            return lettre

    # Fonctions du jeu de pendu

    def choisir_mot(self): 
        """Cette fonction renvoie le mot choisi dans la liste des mots liste_mots.
        On utilise la fonction choice du module random (voir l'aide)."""
        word = randrange(len(liste_mots))
        return liste_mots[word]

    def recup_mot_masque(self, mot_complet, lettres_trouvees):

        """Cette fonction renvoie un mot masqué tout ou en partie, en fonction :
        - du mot d'origine (type str)
        - des lettres déjà trouvées (type list)
        On renvoie le mot d'origine avec des * remplaçant les lettres que l'on n'a pas encore trouvées."""

        mot_masque = ""
        for lettre in mot_complet:
            if lettre in lettres_trouvees:
                mot_masque += lettre
            else:
                mot_masque += "*"
        return mot_masque

    def ajouter_mot(self, liste_mots):
        #Cette foction permet aux gagnant d'aujouter de nouveaux mots

        nouveau_mot = input("Souhaitez vous enrichir notre dictionnaire? (o/n) ")
        if nouveau_mot == 'o':
            nouveau_mot = input("Tapez votre mot: ")
            if nouveau_mot in liste_mots:
                print("Merci mais votre mot fait déjà partir de notre jeu")
            else:
                liste_mots.append(nouveau_mot)
                

# daemon = Pyro4.Daemon()                # make a Pyro daemon
# ns = Pyro4.locateNS()                  # find the name server
# uri = daemon.register(Server)   # register the greeting maker as a Pyro object
# ns.register("example.server", uri)   # register the object with a name in the name server

# print("Ready.")
# daemon.requestLoop()
def main():
    dmn=Pyro4.Daemon(host="0.0.0.0", port=9091)
    Pyro4.Daemon.serveSimple(
        {Server(): 'example.pendu'}, 
        daemon=dmn,
        ns=False, 
    )

if __name__=="__main__":
    main()
