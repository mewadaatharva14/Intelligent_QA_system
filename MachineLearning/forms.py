from django import forms

class InputForm(forms.Form):
    question = forms.CharField(max_length=100)
    pdf_reader = forms.FileField()
    
