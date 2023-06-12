from PIL import Image

# Define a custom character set with varying intensity
ascii_chars = '@%#*+=-:. '

def image_to_ascii(image_path, width):
    # Open the image and resize it
    image = Image.open(image_path)
    aspect_ratio = image.width / image.height
    height = int(width / aspect_ratio)
    image = image.resize((width, height))

    # Convert the image to grayscale
    image = image.convert('L')

    # Define the custom character set
    char_set = list(ascii_chars)
    char_set = char_set[::-1]  # Reverse the character set for better intensity mapping

    # Convert each pixel to an ASCII character based on intensity
    ascii_image = ''
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            char_index = int(pixel / 256 * len(char_set))
            ascii_image += char_set[char_index]
        ascii_image += '\n'
    
    return ascii_image

# Example usage
image_path = '60103642ed389ef50e31a8b29d7fdd5c--floyd-mayweather--cent.jpg'
output_width = 80

ascii_image = image_to_ascii(image_path, output_width)
print(ascii_image)

