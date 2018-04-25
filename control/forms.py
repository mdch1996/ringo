from django import forms


class SwitchForm(forms.Form):
    switch = forms.IntegerField()
