
from PIL import Image
from glob import glob
import random
import time

"""
n255 = 225
n = 15
print(str(bin(n255)[2:]).rjust(8)+" -> "+str(n255))
print(str(bin(n)[2:]).rjust(8)+" -> "+str(n))
print(10*"-")
#resn = n&n255
res_xor = n^n255
#resn = n&n255
print(str(bin(res_xor)[2:]).rjust(8)+" -> "+str(res_xor))
print(str(res_xor).rjust(8))
quit()

bits = list(range(8))
r = random.choice(bits)
rnd_px_r = random.choice(list(range(256)))
rnd_px_g = random.choice(list(range(256)))
rnd_px_b = random.choice(list(range(256)))
x = rnd_px_r,rnd_px_g,rnd_px_b
print("pix : "+str(x))
print("bit : "+str(r))
pix = (x[0]&r,x[1]&r,x[2]&r)
print(pix)
quit()
"""
# Functions

def BlurFacebookTracking3(x):
    #bits = list(range(15))
    #rand_bit = random.choice(bits)
    x1 = list(x)
    x1[0]^=7
    x1[1]^=7
    x1[2]^=7
    new_pixel = tuple(x1) # x[0]&=rand_bit,x[1]&rand_bit,x[2]&rand_bit)
    # L'affichage de la preuve de l'efficacité de l'algorithme (ligne suivante) alourdi considérablement le temps d'exécution...
    #print("AncienPixel : "+str(x)+"\nNouveau Pixel : "+str(new_pixel)+"\n"+200*"*"+"\n\n")
    return new_pixel



def BlurFacebookTracking(x):
    bits = list(range(15))
    rand_bit = random.choice(bits)
    x1 = list(x)
    x1[0]-=x1[0]&rand_bit
    x1[1]-=x1[1]&rand_bit
    x1[2]-=x1[2]&rand_bit
    new_pixel = tuple(x1) # x[0]&=rand_bit,x[1]&rand_bit,x[2]&rand_bit)
    # L'affichage de la preuve de l'efficacité de l'algorithme (ligne suivante) alourdi considérablement le temps d'exécution...
    print("AncienPixel : "+str(x)+"\nNouveau Pixel : "+str(new_pixel)+"\n"+200*"*"+"\n\n")
    return new_pixel


def BlurFacebookTracking2(x):
    bits = list(range(9))
    rand_bit_r = random.choice(bits)
    rand_bit_g = random.choice(bits)
    rand_bit_b = random.choice(bits)
    new_pixel = (x[0]-rand_bit_r,x[1]-rand_bit_g,x[2]-rand_bit_b)
    #new_pixel = (x[0]&rand_bit,x[1]&rand_bit,x[2]&rand_bit)
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

# Juste pour éviter de mettre en commentaire cette partie...
if int(resize_choice) > 0:
    while True:
        if type_of_blur == 1:
            print("Voulez-vous redimentionner l'image pour accelérer le processus ?")

        elif type_of_blur == 2:
            print("Voulez-vous redimentionner les images pour accelérer le processus ?")

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


    # Juste pour éviter de mettre en commentaire cette partie...
    if int(resize_choice) > 0:
        # Resize
        if int(resize_choice) == 2:
            # Own value
            im = ResizeImage(own_w, own_h, im)
        elif int(resize_choice) == 3:
            im = ResizeImageByRatio(2, im)
        elif int(resize_choice) == 4:
            im = ResizeImageByRatio(4, im)



        # Run

    #pic_data = list(im.getdata())
    #res = map(BlurFacebookTracking, pic_data)
    im = Image.eval(im, lambda x: x^1)

    #print(list(res))

    #im2 = im.copy()
    #im2.putdata(list(res))


    im.save(path_.split('/')[-1][:-4] + "_cleanFB.jpg")
    #im2.save(path_.split('/')[-1][:-4] + "_cleanFB.jpg")

    endTime = time.time()

    print("Durée : " + str(endTime - startTime))


elif type_of_blur == 2:
    # Many Photos
    startTime = time.time()
    for pic in glob(path_+"/*"):
        im = Image.open(pic)

        # Juste pour éviter de mettre en commentaire cette partie...
        if int(resize_choice) > 0:
            # Resize
            if int(resize_choice) == 2:
                # Own value
                im = ResizeImage(own_w, own_h, im)
            elif int(resize_choice) == 3:
                im = ResizeImageByRatio(2, im)
            elif int(resize_choice) == 4:
                im = ResizeImageByRatio(4, im)

        #pic_data = list(im.getdata())
        #res = map(BlurFacebookTracking, pic_data)
        im = Image.eval(im, lambda x: x^1)
        #print(list(res))

        #im2 = im.copy()
        #im2.putdata(list(res))


        #im2.save(pic[:-4]+"_cleanFB.jpg")
        im.save(pic[:-4]+"_cleanFB.jpg")

    endTime = time.time()
    print("Durée : "+str(endTime-startTime))

