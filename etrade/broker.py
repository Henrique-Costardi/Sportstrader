import datetime
import time

#from background_task import background
from django.contrib.auth.models import User

from etrade.models import *
from accounts.models import *




# dna generator
def dna_gen(arg):
    dna_output = ""
    for letter in arg:
        dna_output += str(ord(letter))
    return dna_output


# transaction id generator
def transac_gen():
    import datetime
    chars = ["-", " ", ":", "."]
    id_output = ""
    id_time = str(datetime.datetime.now())
    for char in chars:
        id_time = id_time.replace(char, "")
    return id_time





# execute orders (Background task)
# @background(schedule=5)
def execute_orders():
    import datetime
    import time
    from django.contrib.auth.models import User
    from etrade.models import Paper, PaperBank, OrderBuy, OrderExecuted, OrderSell
    from accounts.models import UserProfile

    def transac_gen():
        import datetime
        chars = ["-", " ", ":", "."]
        id_output = ""
        id_time = str(datetime.datetime.now())
        for char in chars:
            id_time = id_time.replace(char, "")
        return id_time

    def dna_gen(arg):
        dna_output = ""
        for letter in arg:
            dna_output += str(ord(letter))
        return dna_output

    while True:
        time.sleep(10)
        print('running at timestamp --> '+ str(datetime.datetime.now()))
        sell = OrderSell.objects.filter(status='OPEN') | OrderSell.objects.filter(status='PARTIAL')
        sell = sell.order_by('order_value')
        buy = OrderBuy.objects.filter(status='OPEN') | OrderBuy.objects.filter(status='PARTIAL')
        buy = buy.order_by('order_value')
        bank = PaperBank.objects.all()
        paper_ref = Paper.objects.all()
        executed = OrderExecuted.objects.all()
        for order in buy:
            """INITIAL PAPER CHECK"""
            paper = paper_ref.get(paper_code=order.paper_code)
            if paper.paper_current_qty > 0 and order.order_value >= paper.paper_value:
                if paper.paper_current_qty >= order.order_qty:
                    paper.paper_current_qty = paper.paper_current_qty - order.order_qty
                    if paper.paper_highest_value < order.order_value:
                        paper.paper_highest_value = order.order_value
                    if paper.paper_lowest_value > order.order_value:
                        paper.paper_lowest_value = order.order_value
                    # paper.paper_variation = ((order.order_value / paper.paper_reference_value) - 1.0) * 100
                    paper.save()
                    executed.create(buyer_id=order.owner_id,
                                    buyer_dna=order.owner_dna,
                                    seller_id=paper.paper_name,
                                    seller_dna=paper.paper_name,
                                    paper_name=order.paper_name,
                                    paper_code=order.paper_code,
                                    order_value=order.order_value,
                                    executed_qty=order.order_qty,
                                    buy_id=order.order_id,
                                    sport=order.sport,
                                    order_id="exec"+transac_gen())
                    try:
                        bank = PaperBank.objects.all()
                        update_bank = bank.get(owner_id = order.owner_id, paper_name = order.paper_name)
                        update_bank.paper_qty += order.order_qty
                        update_bank.paper_value = order.order_value
                        update_bank.save()
                        order.status = 'COMPLETE'
                        order.order_qty = 0
                        order.save()
                    except:
                        PaperBank.objects.create(owner_id=order.owner_id,
                                         owner_dna=order.owner_dna,
                                         paper_name=order.paper_name,
                                         paper_code=order.paper_code,
                                         paper_value=order.order_value,
                                         paper_qty = order.order_qty,
                                         sport = paper.sport)
                        order.status = 'COMPLETE'
                        order.order_qty = 0
                        order.save()
                elif paper.paper_current_qty < order.order_qty:
                    order_result = order.order_qty - paper.paper_current_qty
                    paper.paper_current_qty = 0
                    if paper.paper_highest_value < order.order_value:
                        paper.paper_highest_value = order.order_value
                    if paper.paper_lowest_value > order.order_value:
                        paper.paper_lowest_value = order.order_value
                    # paper.paper_variation = ((order.order_value / paper.paper_reference_value) - 1.0) * 100
                    paper.save()
                    executed.create(buyer_id=order.owner_id,
                                    buyer_dna=order.owner_dna,
                                    seller_id=paper.paper_name,
                                    seller_dna=paper.paper_name,
                                    paper_name=order.paper_name,
                                    paper_code=order.paper_code,
                                    order_value=order.order_value,
                                    executed_qty=order.order_qty-order_result,
                                    buy_id=order.order_id,
                                    sport=order.sport,
                                    order_id="exec" + transac_gen())
                    try:
                        bank = PaperBank.objects.all()
                        update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                        update_bank.paper_qty += order.order_qty-order_result
                        update_bank.paper_value = order.order_value
                        update_bank.save()
                        order.order_qty = order_result
                        order.status = "PARTIAL"
                        order.save()
                    except:
                        PaperBank.objects.create(owner_id=order.owner_id,
                                                 owner_dna=order.owner_dna,
                                                 paper_name=order.paper_name,
                                                 paper_code=order.paper_code,
                                                 paper_value=order.order_value,
                                                 paper_qty=order.order_qty-order_result,
                                                 sport=paper.sport)
                        order.order_qty = order_result
                        order.status = "PARTIAL"
                        order.save()
            else:
                for sale in sell:
                    if sale.paper_name==order.paper_name and sale.order_value <= order.order_value:
                        if sale.order_qty > order.order_qty:
                            sale.order_qty = sale.order_qty - order.order_qty
                            if paper.paper_highest_value < order.order_value:
                                paper.paper_highest_value = order.order_value
                            elif paper.paper_lowest_value > order.order_value:
                                paper.paper_lowest_value = order.order_value
                            paper.paper_value = order.order_value
                            paper.paper_variation = ((order.order_value / paper.paper_reference_value) - 1.0) * 100
                            paper.save()
                            executed.create(buyer_id=order.owner_id,
                                            buyer_dna=order.owner_dna,
                                            seller_id=sale.owner_id,
                                            seller_dna=sale.owner_dna,
                                            paper_name=order.paper_name,
                                            paper_code=order.paper_code,
                                            order_value=order.order_value,
                                            executed_qty=order.order_qty,
                                            buy_id=order.order_id,
                                            sport=order.sport,
                                            order_id="exec" + transac_gen())
                            user = User.objects.get(username=sale.owner_id)
                            user.userprofile.cash += (order.order_value * order.order_qty)
                            user.userprofile.save()
                            sale.status = 'PARTIAL'
                            sale.save()
                            try:
                                bank = PaperBank.objects.all()
                                update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                                update_bank.paper_qty += order.order_qty
                                update_bank.paper_value = order.order_value
                                update_bank.save()
                                order.status = 'COMPLETE'
                                order.order_qty = 0
                                order.save()
                            except:
                                PaperBank.objects.create(owner_id=order.owner_id,
                                                         owner_dna=order.owner_dna,
                                                         paper_name=order.paper_name,
                                                         paper_code=order.paper_code,
                                                         paper_value=order.order_value,
                                                         paper_qty=order.order_qty,
                                                         sport=paper.sport)
                                order.status = 'COMPLETE'
                                order.order_qty = 0
                                order.save()
                        elif sale.order_qty <= order.order_qty:
                            order_result = order.order_qty - sale.order_qty
                            sale.order_qty = 0
                            if paper.paper_highest_value < order.order_value:
                                paper.paper_highest_value = order.order_value
                            if paper.paper_lowest_value > order.order_value:
                                paper.paper_lowest_value = order.order_value
                            paper.paper_value = order.order_value
                            paper.paper_variation = ((order.order_value / paper.paper_reference_value) - 1.0)*100
                            paper.save()
                            executed.create(buyer_id=order.owner_id,
                                            buyer_dna=order.owner_dna,
                                            seller_id=sale.owner_id,
                                            seller_dna=sale.owner_dna,
                                            paper_name=order.paper_name,
                                            paper_code=order.paper_code,
                                            order_value=order.order_value,
                                            executed_qty=order.order_qty-order_result,
                                            buy_id=order.order_id,
                                            sport=order.sport,
                                            order_id="exec" + transac_gen())
                            user = User.objects.get(username=sale.owner_id)
                            user.userprofile.cash += (order.order_value * (order.order_qty-order_result))
                            user.userprofile.save()
                            sale.status = 'COMPLETE'
                            sale.save()
                            try:
                                bank = PaperBank.objects.all()
                                update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                                update_bank.paper_qty += order.order_qty-order_result
                                update_bank.paper_value = order.order_value
                                update_bank.save()
                                order.order_qty = order_result
                            except:
                                PaperBank.objects.create(owner_id=order.owner_id,
                                                         owner_dna=order.owner_dna,
                                                         paper_name=order.paper_name,
                                                         paper_code=order.paper_code,
                                                         paper_value=order.order_value,
                                                         paper_qty=order.order_qty - order_result,
                                                         sport=paper.sport)
                                order.order_qty = order_result
                            if order_result == 0:
                                order.status = 'COMPLETE'
                                order.save()
                            else:
                                order.status = 'PARTIAL'
                                order.save()


execute_orders()