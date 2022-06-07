from random import choice, choices
from django import forms

ORDER_TYPES = [
    ('Buy','Buy'),
    ('Sell','Sell')
]
class OrderForm(forms.Form):
    orderType = forms.ChoiceField(choices=ORDER_TYPES)
    quantity = forms.IntegerField(min_value=0)
