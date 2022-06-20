from django.urls import path

from .views import StuffList, RentalList, StuffDetailView, RentalDetailView, StuffCreateView, \
    MyRentalListView, MyStuffListView, index, categories_posts

app_name = 'bilyeo'

urlpatterns = [
    path('', index, name='index'),
    path('stuff_list/', StuffList.as_view(), name='stuff_list'),
    path('stuff/create/', StuffCreateView.as_view(), name='stuff_create'),
    path('stuff/<int:pk>/', StuffDetailView.as_view(), name='stuff_detail'),
    path('stuff/category/<str:slug>/', categories_posts, name='category_list'),
    path('rental/<int:pk>/', RentalDetailView.as_view(), name='rental_detail'),
    path('rental_list/', RentalList.as_view(), name='rental_list'),
    path('my_rental_list/', MyRentalListView.as_view(), name='my_rental_list'),
    path('my_stuff_list/', MyStuffListView.as_view(), name='my_stuff_list'),
]
