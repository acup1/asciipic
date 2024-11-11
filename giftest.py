from PIL import Image, ImageSequence

seq = Image.open("g1.gif")
list(i.convert("RGBA") for i in ImageSequence.Iterator(seq))