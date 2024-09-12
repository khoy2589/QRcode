import qrcode
from PIL import Image, ImageDraw

# Define the URL for the QR code
url = "https://github.com/khoy2589"  # Replace with your desired URL

# Create a QR code object with enhanced styling options
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo embedding
    box_size=10,
    border=4,
)

# Add the URL data to the QR code
qr.add_data(url)
qr.make(fit=True)

# Create an image with the QR code with a transparent background
qr_img = qr.make_image(fill_color="darkblue", back_color=None).convert("RGBA")

# Adjust the opacity of only the QR code
opacity = 150  # Set opacity level (0-255, where 255 is fully opaque)
qr_alpha = qr_img.split()[3]  # Extract the alpha channel of the QR code
qr_alpha = qr_alpha.point(lambda p: int(p * (opacity / 1)))  # Adjust alpha based on desired opacity
qr_img.putalpha(qr_alpha)  # Apply the modified alpha channel back to the QR code image

# Create a solid background image
bg_color = "white"  # Background color
bg_img = Image.new("RGBA", qr_img.size, bg_color)

# Composite the QR code onto the background
final_img = Image.alpha_composite(bg_img, qr_img)

# Optional: Add a logo in the center of the QR code
logo_path = "logo.png"  # Path to your logo image, if available
try:
    logo = Image.open(logo_path).convert("RGBA")  # Ensure logo has an alpha channel

    # Resize the logo to fit within the QR code
    logo_size = min(final_img.size) // 4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Create a mask for the logo based on its alpha channel
    logo_mask = logo.split()[3]  # Use the alpha channel as the mask

    # Calculate position to place the logo in the center
    logo_pos = ((final_img.size[0] - logo_size) // 2, (final_img.size[1] - logo_size) // 2)
    final_img.paste(logo, logo_pos, mask=logo_mask)  # Use the mask for proper transparency handling
except FileNotFoundError:
    print("Logo not found; generating QR code without a logo.")

# Optional: Add rounded corners or border enhancements
draw = ImageDraw.Draw(final_img)
draw.rectangle([5, 5, final_img.size[0] - 5, final_img.size[1] - 5], outline="gold", width=3)

# Save the fancy QR code image
final_img.save("qrcode.png")
print("Fancy QR code generated and saved as qrcode.png")