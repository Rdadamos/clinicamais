from django.shortcuts import get_object_or_404, render, redirect
from .models import Attendant, Doctor, DoctorSchedule
from .forms import DoctorScheduleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime as datetime

@login_required(login_url='/')
def index(request):
    latest_question_list = Attendant.objects.order_by('name')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'appointments/index.html', context)

@login_required(login_url='/')
def doctor_schedule(request, id):
    schedule_forms = {}
    count = 0
    schedule = DoctorSchedule.objects.filter(doctor=id).order_by('hour', 'day')
    doctor = get_object_or_404(Doctor, id=id)
    formInvalid = False
    for hour in range(8, 18):
        position = str(datetime.time(hour).strftime("%H:%M"))
        schedule_forms[position] = []
        for day in range(1, 7):
            if request.method == 'POST':
                schedule_forms[position].append(DoctorScheduleForm(request.POST, instance=schedule[count], auto_id=False, prefix=str(hour)+"-"+str(day)))
                if schedule_forms[position][day-1].is_valid():
                    schedule_forms[position][day-1].save()
                else:
                    formInvalid = True
            else:
                schedule_forms[position].append(
                DoctorScheduleForm(instance=schedule[count], auto_id=False, prefix=str(hour)+"-"+str(day),
                    initial={
                        'day': day,
                        'hour': datetime.time(hour),
                        'doctor': doctor.id
                }))
            count += 1
    if request.method == 'POST':
        if formInvalid:
            messages.error(request, 'Verifique os erros abaixo')
            return render(request, 'appointments/doctor_schedule.html', { 'schedule_forms': schedule_forms, 'doctor': doctor })
        messages.success(request, 'Agenda de ' + doctor.name + ' salva com sucesso')
        return redirect('all_doctor')
    return render(request, 'appointments/doctor_schedule.html', { 'schedule_forms': schedule_forms, 'doctor': doctor })
