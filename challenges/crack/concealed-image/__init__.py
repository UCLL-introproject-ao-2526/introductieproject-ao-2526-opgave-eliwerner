from PIL import Image, ImageEnhance

# laad afbeelding

img = Image.open("whoami.png")

# contrast verhogen (sterk omhoog)
contrast = ImageEnhance.Contrast(img)
img = contrast.enhance(10) # 10 is veel, maar goed voor verborgen lijnen


# brightness verlagen
brightness = ImageEnhance.Brightness(img)
img = brightness.enhance(0.3) # lager = donkerder

# extra: sharpness verhogen
sharpness = ImageEnhance.Sharpness(img)
img = sharpness.enhance(5) 

# opslaan als nieuwe file
img.save("whoami_revealed.png")

print("Afbeelding opgeslagen als whoami_revealed.png")



# chatgpt heeft me hiermee geholpen

