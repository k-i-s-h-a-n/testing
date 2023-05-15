



from django.shortcuts import render
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import redirect
import os



import cv2
import numpy as np
from Teachers import utlis
from Teachers import new_utils
from Teachers import read_qr_and_scan
import glob



from django.contrib.auth.decorators import login_required


# Create your views here.

def bulana():
    import os
    import uuid
    from django.conf import settings
    unique_omrfolder_name = uuid.uuid4().hex
    upload_folder = os.path.join(settings.MEDIA_ROOT, unique_omrfolder_name)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
            
                # print("!!!!!!!!!!! : ",upload_folder)
                # path = r"C:\Users\kishf\OneDrive\Desktop\OMR\env\Scripts\ExamSystem\media\c4c2d01773974a829e23a83a0772fc35"
    filename = upload_folder.split('\\')[-1]
                # print("@@@@@@@@@@@ ",filename)
            # print("K I S H A N     B H A I   F U N C T I O N    K     A N D H A R")

    return filename






# ___________________________________________________

# S I G N U P
from .forms import SignUpForm
def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account Created Successfully !! ')
            fm.save()
    else:
        # print("else----------------")
        fm=SignUpForm()
    return render(request,'enroll/signup.html',{'form':fm})


# L O G I N
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
def teachers_login(request):
    if not  request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                teachers_username=fm.cleaned_data['username']
                teachers_password=fm.cleaned_data['password']
                user=authenticate(username=teachers_username,password=teachers_password)
                if user is not None:
                    login(request,user)
                    if request.GET.get('next',None):
                        return redirect(request.GET['next'])
                        
                    # messages.success(request,'Logged in successfully !! ')
                    request.session['teacher_id']=user.id
                    request.session['teacher_username']=user.username
                    return redirect("/")
        else:
            # print("else----------------")
            fm=AuthenticationForm()
        return render(request,'enroll/teacherslogin.html',{'form':fm})
    else:
        return redirect('/')




# L O G O U T
def teachers_logout(request):
    logout(request)
    return redirect('/login')



def index(request):
    if request.user.is_authenticated:
        print('HHH you are : ',request.session.get('teacher_username'))
        return render(request,'index.html')
    else:
        return redirect("/login")


# ___________________________________________________






# def loginuser(request):
#     if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:            
#             # A backend authenticated the credentials
#             login(request,user)
#             return redirect('/')
#         else:
#             # No backend authenticated the credentials
#             return render(request,'login.html')

#     return render(request,'login.html')


# def questions(request):
#     return render(request,'questions.html')


# def logoutuser(request):
#     logout(request)
#     return redirect("/login")



# --------------------QUESTION PAPER DOWNLOAD------------------------
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


@login_required(login_url="/login")
def generate_pdf(request):
    # Render the HTML template to a string
    html = render_to_string('questions.html')

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Generate the PDF using the buffer
    pisa.CreatePDF(html, dest=buffer)

    # Use the buffer content to create a PDF response
    pdf = buffer.getvalue()
    buffer.close()

    # Set the content type of the response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
    return response






# --------------------OMR PAPER UPLOAD------------------------
from django.shortcuts import redirect, render  
from .forms import ImageForm
from .models import Image  

@login_required(login_url="/login")
def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = ImageForm()
    return render(request, "upload_image.html", {"form": form})










@login_required(login_url="/login")
def success(request):
    return HttpResponse("Image uploaded successfully")



@login_required(login_url="/login")
def omr(request):
    return render(request,"omr_generation.html")


from django.contrib import messages
def search(request):
    if request.method == 'POST':
        exam_center = request.POST['exam_center']
        classes = request.POST['classes']
        subject = request.POST['subject']
        if not (exam_center or classes or subject):
            messages.error(request, 'Please provide Details')
            return redirect('search')
        elif not exam_center:
            messages.error(request, 'Please provide Exam center')
            return redirect('search')
        elif not classes:
            messages.error(request, 'Please provide Class')
            return redirect('search')
        elif not subject:
            messages.error(request, 'Please provide Subject')
            return redirect('search')
        return redirect('search_results', exam_center=exam_center,classes=classes,subject=subject)
    return render(request, 'search.html')









######################################
####################################
###################################




