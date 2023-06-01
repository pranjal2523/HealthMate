from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from payment.models import Appointment
from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import patient , doctor , diseaseinfo
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#For Payment
from sslcommerz_lib import SSLCOMMERZ 



SID = "abeds6401ce5c930e7",
KEY = "abeds6401ce5c930e7@ssl",

@login_required
def schedule(request, doctorusername):
        if request.method == "POST":
            patientusername = request.session['patientusername']
            puser = User.objects.get(username=patientusername)
            patient_obj = puser.patient

            #doctorusername = request.session['doctorusername']
            duser = User.objects.get(username=doctorusername)
            doctor_obj = duser.doctor
            request.session['doctorusername'] = doctorusername
            
            diseaseinfo_id = request.session['diseaseinfo_id']
            diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)
            #booking_date = date.today()
            patient_name_val = patient_obj.name
            doctor_name_val = doctor_obj.name
            status = "pending"
            appointment_new = Appointment( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj,status=status, patient_name=patient_name_val, doctor_name = doctor_name_val)
            appointment_new.save()

            request.session['appointment_id'] = appointment_new.id

            #print("consultation record is saved sucessfully.............................")
            
            #request.session['appointment_id'] = appoint_id
            #appointment_obj = Appointment.objects.get(id=appoint_id)
            
#            return render(request,'payment/appoint_page.html', {"appointment":appointment_obj})
            return redirect('payment:appointview',appointment_new.id)
        
@login_required
def  appointview(request,appoint_id):
    if request.method == 'GET':   
#      request.session['appointment_id'] = appoint_id
      appointment_obj = Appointment.objects.get(id=appoint_id)

      #print(appointment_obj)
      #print(date.today())
      return render(request,'payment/apoint_page.html', {"appoint":appointment_obj})

        
        
        
def update_appointview(request, appoint_id):    
    if request.method =="POST":
        appointment_obj = Appointment.objects.filter(id=appoint_id)
        seltime =  request.POST['seltime']
        seldate =  request.POST['seldate']
        booked_date = date.today()
        booked_date = booked_date.strftime("%Y-%m-%d")

        appointment_obj.update(booked_date= booked_date , appoint_date=seldate , appoint_time=seltime, status="confirm")            
        
        return redirect('payment:pay', appoint_id)
        


@login_required
def payment(request,appoint_id):

    cur_user = Appointment.objects.get(id=appoint_id)
    status_url = request.build_absolute_uri(reverse("payment:complete"))
    #print(status_url)
    settings = { 'store_id': SID, 'store_pass': KEY, 'issandbox': True }
    #cur_user = request.user
    sslcommez = SSLCOMMERZ(settings)
    print(sslcommez)
    #print(cur_user)
    post_body = {}
    post_body['total_amount'] = 300
    post_body['currency'] = "INR"
    post_body['tran_id'] = "comerce01"
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = cur_user.patient.name
    post_body['cus_email'] = cur_user.patient.user.email
    post_body['cus_phone'] = cur_user.patient.mobile_no
    post_body['cus_add1'] = "not required"
    post_body['cus_city'] = "not required"
    post_body['cus_country'] = "not required"
    post_body['shipping_method'] = "courier"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
    post_body['ship_name'] = "not required" 
    post_body['ship_add1'] = "not required" 
    post_body['ship_city'] = "not required" 
    post_body['ship_country'] = "not required"    
    post_body['ship_postcode'] = "not required"     

    response = sslcommez.createSession(post_body)
    
    #print(response)
    return redirect(response['redirectGatewayURL'])


@csrf_exempt
def complete(request):
    
#    patientusername = request.session['patientusername']
#    puser = User.objects.get(username=patientusername)
#    patient_obj = puser.patient.id
#    appoint = Appointment.objects.get(id= patient_obj)
#   print(appoint)

#    patientid = request.session['']
#   print(patientid)
    if request.method == 'POST' or request.method == "post":
        pay_data = request.POST
        status = pay_data['status']

        if status == 'VALID':
            #v_id = pay_data['val_id']
            #tran_id  = pay_data['bank_tran_id']             
            messages.success(request, "Your payment is successfull")
            return HttpResponseRedirect(reverse("payment:appoint"))
        elif status == 'FAILED':
            messages.success(request, "Your payment is Unsuccessfull")
    #return redirect("app_shop:home")
    return render(request, 'payment/complete.html')

def patappointview(request):
    if request.method == 'GET':

      if request.user.is_authenticated:
        #doc_obj = []
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        appoint_obj = Appointment.objects.filter(patient_id=puser.id)
        
        #print(appoint_obj[0])
        #for doc_val in appoint_obj:
        #    doc = doctor.objects.get(pk = doc_val.doctor_id)
        #    doc_obj.append(doc)
        #print(appoint_obj[0].doctor_id)
        #print(doc_obj[0].name)

        return render(request,'payment/appoint.html' , {"appoint":appoint_obj})

      else :
        return redirect('home')

#    if request.method == 'POST':
#
#       return render(request,'patient/patient_ui/profile.html')


def drappointview(request):
    if request.method == 'GET':

      if request.user.is_authenticated:
        #doc_obj = []
        doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        appoint_obj = Appointment.objects.filter(doctor_id=duser.id)
        
        #print(appoint_obj[0])
        #for doc_val in appoint_obj:
        #    doc = doctor.objects.get(pk = doc_val.doctor_id)
        #    doc_obj.append(doc)
        #print(appoint_obj[0].doctor_id)
        #print(doc_obj[0].name)

        return render(request,'payment/drappoint.html' , {"appoint":appoint_obj})

      else :
        return redirect('home')



    '''
    appointment = Appointment.objects.get_or_create(user=request.user)
    appointment = appointment[0]
    form = Appoint(instance=appointment)
    if request.method =='POST':
    form = Appoint(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            form = Appoint(instance=appointment)
            #messages.success(request, "Shipping Address Saved!")

#    order_qs = Order.objects.filter(user= request.user, ordered = False)
#    order_item = order_qs[0].orderitems.all()
#    order_total = order_qs[0].get_total()

# return render(request, 'payment/checkout.html', context={'form':form, 'total':order_total, 'order_items': order_item, 'appointment': appointment })






@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == "post":
        pay_data = request.POST
        status = pay_data['status']

        if status == 'VALID':
            v_id = pay_data['val_id']
            tran_id  = pay_data['bank_tran_id']             
            messages.success(request, "Your payment is successfull")
            return HttpResponseRedirect(reverse("payment:purchased", kwargs={'tran_id':tran_id,}))
        elif status == 'FAILED':
            messages.success(request, "Your payment is Unsuccessfull")
    #return redirect("app_shop:home")
    return render(request, 'payment/complete.html')


@login_required
def purchased(request, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderid = tran_id
    order.ordered = True
    order.orderid = orderid
    order.save()

    cart_item = cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()


    return HttpResponseRedirect(reverse("app_shop:home"))


@login_required
def order_view(request):
    try:
        order = Order.objects.filter(user=request.user, ordered= True)
        context = {"orders": order}
        if order[0].orderitems.count() == 0:
            raise Exception
    except:
        messages.warning(request, "You dont have any Order!")
        return redirect("app_shop:home")
    return render(request, "payment/order.html", context)


    '''