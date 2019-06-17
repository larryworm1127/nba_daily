from django import forms


class DateForm(forms.Form):

    date = forms.DateField(
        label='Date',
        input_formats=['%m-%d-%Y'],
    )
