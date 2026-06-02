from PIL import Image

# img = Image.open("Stonehenge2007_07_30.jpg").convert("RGB")
# img.save("content.jpg", "JPEG")
#
# img = Image.open("Vincent van Gogh Wheatfield with Crows 1890.webp").convert("RGB")
# img.save("style.jpg", "JPEG")

img = Image.open("stephen mulhern.webp").convert("RGB")
img.save("content.jpg", "JPEG")

img = Image.open("creation-of-adam-sistine-chapel.webp").convert("RGB")
img.save("style.jpg", "JPEG")


