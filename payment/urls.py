from django.urls import path
from payment import views

app_name = "payment"

urlpatterns=[
    path('schedule_appointment/<str:doctorusername>', views.schedule, name="schedule"),
    path('appoint_view/<int:appoint_id>', views.appointview, name="appointview"),
    path('update_appoint_view/<int:appoint_id>', views.update_appointview, name="updateappointview"),
    path('pay/<int:appoint_id>', views.payment, name="pay"),
    path('complete/', views.complete, name="complete"),
    path('appointment/', views.patappointview, name="appoint"),
    path('appointments/', views.drappointview, name="drappoint"),
    #path('purchased/<tran_id>/', views.purchased, name="purchased"), 

#    path('checkout/', views.checkout, name="checkout"), 
    #path('orders/', views.order_view, name="orders"), 
]