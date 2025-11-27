import os
from PIL import Image

# --- S E T T I N G S : ADJUST THESE ---

# 1. Image Paths
TEMPLATE_PATH = "template.png"
QR_CODES_FOLDER = "qr_codes"
OUTPUT_FOLDER = "output_tokens2"

# 2. QR Code Size
# Set the size your QR code should be on the final token.
QR_SIZE = (150, 150)  # (width, height) in pixels. Adjust as needed.

# 3. QR Code Position
# This is the MOST IMPORTANT setting.
# It's the (x, y) coordinate of the TOP-LEFT corner
# where the QR code will be pasted onto the template.
#
# HOW TO FIND IT:
# 1. Open your 'template.png' in MS Paint or any image editor.
# 2. Move your mouse to the top-left corner of the white box.
# 3. Note the (x, y) pixel coordinates at the bottom of the editor.
# 4. Enter those coordinates below.
#
# (I am guessing a position, you MUST change this)
QR_POSITION = (73, 123)  # (X, Y) - REPLACE WITH YOUR COORDINATES

# --- E N D  O F  S E T T I NGS ---


def create_final_tokens():
    """
    Loops through all QR codes, pastes them onto the template,
    and saves them to the output folder.
    """
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Load the base template image
    try:
        base_template = Image.open(TEMPLATE_PATH).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Template file not found at '{TEMPLATE_PATH}'")
        print("Please make sure 'template.png' is in the same folder as the script.")
        return

    # Get a list of all QR code files
    try:
        qr_files = sorted(os.listdir(QR_CODES_FOLDER))
        if not qr_files:
            print(f"Error: No QR codes found in '{QR_CODES_FOLDER}' folder.")
            return
    except FileNotFoundError:
        print(f"Error: '{QR_CODES_FOLDER}' folder not found.")
        print("Please create it and add your QR code images.")
        return

    print(f"Found {len(qr_files)} QR codes. Starting process...")

    # Loop through each QR code file
    for filename in qr_files:
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            qr_path = os.path.join(QR_CODES_FOLDER, filename)
            
            try:
                # Open and resize the QR code
                qr_code = Image.open(qr_path).convert("RGBA")
                qr_code_resized = qr_code.resize(QR_SIZE, Image.LANCZOS)
                
                # Make a copy of the template to work on
                # This is important! Don't paste on the original.
                token_copy = base_template.copy()
                
                # Paste the resized QR code onto the template copy
                # The 'qr_code_resized' is used as a mask for transparency
                token_copy.paste(qr_code_resized, QR_POSITION, qr_code_resized)
                
                # Create the output filename
                output_filename = f"final_{filename}"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                
                # Save the final token
                token_copy.save(output_path)
                
                print(f"Successfully created: {output_filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("-" * 30)
    print("Batch process complete!")
    print(f"All {len(qr_files)} tokens have been saved to the '{OUTPUT_FOLDER}' folder.")


# --- Run the script ---
if __name__ == "__main__":
    create_final_tokens()