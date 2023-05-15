




        


from pyzbar.pyzbar import decode
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol

# Load the QR code image
img = Image.open('4d.jpg')

# Decode the QR code image
result = decode(img, symbols=[ZBarSymbol.QRCODE])

# Print the decoded text
print(result[0].data.decode("utf-8"))







