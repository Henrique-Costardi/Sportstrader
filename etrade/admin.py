from django.contrib import admin

# Register your models here.

from .models import Paper,PaperBank, OrderBuy, OrderExecuted, OrderSell

admin.site.register(Paper)
admin.site.register(PaperBank)
admin.site.register(OrderSell)
admin.site.register(OrderBuy)
admin.site.register(OrderExecuted)