from django.contrib import messages
@login_required(login_url="/login")
def scan_search(request):
    if request.method == 'POST':
        exam_center = request.POST['exam_center']
        classes = request.POST['classes']
        subject = request.POST['subject']
        if not (exam_center or classes or subject):
            messages.error(request, 'Please provide Details')
            return redirect('scan_search')
        elif not exam_center:
            messages.error(request, 'Please provide Exam center')
            return redirect('scan_search')
        elif not classes:
            messages.error(request, 'Please provide Class')
            return redirect('scan_search')
        elif not subject:
            messages.error(request, 'Please provide Subject')
            return redirect('scan_search')
        return redirect('rrr', exam_center=exam_center,classes=classes,subject=subject)
    return render(request, 'scan_omr/scan_search.html')




@login_required(login_url="/login")
def scan_search_results(request, exam_center,classes,subject):
    # perform search based on exam_center an classes
    data = Qr.objects.filter(center_code=exam_center,classes=classes,subject=subject)
    
   
    # print(data)
    url = f"/upload/{exam_center}/{classes}/{subject}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"no_data_found.html")
        
    return render(request, 'upload.html',context)




######################################
####################################
###################################









@login_required(login_url="/login")
def search_results(request, exam_center,classes,subject):
    # perform search based on exam_center an classes
    data = Qr.objects.filter(center_code=exam_center,classes=classes,subject=subject)
    
   
    # print(data)
    url = f"/omr_gen_dow/{exam_center}/{classes}/{subject}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"no_data_found.html")
        
    return render(request, 'search_results.html',context)












############# A D D I N G    D A T A  ################
@login_required(login_url="/login")
def add_data(request):
    if request.method=="POST":
        Exam_name=request.POST.get('exam_name')
        Exam_id=request.POST.get('exam_id')
        Name=request.POST.get('name')
        Roll_no=request.POST.get('roll_no')
        classes=request.POST.get('classes')
        section=request.POST.get('section')
        center_code=request.POST.get('center_code')
        subject=request.POST.get('subject')
        add_data=Qr(Exam_name=Exam_name,Exam_id=Exam_id,Name=Name,Roll_no=Roll_no,classes=classes,section=section,center_code=center_code,subject=subject)
        add_data.save()
        messages.success(request, 'Your response has been recorded!')
        
    return render(request,'add_data.html')

##############################################







############### D O W N L O A D I N G ############





#################### O M R   G E N E R A T I O N ####################################

from .models import Qr
@login_required(login_url="/login")


