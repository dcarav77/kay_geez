from PIL import Image

# Load the image
input_path = "/Users/dustin_caravaglia/Desktop/kg2.jpeg"  # Replace with your image path
output_path = "/Users/dustin_caravaglia/Desktop/resized_image.jpg"  # Desired output file path

# Target dimensions (e.g., for 8.5x11 inches at 300 DPI)
target_width, target_height = 2550, 3300  # Adjust dimensions as needed

# Open the image
with Image.open(input_path) as img:
    # Calculate cropping box to maintain aspect ratio
    aspect_ratio = target_width / target_height
    img_width, img_height = img.size
    img_aspect_ratio = img_width / img_height

    if img_aspect_ratio > aspect_ratio:
        # Wider image: Crop horizontally
        new_width = int(img_height * aspect_ratio)
        left = (img_width - new_width) // 2
        right = left + new_width
        top, bottom = 0, img_height
    else:
        # Taller image: Crop vertically
        new_height = int(img_width / aspect_ratio)
        top = (img_height - new_height) // 2
        bottom = top + new_height
        left, right = 0, img_width

    cropped_img = img.crop((left, top, right, bottom))
    resized_img = cropped_img.resize((target_width, target_height), Image.ANTIALIAS)
    resized_img.save(output_path, quality=95)  # Save with high quality

print(f"Image successfully resized to {target_width}x{target_height} and saved at {output_path}")
