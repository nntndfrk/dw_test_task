from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.index), name='index'),
    url(r'^get_main_data/$', login_required(views.main_data), name='main_data'),
    url(r'^get_prod_data/$', login_required(views.products_data), name='products_data'),
]