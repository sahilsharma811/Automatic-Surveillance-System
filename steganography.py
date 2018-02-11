from PIL import Image
def encode_image(tail, image_path):
    print('Encoder..!')
    img = Image.open(image_path)
    encoded_image_file = "enc_" + tail
    secret_msg = input("Enter the secret Message: ")
    length = len(secret_msg)
    # limit length of message to 255
    if length > 255:
        print("text too long! (don't exeed 255 characters)")
        return False
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    print('Encoding....')

    encoded = img.copy()
    width, height = img.size

    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = secret_msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1

    if encoded:
        encoded.save(encoded_image_file)
        print("{} saved!".format(encoded_image_file))

        import webbrowser
        webbrowser.open(encoded_image_file)
    return encoded

def decode_image(tail,encoded_image_file):
    print('Decoder...')
    img = Image.open(encoded_image_file)

    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    print (msg)

if __name__ == '__main__':
    img_encoded = encode_image()
    hidden_text = decode_image()
    print("Hidden text:\n{}".format(hidden_text))
