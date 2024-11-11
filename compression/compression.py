from PIL import Image
Original_image = Image.open("E:\HAPPY.jpg")
Original_image.save("HAPPY", "JPEG", quality=2)

Compressed_image = Image.open("HAPPY")

Original_image.show()
Compressed_image.show()
