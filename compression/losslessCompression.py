from PIL import Image

# Specify file paths using double backslashes or a raw string
original_image_path = "E:\HAPPY.jpg"

# Open the original image
original_image = Image.open(original_image_path)

# Save the compressed image in PNG format (lossless)
compressed_image_path = "compressed_HAPPY.png"
original_image.save(compressed_image_path, 'PNG')

# Open the compressed image
compressed_image = Image.open(compressed_image_path)

# Display the original and compressed images
original_image.show()
compressed_image.show()