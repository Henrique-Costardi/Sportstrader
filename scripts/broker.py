import datetime
import time
from etrade.models import *


# dna generator
def dna_gen(arg):
    dna_output = ""
    for letter in arg:
        dna_output += str(ord(letter))
    return dna_output

# transaction id generator
def transac_gen():
    chars = ["-", " ", ":", "."]
    id_output = ""
    id_time = str(datetime.datetime.now())
    for char in chars:
        id_time = id_time.replace(char, "")
    return id_time


# execute orders (Background task)
def execute_orders():
    while True:
        # time.sleep(10)
        # print('running')
        sell = OrderSell.objects.all().order_by('order_value')
        buy = OrderBuy.objects.all().order_by('-order_value')
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
                    paper.paper_value = order.order_value
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
                        update_bank = bank.get(owner_id = order.owner_id, paper_name = order.paper_name)
                        update_bank.paper_qty += order.order_qty
                        update_bank.paper_value = order.order_value
                        update_bank.save()
                        order.delete()
                    except:
                        PaperBank.objects.create(owner_id=order.owner_id,
                                         owner_dna=order.owner_dna,
                                         paper_name=order.paper_name,
                                         paper_value=order.order_value,
                                         paper_qty = order.order_qty,
                                         sport = paper.sport)
                        order.delete()
                elif paper.paper_current_qty < order.order_qty:
                    order_result = order.order_qty - paper.paper_current_qty
                    paper.paper_current_qty = 0
                    if paper.paper_highest_value < order.order_value:
                        paper.paper_highest_value = order.order_value
                    if paper.paper_lowest_value > order.order_value:
                        paper.paper_lowest_value = order.order_value
                    paper.paper_value = order.order_value
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
                    order.order_qty=order_result
                    order.save()
                    try:
                        update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                        update_bank.paper_qty += order.order_qty-order_result
                        update_bank.paper_value = order.order_value
                        update_bank.save()
                    except:
                        PaperBank.objects.create(owner_id=order.owner_id,
                                                 owner_dna=order.owner_dna,
                                                 paper_name=order.paper_name,
                                                 paper_value=order.order_value,
                                                 paper_qty=order.order_qty-order_result,
                                                 sport=paper.sport)
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
                            sale.save()
                            try:
                                update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                                update_bank.paper_qty += order.order_qty
                                update_bank.paper_value = order.order_value
                                update_bank.save()
                                order.delete()
                            except:
                                PaperBank.objects.create(owner_id=order.owner_id,
                                                         owner_dna=order.owner_dna,
                                                         paper_name=order.paper_name,
                                                         paper_value=order.order_value,
                                                         paper_qty=order.order_qty,
                                                         sport=paper.sport)
                                order.delete()
                        elif sale.order_qty <= order.order_qty:
                            order_result = order.order_qty - sale.order_qty
                            sale.order_qty = 0
                            if paper.paper_highest_value < order.order_value:
                                paper.paper_highest_value = order.order_value
                            if paper.paper_lowest_value > order.order_value:
                                paper.paper_lowest_value = order.order_value
                            paper.paper_value = order.order_value
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
                            sale.delete()
                            order.order_qty = order_result
                            try:
                                update_bank = bank.get(owner_id=order.owner_id, paper_name=order.paper_name)
                                update_bank.paper_qty += order.order_qty-order_result
                                update_bank.paper_value = order.order_value
                                update_bank.save()
                            except:
                                PaperBank.objects.create(owner_id=order.owner_id,
                                                         owner_dna=order.owner_dna,
                                                         paper_name=order.paper_name,
                                                         paper_value=order.order_value,
                                                         paper_qty=order_result - order.order_qty,
                                                         sport=paper.sport)
                            if order_result == 0:
                                order.delete()
                            else:
                                order.save()




if __name__ == '__main__':
    execute_orders()