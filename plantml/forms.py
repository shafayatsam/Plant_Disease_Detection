from django import forms

class UploadForm(forms.Form):
    uploaded_file = forms.FileField(label='')



class MessageForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Name'}))
    email = forms.EmailField(label='', max_length=100, 
                            widget= forms.EmailInput(attrs={'placeholder':'Email'}))
    phone = forms.CharField(label='', max_length=14,widget=forms.TextInput(attrs={'placeholder':'Phone'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write your Message', 'rows':4}), 
                            label='')

class SubscribeForm(forms.Form):
    email = forms.EmailField(label='', max_length=100, 
                            widget= forms.EmailInput(attrs={'placeholder':'Your Email'}))

class SearchForm(forms.Form):
    keyWord = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'placeholder':'Search here'}))