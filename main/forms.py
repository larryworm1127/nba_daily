"""Main App Forms Module

@date: 06/16/2019
@author: Larry Shi
"""
from django import forms


class DateForm(forms.Form):

    date = forms.DateField(
        label='Date',
        input_formats=['%m-%d-%Y'],
    )
