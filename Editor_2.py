from PIL import Image
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm # type: ignore

opacity = 1.0


# Logging setup
logging.basicConfig(filename='image_processing.log', level=logging.INFO)

# Paths specification
imageInput = r'C:\Users\pc\Desktop\.py\Dah\Image editor\ImageInput'
imageOutput = r'C:\Users\pc\Desktop\.py\Dah\Image editor\ImageOutput'
watermark_path = r'C:\Users\pc\Desktop\.py\logo_bw.png'  # Path to the watermark image

# Create output directory if it doesn't exist
if not os.path.exists(imageOutput):
    os.makedirs(imageOutput)


# Open the watermark image and convert it to RGBA (for transparency)
print('image conversion starting...................')
print(f"Trying to open watermark from: {watermark_path}")
watermark = Image.open(watermark_path).convert("RGBA")


# Resize the watermark if necessary
watermark = watermark.resize((100, 100))  # Resize watermark (adjust as needed)



# Function to adjust opacity of watermark
def adjust_opacity(image, opacity):
    """Adjust opacity of an RGBA image."""
    alpha = image.split()[3]  # Extract alpha channel
    alpha = alpha.point(lambda p: p * opacity)  # Modify alpha by a factor
    image.putalpha(alpha)  # Update image with new alpha channel
    return image

# # Adjust watermark opacity
print('Adjusting opacity.......\n')
opacity = 1.0  # 1.0 for fully opaque, 0.0 for fully transparent
watermark = adjust_opacity(watermark, opacity)

# Function to get watermark position dynamically
print('Water-Mark locaton specification...............')


def get_watermark_position(image, watermark, position="bottom-right"):
    if position == "bottom-right":
        return (image.width - watermark.width - 10, image.height - watermark.height - 10)
    elif position == "bottom-left":
        return (10, image.height - watermark.height - 10)
    elif position == "top-right":
        return (image.width - watermark.width - 10, 10)
    elif position == "center":
        return ((image.width - watermark.width) // 2, (image.height - watermark.height) // 2)
    else:
        return (image.width - watermark.width - 10, image.height - watermark.height - 10)
    


# Function to apply image enhancements
print('Applying Image enhacements...............')
def apply_enhancements(image, brightness_factor=1.2, contrast_factor=2.0):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(contrast_factor)


# Function to add watermark (supports both text and image watermarks)
def add_watermark(image, watermark, text=None, position="bottom-right"):
    if text:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 36)
        draw.text((10, 10), text, font=font, fill="white")
    elif watermark:
        watermark = watermark.convert("RGBA")  # Ensure's that watermark has an alpha channel
        pos = get_watermark_position(image, watermark, position)
        image.paste(watermark, pos, watermark)  # Paste watermark with transparency
    return image



# Function to process a single image
print('Attempting Image processing...............')

def process_image(filename):
    try:
        img_path = os.path.join(imageInput, filename)
        img = Image.open(img_path).convert("RGBA")

        # Apply different filters and save the results
        # 1. Grayscale with Sharpen
        grayscale_img = img.convert('L').filter(ImageFilter.SHARPEN).convert("RGB")
        grayscale_img = add_watermark(grayscale_img, watermark, position="bottom-right")
        grayscale_img.save(os.path.join(imageOutput, f'{filename}_grayscale.jpg'))

        # 2. Increased Brightness
        bright_img = apply_enhancements(img, brightness_factor=1.5)
        bright_img = add_watermark(bright_img.convert("RGB"), watermark, position="bottom-right")
        bright_img.save(os.path.join(imageOutput, f'{filename}_bright.jpg'))

        # 3. Increased Contrast
        contrast_img = apply_enhancements(img, contrast_factor=2.0)
        contrast_img = add_watermark(contrast_img.convert("RGB"), watermark, position="bottom-right")
        contrast_img.save(os.path.join(imageOutput, f'{filename}_contrast.jpg'))

        logging.info(f"Successfully processed {filename}")
        print(f"Editing completed for {filename}")

    except Exception as e:
        logging.error(f"Failed to process {filename}: {e}")
        print(f"Error processing {filename}: {e}")



# Function to batch process images using threading
print('About to start batch processing...........')
def batch_process_images():
    filenames = [f for f in os.listdir(imageInput) if f.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(tqdm(executor.map(process_image, filenames), total=len(filenames)))



if __name__ == "__main__":
    print('Starting batch image processing...')
    batch_process_images()
    print('Batch processing complete!')
