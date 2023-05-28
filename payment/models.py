from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from main_app.models import patient , doctor , diseaseinfo


# Create your views here.

class Appointment(models.Model):
    patient_name = models.CharField(max_length=20, null=True, blank=True)
    doctor_name = models.CharField(max_length=20, null=True, blank=True)
    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    diseaseinfo = models.OneToOneField(diseaseinfo, null=True, on_delete=models.SET_NULL, unique=False)
    booked_date = models.DateField(null=True, blank=True)
    appoint_date = models.DateField(null=True, blank=True)
    appoint_time = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length = 20)
    

    def __str__(self) -> str:
        return f'{self.patient.user.username} Appiontment'

    def is_fully_filled(self):
        fields = [f.name for f in self._meta.get_fields()]

        for field in fields:
            value = getattr(self, field)
            if value is None or value =="":
                return False
        return True
    
    class Meta:
        verbose_name_plural = "Appointment"