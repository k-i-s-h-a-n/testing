import qrcode
from PIL import Image
import img2pdf
# Prompt the user to input values for the fields


exam_name=input("Enter Exam name: ")
exam_id=input("Enter Exam ID: ")
name = input("Enter name: ")
roll_no = input("Enter roll no.: ")
class_ = input("Enter class: ")
section = input("Enter section: ")

# Create a dictionary of the fields and their values
fields = {
    'Exam name':exam_name,
    'Exam ID':exam_id,
    'Name': name,
    'Roll No': roll_no,
    'Class': class_,
    'Section': section
}

# Convert the dictionary to a string
data = '\n'.join([f"{key}: {value}" for key, value in fields.items()])

# Generate the QR code
qr_img = qrcode.make(data)

# Load the student image
bg_img = Image.open('omr24april.jpg')

# Resize the QR code image to fit the student image
qr_img = qr_img.resize((250, 250))

# Calculate the position to paste the QR code image onto the student image
x = bg_img.width - qr_img.width - 1000
y = bg_img.height - qr_img.height - 90

# Paste the QR code image onto the student image
bg_img.paste(qr_img, (x, y))

# Save the QR code as a PNG file with the name of the class name and student roll number
filename = f"{exam_name}_{roll_no}.jpg"
bg_img.save(filename)



#Printing Name and Roll no
# from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# Open the image file
img = Image.open(filename)

# Create a drawing context
draw = ImageDraw.Draw(img)

# Define the font to use
font = ImageFont.truetype("arial.ttf", 30)


# # Determine the size of the text
# text_width, text_height = draw.textsize(name, font)

# Draw the name on the image
x=760
y=1680
draw.text((x, y), name, font=font, fill=(0,0,0))

# Draw the name on the image
roll_x=780
roll_y=1720
draw.text((roll_x, roll_y), roll_no, font=font, fill=(0,0,0))

# Save the modified image
s=f"pdf_check/{exam_name}_{roll_no}.jpg"
img.save(s)


