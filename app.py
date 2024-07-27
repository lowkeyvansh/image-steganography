from PIL import Image
import numpy as np

def encode_message(image_path, message, output_path):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Convert the image to a numpy array
    img_array = np.array(image)
    
    # Append a delimiter to the message
    message += '##'
    
    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Ensure the message fits in the image
    if len(binary_message) > img_array.size:
        raise ValueError("Message too long to encode in this image.")
    
    # Encode the message in the image
    flat_array = img_array.flatten()
    for i in range(len(binary_message)):
        flat_array[i] = (flat_array[i] & ~1) | int(binary_message[i])
    
    # Reshape the array back to the image dimensions
    img_array = flat_array.reshape(img_array.shape)
    
    # Save the new image with the hidden message
    encoded_image = Image.fromarray(img_array)
    encoded_image.save(output_path)
    print(f"Message encoded and saved to {output_path}")

def decode_message(image_path):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Convert the image to a numpy array
    img_array = np.array(image)
    
    # Flatten the array
    flat_array = img_array.flatten()
    
    # Extract the binary message
    binary_message = ''.join(str(flat_array[i] & 1) for i in range(len(flat_array)))
    
    # Find the delimiter
    delimiter_index = binary_message.find('001000000011001000000001')
    if delimiter_index == -1:
        raise ValueError("No message found.")
    
    # Extract the message
    binary_message = binary_message[:delimiter_index]
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    print(f"Decoded Message: {message}")

# Example usage
if __name__ == "__main__":
    encode_message('input_image.png', 'Hello, World!', 'encoded_image.png')
    decode_message('encoded_image.png')
