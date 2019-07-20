
from PIL import Image
from glob import glob
import random
import time

# Functions

def BlurFacebookTracking(x):
    bits = list(range(9))
    rand_bit_r = random.choice(bits)
    rand_bit_g = random.choice(bits)
    rand_bit_b = random.choice(bits)
    new_pixel = (x[0]-rand_bit_r,x[1]-rand_bit_g,x[2]-rand_bit_b)
    # L'affichage de la preuve de l'efficacité de l'algorithme (ligne suivante) alourdi considérablement le temps d'exécution...
    #print("AncienPixel : "+str(x)+"\nNouveau Pixel : "+str(new_pixel)+"\n"+200*"*"+"\n\n")
    return new_pixel


def ResizeImage(w,h, im):
    (width, height) = (w, h)
    im3 = im.resize((width, height))
    return im3

def ResizeImageByRatio(ratio, im):
    (width, height) = (im.width // ratio, im.height // ratio)
    im3 = im.resize((width, height))
    return im3

# Menu
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


# Resize
resize_choice = "0"
own_w = "0"
own_h = "0"

while True:
    if type_of_blur == 1:
        print("Voulez-vous redimentionnez l'image pour accelérer le processus ?")

    elif type_of_blur == 2:
        print("Voulez-vous redimentionnez les images pour accelérer le processus ?")

    resize_choice = input("""
        1. Non\n
        2. Oui, en entrant mes propres valeurs (largeur/hauteur)\n
        3. Oui, avec un ratio de 2 pour largeur et hauteur\n
        4. Oui, avec un ratio de 4 pour largeur et hauteur\n
        """)

    if int(resize_choice) > 0 and int(resize_choice) < 5:
        if int(resize_choice) == 2:
            own_w = int(input("Entrez la largeur en pixels"))
            own_h = int(input("Entrez la hauteur en pixels"))
        break
# Run

if type_of_blur == 1:
    # Open photo
    startTime = time.time()
    image_path = path_
    im = Image.open(image_path)

    # Resize
    if int(resize_choice) == 2:
        # Own value
        im = ResizeImage(own_w, own_h, im)
    elif int(resize_choice) == 3:
        im = ResizeImageByRatio(2, im)
    elif int(resize_choice) == 4:
        im = ResizeImageByRatio(4, im)

        # Run

    pic_data = list(im.getdata())
    res = map(BlurFacebookTracking, pic_data)

    #print(list(res))

    im2 = im.copy()
    im2.putdata(list(res))

    im2.save(path_.split('/')[-1][:-4] + "_cleanFB.jpg")

    endTime = time.time()

    print("Durée : " + str(endTime - startTime))


elif type_of_blur == 2:
    # Many Photos
    startTime = time.time()
    for pic in glob(path_+"/*"):
        im = Image.open(pic)
        # Resize
        if int(resize_choice) == 2:
            # Own value
            im = ResizeImage(own_w, own_h, im)
        elif int(resize_choice) == 3:
            im = ResizeImageByRatio(2, im)
        elif int(resize_choice) == 4:
            im = ResizeImageByRatio(4, im)

        pic_data = list(im.getdata())
        res = map(BlurFacebookTracking, pic_data)

        #print(list(res))

        im2 = im.copy()
        im2.putdata(list(res))


        im2.save(pic[:-4]+"_cleanFB.jpg")

    endTime = time.time()
    print("Durée : "+str(endTime-startTime))

