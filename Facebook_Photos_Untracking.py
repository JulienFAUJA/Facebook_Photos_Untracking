
from PIL import Image
from glob import glob
import random
import time

terme = ""
type_of_blur = 0
while True:
    print("Sur quoi voulez-vous enlever le pistage Facebook ?")
    choix = input("1. Une Photo unique\n2. Un dossier de Photos")
    if choix == "1":
        terme = "de la photo"
        type_of_blur = 1
        break
    elif choix == "2":
        terme = "du dossier"
        type_of_blur = 2
        break
    else:
        continue
path_ = input("Veuillez entrer le chemin "+terme)

if type_of_blur == 1:
    # Open photo
    startTime = time.time()
    image_path = path_
    im = Image.open(image_path)
    im = Image.eval(im, lambda x: x^1)
    im.save(path_.split('/')[-1][:-4] + "_cleanFB.jpg")
    endTime = time.time()
    print("Durée : " + str(endTime - startTime))
    
elif type_of_blur == 2:
    # Many Photos
    startTime = time.time()
    for pic in glob(path_+"/*"):
        im = Image.open(pic)
        im = Image.eval(im, lambda x: x^1)
        im.save(pic[:-4]+"_cleanFB.jpg")
    endTime = time.time()
    print("Durée : "+str(endTime-startTime))

