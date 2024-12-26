import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import binascii


# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)


# Convert binary to text
def binary_to_text(binary_data):
    binary_values = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_characters)


# Encode the message into the image
def encode_message(image, message):
    # Convert message to binary
    binary_message = text_to_binary(message)
    binary_message += '1111111111111110'  # Adding a delimiter to mark the end of the message

    # Get the image's pixels
    pixels = image.load()
    width, height = image.size
    data_index = 0

    # Modify the LSB of pixels to embed the message
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):  # Loop through RGB values
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])  # Update the LSB
                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    return image


# Decode the message from the image
def decode_message(image):
    # Get the image's pixels
    pixels = image.load()
    width, height = image.size

    binary_data = ''
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):  # Loop through RGB values
                binary_data += str(pixel[i] & 1)  # Extract the LSB

    # Find the delimiter (end of the message) and strip the binary data
    end_index = binary_data.find('1111111111111110')
    if end_index != -1:
        binary_data = binary_data[:end_index]

    return binary_to_text(binary_data)


# Save the encoded image
def save_encoded_image(encoded_image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")])
    if file_path:
        encoded_image.save(file_path)
        messagebox.showinfo("Success", f"Image saved successfully as {file_path}")


# Main encoding function
def encode_image():
    img_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not img_path:
        messagebox.showerror("Error", "No image selected")
        return

    image = Image.open(img_path)

    message = message_entry.get()
    if not message:
        messagebox.showerror("Error", "No message entered")
        return

    encoded_image = encode_message(image, message)
    save_encoded_image(encoded_image)


# Main decoding function
def decode_image():
    img_path = filedialog.askopenfilename(title="Select an Encoded Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not img_path:
        messagebox.showerror("Error", "No image selected")
        return

    image = Image.open(img_path)
    decoded_message = decode_message(image)

    decoded_text.set(decoded_message)


# Setting up the GUI
root = tk.Tk()
root.title("Image Steganography")
root.geometry("600x400")

# Encoding section
tk.Label(root, text="Enter the message to encode into an image:").pack(pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)

encode_button = tk.Button(root, text="Encode Message into Image", command=encode_image)
encode_button.pack(pady=20)

# Decoding section
tk.Label(root, text="Decoded Message:").pack(pady=10)
decoded_text = tk.StringVar()
decoded_label = tk.Label(root, textvariable=decoded_text, width=50, height=4, relief="sunken")
decoded_label.pack(pady=10)

decode_button = tk.Button(root, text="Decode Message from Image", command=decode_image)
decode_button.pack(pady=20)

root.mainloop()
