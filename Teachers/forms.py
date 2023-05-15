from django import forms
from .models import Image
from PIL import Image as PIL_Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = (
            "title",
            "image",
        )

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            img = PIL_Image.open(image)
            if img.format not in ["JPEG", "PNG", "JPG"]:
                raise forms.ValidationError("Unsupported image format")
        return image




from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    password2=forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}