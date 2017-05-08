from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User

from accounts.models import *
from . import models
from . import mixin
from . import forms

import datetime

# transaction id generator
def transac_gen():
    chars = ["-", " ", ":", "."]
    id_output = ""
    id_time = str(datetime.datetime.now())
    for char in chars:
        id_time = id_time.replace(char, "")
    return id_time



def send_lead(email, url):
    send_mail(
        'Lead from {}'.format(email),
        '{} submitted {}'.format(email, url),
        email,
        ['kenneth@teamtreehouse.com']
    )


def user_list(request):
    users = models.Paper.objects.all()
    output = ', '.join(str(user) for user in users)
    return HttpResponse(output)


class AthleteListView(generic.ListView):
    context_object_name = 'athletes'
    model = models.Paper

@login_required
def user_home(request):
    context1 = models.OrderBuy.objects.all()
    context2 = models.OrderSell.objects.all()
    context3 = models.PaperBank.objects.all()
    context = {context1, context2, context3}
    return render(request, "etrade/user_home.html", {'context': context})


# class OrderCreateView(generic.CreateView):
#     fields =
#     context_object_name = 'athletes'
#     model = models.Paper


# class TeamDetailView(DetailView):
#     model = models.Team


# class TeamCreateView(CreateView):
#     fields = 'get from model'
#     model = models.Team
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial["coach"] = self.request.user.pk
#         return initial

# class TeamUpdateView(UpdateView):
#     fields = 'get from model'
#     model = models.Team
#
# class TeamDeleteView(DeleteView):
#     model = models.Team
#     success_url = reverse_lazy("teams:list")
#
#     def get_queryset(self):
#         if not self.request.user.is_superuser:
#             return self.model.objects.filter(coach=self.request.user)
#         return self.model.objects.all()
#
# def orderbuylist(request):
#     context = models.OrderBuy.objects.filter(owner_id=request.user)
#     return render(request, 'etrade/order_list.html', {'context': context})

@login_required
def ordersellbuylist(request):
    context1 = models.OrderBuy.objects.all()
    context2 = models.OrderSell.objects.all()
    context3 = models.Paper.objects.all()
    context = {context1, context2, context3}
    return render(request, 'etrade/ordersellbuy_list.html', {'context': context})

#
# class PlaceOrderBuyView(generic.CreateView):
#     form_class = forms.PlaceOrderBuyForm
#     success_url = reverse_lazy("etrade:ordersellbuy_list")
#     template_name = "etrade/place_order.html"


# dna generator
def dna_gen(arg):
    chars = ["-", " ", ":", "."]
    id_time = str(arg.user.date_joined)
    for char in chars:
        id_time = id_time.replace(char, "")
    return id_time

@login_required
def placeorderbuy(request):
    form = forms.PlaceOrderBuyForm()
    if request.method == 'POST':
        form = forms.PlaceOrderBuyForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = request.user
            if (order.order_value * order.order_qty) <= user.userprofile.cash:
                user.userprofile.cash -= (order.order_value * order.order_qty)
                user.userprofile.save()
                paper = models.Paper.objects.get(paper_name=order.paper_name)
                order.paper_code = paper.paper_code
                order.owner_id = request.user
                order.order_id = 'buy'+ transac_gen()
                order.order_initial_qty = order.order_qty
                order.owner_dna = str(request.user) + dna_gen(request)
                order.sport = paper.sport
                order.status = "OPEN"
                order.save()
                return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))
            else:
                messages.add_message(request, messages.ERROR,
                                     'You do not have enough credit for this order...')
    return render(request, "etrade/place_order.html", {'form': form})

@login_required
def placeordersell(request):
    form = forms.PlaceOrderSellForm()
    if request.method == 'POST':
        form = forms.PlaceOrderSellForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            try:
                paper_bank = models.PaperBank.objects.get(owner_id=request.user, paper_name=order.paper_name)
                paper = models.Paper.objects.get(paper_name=order.paper_name)
                if order.order_qty <= paper_bank.paper_qty:
                    print(paper.paper_code)
                    order.paper_code = paper.paper_code
                    order.owner_id = request.user
                    order.order_id = 'sell'+ transac_gen()
                    order.order_initial_qty = order.order_qty
                    order.owner_dna = str(request.user) + dna_gen(request)
                    order.sport = paper.sport
                    order.status = "OPEN"
                    paper_bank.paper_qty -= order.order_qty
                    order.save()
                    paper_bank.save()
                    return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))
                else:
                    messages.add_message(request, messages.ERROR,
                                         'You do not have enough shares for this athlete...')
            except:
                messages.add_message(request, messages.ERROR,
                                     'You do not have any shares for this athlete...')
    return render(request, "etrade/place_order.html", {'form': form})

@login_required
def cancelorder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print(order_id)
        if 'buy' in order_id:
            buy = models.OrderBuy.objects.get(order_id=order_id)
            # paper_bank = models.PaperBank.objects.get(owner_id=request.user, paper_name=buy.paper_name)
            buy.status = "CANCELLED"
            user = request.user
            user.userprofile.cash += (buy.order_value * buy.order_qty)
            user.userprofile.save()
            buy.save()
            return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))
        elif 'sell' in order_id:
            sell = models.OrderSell.objects.get(order_id=order_id)
            paper_bank = models.PaperBank.objects.get(owner_id=request.user, paper_name=sell.paper_name)
            sell.status = "CANCELLED"
            paper_bank.paper_qty += sell.order_qty
            sell.save()
            paper_bank.save()
            return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))

@login_required
def reactivateorder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print(order_id)
        if 'buy' in order_id:
            buy = models.OrderBuy.objects.get(order_id=order_id)
            paper_bank = models.PaperBank.objects.get(owner_id=request.user, paper_name=buy.paper_name)
            buy.status = "OPEN"
            user = request.user
            user.userprofile.cash += (buy.order_value * buy.order_qty)
            user.userprofile.save()
            buy.save()
            return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))
        elif 'sell' in order_id:
            sell = models.OrderSell.objects.get(order_id=order_id)
            paper_bank = models.PaperBank.objects.get(owner_id=request.user, paper_name=sell.paper_name)
            sell.status = "OPEN"
            paper_bank.paper_qty += sell.order_qty
            sell.save()
            paper_bank.save()
            return HttpResponseRedirect(reverse('etrade:ordersellbuy_list'))