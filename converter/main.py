import os
from PIL import Image

# Specify the path to the folder containing the JPG images
input_folder = r'C:\Users\cpchun\OneDrive\My PO\PO 平時'
output_folder = r'C:\Users\cpchun\OneDrive\My PO\PO 平時\png'

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):  # Check if the file is a JPG
        # Open the image
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        
        # Convert the filename to PNG format by changing the extension
        png_filename = os.path.splitext(filename)[0] + ".png"
        png_path = os.path.join(output_folder, png_filename)
        
        # Save the image as PNG
        img.save(png_path, "PNG")
        print(f"Converted: {filename} -> {png_filename}")