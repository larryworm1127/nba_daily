"""Main App Forms Module

@date: 06/16/2019
@author: Larry Shi
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Game


class DateForm(forms.Form):
    """Form for selecting date on <scores> page.
    """
    date = forms.DateField(
        label='Date',
        input_formats=['%m-%d-%Y'],
    )

    # def clean_date(self):
    #     """Determine whether the selected date is valid or not.
    #     """
    #     data = self.cleaned_data['date']
    #
    #     # Check if there is a game on the selected date
    #     if Game.objects.filter(game_date__contains=str(data)).count() == 0:
    #         raise ValidationError(_('No games on selected date.'))
    #
    #     return data
