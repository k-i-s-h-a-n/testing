from django.contrib import admin
from Teachers.models import *

# Register your models here.

# @admin.register(user)
# class StudentAdmin(admin.ModelAdmin):
#     list_display=['id','username']

admin.site.register(Image)




@admin.register(Qr)
class StudentAdmin(admin.ModelAdmin):
    list_display=['id','center_code','Exam_name','Exam_id',"Name","Roll_no","classes","section","subject"]


    

@admin.register(ExamScore)
class StudentAdmin(admin.ModelAdmin):
    list_display=['id','exam_name','exam_id',"name","roll_no","classes","section","score"]