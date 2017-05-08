from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.user_home, name="user_home"),
    url(r'^athlete_list/$', views.AthleteListView.as_view(), name="athlete_list"),
    # url(r'^orderbuy_list/$', views.orderbuylist, name="order_list"),
    url(r'^ordersellbuy_list/$', views.ordersellbuylist, name="ordersellbuy_list"),
    url(r'^place_orderbuy/$', views.placeorderbuy, name="place_orderbuy"),
    url(r'^place_ordersell/$', views.placeordersell, name="place_ordersell"),
    url(r'^cancel_order/$', views.cancelorder, name="cancel_order"),
    url(r'^reactivate_order/$', views.reactivateorder, name="reactivate_order"),
]