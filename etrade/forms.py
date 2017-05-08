from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django import forms

from . import models


class PlaceOrderBuyForm(forms.ModelForm):
    class Meta:
        model = models.OrderBuy
        fields = [
            'paper_name',
            'order_qty',
            'order_value',
            ]


class PlaceOrderSellForm(forms.ModelForm):
    class Meta:
        model = models.OrderSell
        fields = [
            'paper_name',
            'order_qty',
            'order_value'
        ]

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = models.OrderSell
        fields = [
           ]


class PersonalForm(forms.ModelForm):
    class Meta:
        model = models.OrderSell
        fields = [
           ]