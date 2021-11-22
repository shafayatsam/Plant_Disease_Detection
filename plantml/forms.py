from django import forms

class UploadForm(forms.Form):
    uploaded_file = forms.FileField(label='' )
    