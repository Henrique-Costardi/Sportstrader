from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from etrade import models


def index(request):
    context1 = models.Paper.objects.all().order_by('-last_transaction')[:12]
    # context2 = models.OrderSell.objects.all()
    # context3 = models.PaperBank.objects.all()
    context = {context1}
    return render(request, 'index.html', {'context': context1})

