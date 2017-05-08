from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Paper(models.Model):
    """A base model that will use our database"""
    paper_code = models.CharField(max_length=255, unique=True)
    paper_name = models.CharField(max_length=255, unique=True)
    paper_value = models.FloatField(default=1.00)
    paper_initial_qty = models.IntegerField(default=10000)
    paper_current_qty = models.IntegerField(default=10000)
    paper_highest_value = models.FloatField(default=1.00)
    paper_lowest_value = models.FloatField(default=1.00)
    paper_reference_value = models.FloatField(default=1.00)
    paper_variation = models.FloatField(default=1.00)
    sport = models.CharField(max_length=255, unique=False, default="")
    last_transaction = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paper_name

    def get_absolute_url(self):
        return reverse("etrade:detail", kwargs={pk: self.pk})


class PaperBank(models.Model):
    """A base model to store all shares of papers"""
    db_type = models.CharField(max_length=255, unique=False, default="BANK")
    owner_id = models.CharField(max_length=255, unique=False, default="")
    owner_dna = models.CharField(max_length=255, unique=False)
    paper_name = models.CharField(max_length=255, unique=False, default="")
    paper_code = models.CharField(max_length=255, unique=False, default="")
    paper_value = models.CharField(max_length=255, default=1.00)
    paper_qty = models.IntegerField(default=10000)
    sport = models.CharField(max_length=255, unique=False, default="")

    def __str__(self):
        return self.owner_id


class OrderBuy(models.Model):
    """A base model that will use our database"""
    order_id = models.CharField(max_length=255, unique=True)
    owner_id = models.CharField(max_length=255,  unique=False)
    owner_dna = models.CharField(max_length=255, unique=False)
    paper_name = models.ForeignKey(Paper)
    paper_code = models.CharField(max_length=255, unique=False, default="")
    order_value = models.FloatField(default=1.00)
    order_initial_qty = models.IntegerField(default=10000)
    order_qty = models.IntegerField(default=10000)
    status = models.CharField(max_length=255, default="")
    sport = models.CharField(max_length=255, unique=False, default="")


    def __str__(self):
        return self.order_id


class OrderSell(models.Model):
    """A base model that will use our database"""
    order_id = models.CharField(max_length=255, unique=True)
    owner_id = models.CharField(max_length=255, unique=False, default="")
    owner_dna = models.CharField(max_length=255, unique=False)
    paper_name = models.ForeignKey(Paper, default="")
    paper_code = models.CharField(max_length=255, unique=False, default="")
    order_value = models.FloatField(default=1.00)
    order_initial_qty = models.IntegerField(default=10000)
    order_qty = models.IntegerField(default=10000)
    status = models.CharField(max_length=255, default="")
    sport = models.CharField(max_length=255, unique=False, default="")


    def __str__(self):
        return self.order_id


class OrderExecuted(models.Model):
    """A base model that will use our database"""
    order_id = models.CharField(max_length=255, unique=True, default="")
    buyer_id = models.CharField(max_length=255, unique=False)
    buyer_dna = models.CharField(max_length=255, unique=False)
    seller_id = models.CharField(max_length=255, unique=False)
    seller_dna = models.CharField(max_length=255, unique=False)
    paper_name = models.CharField(max_length=255, unique=False)
    paper_code = models.CharField(max_length=255, unique=False, default="")
    order_value = models.FloatField(default=1.00)
    executed_qty = models.IntegerField(default=10000)
    buy_id = models.CharField(max_length=255, unique=False, default="")
    sell_id = models.CharField(max_length=255, unique=False, default="")
    sport = models.CharField(max_length=255, unique=False, default="")


    def __str__(self):
        return self.order_id
