from django import forms
from .models import Product, UploadedImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=255, required=True)
#     description = forms.CharField(widget=forms.Textarea, required=True)
#     category = forms.CharField(max_length=255, required=True)
#     price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
#     image = forms.ImageField(required=True)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ProductName', 'Description', 'Category', 'Price', 'image']