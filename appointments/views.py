from django.shortcuts import get_object_or_404, render
from .models import Attendant, Doctor
from .forms import DoctorScheduleForm
from django.contrib.auth.decorators import login_required
import datetime as datetime

@login_required(login_url='/')
def index(request):
    latest_question_list = Attendant.objects.order_by('name')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'appointments/index.html', context)

@login_required(login_url='/')
def doctor_schedule(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor_schedule_form = []
    for x in range(1, 7):
        for y in range(8, 18):
            doctor_schedule_form.append(DoctorScheduleForm(auto_id=False, initial={'day': x, 'hour': datetime.time(y), 'doctor': doctor.id}))
    return render(request, 'appointments/doctor_schedule.html', {'doctor_schedule_form': doctor_schedule_form, 'doctor': doctor })
