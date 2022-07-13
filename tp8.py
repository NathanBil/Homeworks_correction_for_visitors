#!/usr/bin/python3.8
import subprocess
import os
import csv

#exécute les fichiers .o et vérifie si ils renvoient la bonne valeur
def test_fic(executable):
	test = 0
	resultat = subprocess.run(["eleves_bis/"+executable, "0","0"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 0 et 0 vaut 0\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "1","0"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 1 et 0 vaut 1\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "0","1"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 0 et 1 vaut 1\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "1","1"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 1 et 1 vaut 2\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "12","12"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 12 et 12 vaut 24\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "12","-43"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de 12 et -43 vaut -31\n'):
		test+=1
	resultat = subprocess.run(["eleves_bis/"+executable, "-1","-52"] ,capture_output=True)
	if(resultat.stdout.decode() == 'La somme de -1 et -52 vaut -53\n'):
		test+=1
	return test

#renvoie le nombre de ligne de documentation
def documentation(file):
	resultat = subprocess.Popen("grep -E '^\/\*|^[ ]+\/\*' eleves_bis/" + file + " | wc -l", shell=True, stdout=subprocess.PIPE)
	out, err = resultat.communicate()
	return(out.decode("utf-8")[0])
	
	
#exécute la commande gcc sur chaque fichier .c
def gcc(file):
	subprocess.run(["gcc", "-ansi" , "-Wall", "eleves_bis/" + file, "-o", "eleves_bis/" + file.replace(".c","")], capture_output=True)

#compte le nombre de Warning de chaque fichier 
def Warning2(file):
	resultat_gcc = subprocess.run(["gcc", "-ansi" , "-Wall", "eleves_bis/" + file, "-o", "eleves_bis/" + file.replace(".c","")], capture_output=True)
	liste = resultat_gcc.stderr.decode()
	liste2 = liste.split("warning:")
	return (len(liste2)-1)

#vérifie si un fichier a créé un exécutable 
def error(file):
	resultat_gcc = subprocess.run(["gcc", "-ansi" , "-Wall", "eleves_bis/" + file, "-o", "eleves_bis/" + file.replace(".c","")], capture_output=True)
	liste = resultat_gcc.stderr.decode()
	liste2 = liste.split("error:")
	#cas où il y a une erreur
	if(len(liste2)-1) >= 1:
		return 0
	#cas où il n'y a pas d'erreur
	else:
		return 1

#fonction qui renvoie le nom de l'étudiant
def nom(file):
	liste = file.split("_")
	liste2 = liste[1].replace(".c","")
	return liste2


#fonction qui renvoie le prenom de l'étudiant
def prenom(file):
	liste = file.split("_")
	return liste[0]

#remplit les lignes des élèves
def remplir(file):
	print(file)
	if error(file) == 0:
		liste = []
		liste.append(nom(file))
		liste[0] = liste[0] + " ; " 
		liste[0] = liste[0] + str(prenom(file))
		liste[0] = liste[0] + " ; " 
		liste[0] = liste[0] + str(error(file))
		liste[0] = liste[0] + " ; " 
		liste[0] = liste[0] + str(Warning2(file))
		liste[0] = liste[0] + " ; "
		liste[0] = liste[0] + str(0)
		liste[0] = liste[0] + " ; "
		liste[0] = liste[0] + str(documentation(file))
		return liste
		
	liste = []
	liste.append(nom(file))
	liste[0] = liste[0] + " ; " 
	liste[0] = liste[0] + str(prenom(file))
	liste[0] = liste[0] + " ; " 
	liste[0] = liste[0] + str(error(file))
	liste[0] = liste[0] + " ; " 
	liste[0] = liste[0] + str(Warning2(file))
	liste[0] = liste[0] + " ; "
	liste[0] = liste[0] + str(test_fic(file.replace(".c","")))
	liste[0] = liste[0] + " ; "
	liste[0] = liste[0] + str(documentation(file))
	return liste
	
subprocess.run(["unzip", "Rendus_eleves.zip"])

process = subprocess.Popen(['ls', 'eleves_bis/'], stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
"""modifier le code pour aller de 0 à n"""
liste = stdout.decode("utf-8").split('\n')[:-1]


with open('file.csv', 'w') as f:
	for i in range(0,len(liste)):
		liste2 = remplir(liste[i])
		writer = csv.writer(f)
		writer.writerow(liste2)