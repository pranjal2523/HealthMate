from django.forms import ModelForm
from .models import Appointment

class Appoint(ModelForm):
    class Meta:
        model = Appointment
        fields = ('user','appoint_date', 'doctor_name', 'Time_slot','bookinf_time',)