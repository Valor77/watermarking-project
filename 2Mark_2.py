import rawpy # type: ignore
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

print('Printing started.............')

def add_watermarks_and_text(base_image_path, watermark1_path, watermark2_path, output_dir, text):
    # Load the base image
    base_image = Image.open(base_image_path)

    # this code helps stop some images from rotating, because some images store rotation in their metadata
    base_image = ImageOps.exif_transpose(base_image)


    # Load the watermark images
    watermark1 = Image.open(watermark1_path)
    watermark2 = Image.open(watermark2_path)

    # Resize watermarks to fit.
    wm_size = (200, 200)  
    watermark1 = watermark1.resize(wm_size)
    watermark2 = watermark2.resize(wm_size)

    # Define positions for the watermarks (left to right, bottom-left corner)
    watermark1_position = (10, base_image.height - wm_size[1] - 10)
    watermark2_position = (10 + wm_size[0] + 10, base_image.height - wm_size[1] - 10)
    
    # Prepare to draw text
    draw = ImageDraw.Draw(base_image)
    
    # Set the font (ensure you have a valid font file path or use system font)
    font = ImageFont.truetype("arial.ttf", 60)  # Adjust font size as needed
    

    # Define text position (next to the second watermark, left to right)
    text_position = (watermark2_position[0] + wm_size[0] + 10, base_image.height - wm_size[1] + 20)  # Adjust as needed
    text_color = (255, 255, 255)  # White text color

    # Paste the watermarks onto the base image
    base_image.paste(watermark1, watermark1_position, watermark1)
    base_image.paste(watermark2, watermark2_position, watermark2)

    # Add the text to the image
    #print(help(draw.text))
    #draw.text(text_position, text, font=font, fill=text_color)

    # Save the final image to the output directory
    output_path = os.path.join(output_dir, os.path.basename(base_image_path))
    base_image.save(output_path)
    print(f"Processed {base_image_path} and saved to {output_path}")



# to convert .nef(raw Nikkon camera file format) files to surpported file format(.jpg) 
def convert_nef_to_jpg(nef_path, output_dir):
    with rawpy.imread(nef_path) as raw:
        rgb_image = raw.postprocess()
    jpg_filename = os.path.splitext(os.path.basename(nef_path))[0] + ".jpg"
    jpg_path = os.path.join(output_dir, jpg_filename)
    Image.fromarray(rgb_image).save(jpg_path, 'JPEG')
    return jpg_path


    
def process_images_in_directory(input_dir, watermark1_path, watermark2_path, output_dir, text):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


        # Loop over all image files in the directory
    for filename in os.listdir(input_dir):
        base_image_path = os.path.join(input_dir, filename)
        file_extension = os.path.splitext(filename)[1].lower()

        # Check for .nef files and convert to .jpg
        if file_extension == '.nef':
            # Convert NEF to JPG, and update the path to the new jpg
            base_image_path = convert_nef_to_jpg(base_image_path, output_dir)
            print(f"Converted {filename} to JPEG format.")
            add_watermarks_and_text(base_image_path, watermark1_path, watermark2_path, output_dir, text)
        
        # Proceed if it’s already a supported format
        elif file_extension in (".jpg", ".png", ".jpeg", "PNG", ".JPG", ".JPEG"):
            add_watermarks_and_text(base_image_path, watermark1_path, watermark2_path, output_dir, text)

    # # Loop over all image files in the directory
    # for filename in os.listdir(input_dir):
    #     if filename.endswith((".jpg", ".png", ".jpeg","PNG",".JPG", ".JPEG")):
    #         base_image_path = os.path.join(input_dir, filename)
    #         add_watermarks_and_text(base_image_path, watermark1_path, watermark2_path, output_dir, text)
        




# paths drawer.lol
input_dir = r'C:\Users\pc\Desktop\Pro Jets\Input'
watermark1_path = r'C:\Users\pc\Desktop\Pro Jets\mark_holder\watermark1.png'
watermark2_path = r'C:\Users\pc\Desktop\Pro Jets\mark_holder\watermark2.png'
output_dir = r'C:\Users\pc\Desktop\Pro Jets\Image_storage'
# add line to the text side for readability

text = ("THE REDEEMED CHRISTIAN FELLOWISHIP" '\n'" UNICROSS CALABAR CAMPUS")  # Short text for the image

process_images_in_directory(input_dir, watermark1_path, watermark2_path, output_dir, text)

# from PIL import Image

# barca = Image.open('iconic.jpeg')
# lona = Image.open('FCB.png')

# area = (100,200,300,334)

# barca.paste(lona, area)

# barca.show()