def omr_gen_dow(request,student_id,classes,subject):
    try:      
        import qrcode
        from PIL import Image
        import img2pdf
        import os
        import shutil
        
        # deleting the media/media path contents as to clear all the previous generated pdf's

        # Specify the path of the folder
        folder_path = "media\media"

        # Iterate over the contents of the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # Delete individual files
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # Recursively delete subfolders
                shutil.rmtree(file_path)
        
        # student = Qr.objects.get(center_code=student_id)
        # Create a dictionary of the fields and their values
        qr_objects = Qr.objects.filter(center_code=student_id,classes=classes,subject=subject)

        # # q r   o n l y
        # def bulana():
        #     import os
        #     import uuid
        #     from django.conf import settings
        #     unique_omrfolder_name = uuid.uuid4().hex
        #     upload_folder = os.path.join(settings.MEDIA_ROOT, unique_omrfolder_name)
        #     if not os.path.exists(upload_folder):
        #         os.makedirs(upload_folder)
            
        #         # print("!!!!!!!!!!! : ",upload_folder)
        #         # path = r"C:\Users\kishf\OneDrive\Desktop\OMR\env\Scripts\ExamSystem\media\c4c2d01773974a829e23a83a0772fc35"
        #     filename = upload_folder.split('\\')[-1]
        #         # print("@@@@@@@@@@@ ",filename)
        #     # print("K I S H A N     B H A I   F U N C T I O N    K     A N D H A R")

        #     return filename

        qr_only=bulana()
        
        omrs=bulana()
        


        for student in qr_objects:
            fields = {
                'Exam name':student.Exam_name,
                'Exam ID':student.Exam_id,
                'Name': student.Name,
                'Roll No':student.Roll_no,
                'Class': student.classes,
                'Section': student.section,
                'Exam code':student.center_code,
                'Subject':student.subject,
            }

            # Convert the dictionary to a string
            data = '\n'.join([f"{key}: {value}" for key, value in fields.items()])
            # print("D A T A = ",data)

            # Generate the QR code
            qr_img = qrcode.make(data)

            # Load the qr_template image
            bg_img = Image.open('omr24april.jpg')

            # Resize the QR code image to fit the student image
            qr_img = qr_img.resize((250, 250))

            # Calculate the position to paste the QR code image onto the student image
            x = bg_img.width - qr_img.width - 1000
            y = bg_img.height - qr_img.height - 90

            # Paste the QR code image onto the student image
            bg_img.paste(qr_img, (x, y))

            
            
            
            
            
            # Save the QR code as a PNG file with the name of the class name and student roll number
            # filename = f"media/qr_only/{student.Exam_name}_{student.Roll_no}.jpg"
            # print("K I S H A N     B H A I")
        
            filename = f"media/{qr_only}/{student.Exam_name}_{student.Roll_no}.jpg"
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
            draw.text((x, y), student.Name, font=font, fill=(0,0,0))

            # Draw the name on the image
            roll_x=780
            roll_y=1720
            draw.text((roll_x, roll_y), student.Roll_no, font=font, fill=(0,0,0))

            # Save the modified image
            # s=f"media/omrs/{student.Exam_name}_{student.Roll_no}.jpg"
            # omrs=bulana()
            s=f"media/{omrs}/{student.Exam_name}_{student.Roll_no}.jpg"

            img.save(s)
            
            
            
            ######  A L L   J P G   T O   P D F ########
            import glob, PIL.Image
            import uuid
            # L = [PIL.Image.open(f) for f in glob.glob(f'media/omrs/*.jpg')]
            L = [PIL.Image.open(f) for f in glob.glob(f'media/{omrs}/*.jpg')]
            a=uuid.uuid4().hex
            L[0].save(f'media/media/{a}_OMR.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=L[1:])

            
            from django.http import StreamingHttpResponse
            from django.conf import settings
            import os
            
            file_path=f'media/{a}_OMR.pdf'
            file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path)

        
            def file_iterator(file_path, chunk_size=8192):
                with open(str(file_path), 'rb') as pdf:
                    while True:
                        data = pdf.read(chunk_size)
                        if not data:
                            break
                        yield data          
                os.remove(file_path) 
            
            
            
            
            # import os

            # Global variable to track download status
            # is_downloading = False

            # def file_iterator(file_path, chunk_size=8192):
            #     is_downloading =False
                
            #     # Check if a download is already in progress
            #     if is_downloading:
            #         return None

            #     is_downloading = True

            #     try:
            #         with open(str(file_path), 'rb') as pdf:
            #             while True:
            #                 data = pdf.read(chunk_size)
            #                 if not data:
            #                     break
            #                 yield data
            #     finally:
            #         # Set the download flag to False after the download is complete or encountered an error
            #         is_downloading = False
            #         os.remove(file_path)
    
                

            # Use the StreamingHttpResponse class to serve the file as a stream
            response = StreamingHttpResponse(file_iterator(file_abs_path))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_abs_path)}"'
            response['Content-Type'] = 'application/pdf'   

        # deleteing the folder contents after been used
        import shutil    
        qr_only_folder_path = f"media/{qr_only}"
        omr_folder_path = f"media/{omrs}"
        shutil.rmtree(qr_only_folder_path)
        shutil.rmtree(omr_folder_path)
        return response
    
    except:
        return HttpResponse("Something went wrong")  
    


    
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
        
             
   
@login_required(login_url="/login")
def scan_download(request):
    return render(request,"scan_omr/download_generation.html")


    
@login_required(login_url="/login")
def search_scan_results(request, exam_center):
    # perform search based on exam_center an classes
    data = Qr.objects.filter(center_code=exam_center)
    
   
    # print(data)
    url = f"/omr_scan_dow/{exam_center}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"no_data_found.html")
        
    return render(request, 'scan_omr/search_scan_results.html',context)
   
    
    
    
################ U P L O A D   M U L T I P L E   I M A G E S  ########### 
  

import os
from django.conf import settings
from django.http import JsonResponse
import datetime
from .models import ExamScore
import uuid
from django.utils import timezone




import cv2
import glob
from django.shortcuts import render
from pyzbar.pyzbar import decode
from PIL import Image


data=[]
import threading





