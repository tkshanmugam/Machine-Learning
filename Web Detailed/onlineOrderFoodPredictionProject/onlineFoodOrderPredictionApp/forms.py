from django import forms
from .models import *


class onlineFoodPreForm(forms.ModelForm):
    class Meta():
        model=onlineFoodPreModel
        fields=['Age','Gender','Marital_Status','Monthly_Income','Educational_Qualification','Family_Size', 'Feedback']
