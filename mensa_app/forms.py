from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'picture']

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])