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
    schedule_forms = {}
    for hour in range(8, 18):
        schedule_forms[str(datetime.time(hour).strftime("%H:%M"))] = []
        for day in range(1, 7):
            schedule_forms[str(datetime.time(hour).strftime("%H:%M"))].append(
            DoctorScheduleForm(auto_id=False, initial={
                'day': day,
                'hour': datetime.time(hour),
                'doctor': doctor.id
            }))
    return render(request, 'appointments/doctor_schedule.html', { 'schedule_forms': schedule_forms, 'doctor': doctor })