# Create a lock object
# processing_lock = threading.Lock()
@login_required(login_url="/login")
def upload_file(request, exam_center, classes, subject):
    if request.method == 'POST':
        files = request.FILES.getlist('images')

        if not files:
            return render(request, 'upload.html')

        folder_name = bulana()
        folder_path = os.path.join('media', folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file.name)

            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # Acquire the lock before processing
        # processing_lock.acquire()

        try:
            # P R O C E S S I N G
            path = f"media/{folder_name}/*.jpg"
            # path=f"media/{folder_name}/*.jpg"
            k = glob.glob(path)
            images = [cv2.imread(images) for images in glob.glob(path)]
            image_paths = glob.glob(path)
            images = []
            for image_path in image_paths:
                img = cv2.imread(image_path)
                images.append(img)

            # mar=[]
            
            fin = []
            c = 0
            for img in images:
                p = read_qr_and_scan.display_barcode(img)
                # print("pppppppp: ",p)
                # print(p[0][c])
                i = p[0][c] + f"\nscore: {p[-1]}"
                # i=p[0][c]
                fin.append(i)
                c += 1
            c = 0
            p[0].clear()
            # processing_lock.release()
            

            qr_result = []
            qr_result.clear()
            for item in fin:
                parts = item.split('\n')
                temp_dict = {}
                for part in parts:
                    key, value = part.split(': ')
                    temp_dict[key] = value

                # print(temp_dict)

                # temp_dict["score"] = score
                # print(temp_dict['score'])
                qr_result.append(temp_dict)
            # print(qr_result)
            
            
            for d in qr_result:
                d['Exam_ID'] = d.pop('Exam ID')
                d['Exam_name'] = d.pop('Exam name')
                d['Roll_no'] = d.pop('Roll No')
                # d['score'] = '90'
            # print(qr_result)

            # for i in qr_result:
            #     print(i)

            # for removing duplicates

            new_list = []
            for item in qr_result:
                if item not in new_list:
                    new_list.append(item)

            # print(new_list)
            data = new_list
            # print("data = ",data)

            for result_data in data:
                if not ExamScore.objects.filter(exam_id=int(result_data['Exam_ID']), roll_no=result_data['Roll_no'],
                                               section=result_data['Section'], name=result_data['Name']).exists():
                    result = ExamScore(
                        name=result_data['Name'],
                        classes=result_data['Class'],
                        section=result_data['Section'],
                        score=float(result_data['score']),
                        exam_id=int(result_data['Exam_ID']),
                        exam_name=result_data['Exam_name'],
                        roll_no=result_data['Roll_no']
                    )
                    result.save()

            context = {
                'qr_data': new_list,

                # 'score':mar,
                # 'variable2': 'value2',

            }

            fin.clear()

            # Calling the function for automatically saving to excel
            save_to_excel(data, 'file.xlsx')
            import shutil    
            temp_folder = f"media/{folder_name}"
            shutil.rmtree(temp_folder)
           
            
            

            return render(request, 'result_scan.html', context)
        except:
            return render(request,'upload.html')



    
# automatically saving to excel
import pandas as pd
def save_to_excel(data_list, file_path):
    df = pd.DataFrame(data_list)
    df.to_excel(file_path, index=False)






#EK EK KRKE DATA SAVE KRTA DATABASE MAI


# from django.shortcuts import render, redirect
# from .models import ExamScore

# def save_exam_score(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         # class = request.POST.get('class')
#         section = request.POST.get('section')
#         score = request.POST.get('score')
#         exam_id = request.POST.get('exam_id')
#         exam_name = request.POST.get('exam_name')
#         roll_no = request.POST.get('roll_no')

#         # Create a new ExamScore object and save it to the database
#         if not ExamScore.objects.filter(exam_id=exam_id, roll_no=roll_no,section=section,name=name).exists():
#         # if  ExamScore.objects.all().exists():
#             exam_score = ExamScore(
#                 name=name,
#                 # classes=classes,
#                 section=section,
#                 score=score,
#                 exam_id=exam_id,
#                 exam_name=exam_name,
#                 roll_no=roll_no
#             )
#             exam_score.save()

#             # Redirect to a success page
#             return HttpResponse("Success")
#             # return redirect('success')
#         else:            
#             return HttpResponse("Data Already Exists")
#     else:
#         # return render(request, 'error.html')
#         return HttpResponse("Something went wrong")




    








