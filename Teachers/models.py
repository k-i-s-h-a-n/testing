from django.db import models

# Create your models here.

# class user(models.Model):
#     username = models.CharField(max_length=500)
#     password = models.CharField(max_length=200)   

#     def __str__(self):
#         return self.username
    



class Image(models.Model):
    title = models.CharField(max_length=200)
    # description = models.TextField()
    image = models.ImageField(upload_to="images/")

  
    def __str__(self):  
        return self.title  



# Qr code details
class Qr(models.Model):
    Exam_name=models.CharField(max_length=500)
    Exam_id=models.CharField(max_length=500)
    Name=models.CharField(max_length=500)
    Roll_no=models.CharField(max_length=500)
    classes=models.CharField(max_length=500)
    section=models.CharField(max_length=500)
    center_code=models.CharField(max_length=500)
    subject=models.CharField(max_length=500,default = "")

    
    
    


class ExamScore(models.Model):
    name = models.CharField(max_length=255)
    classes = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    exam_id = models.IntegerField()
    exam_name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=10)
    
