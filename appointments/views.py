from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Appointment, Attendant, Doctor, DoctorSchedule
from .forms import AppointmentForm, DoctorScheduleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime as datetime
from datetime import timedelta, date
from django.utils.translation import gettext

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
        for day in range(0, 6):
            if request.method == 'POST':
                schedule_forms[position].append(DoctorScheduleForm(request.POST, instance=schedule[count], auto_id=False, prefix=str(hour)+"-"+str(day)))
                if schedule_forms[position][day].is_valid():
                    schedule_forms[position][day].save()
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

@login_required(login_url='/')
def appointments(request, id_patient):
    try:
        appointments = get_list_or_404(Appointment)
        return render(request, 'appointments/appointments.html', { 'appointments': appointments })
    except:
        return redirect('new_appointment_doctor', id_patient=id_patient)

@login_required(login_url='/')
def new_appointment_doctor(request, id_patient):
    try:
        doctors = get_list_or_404(Doctor)
        return render(request, 'appointments/new_appointment_doctor.html', { 'doctors': doctors, 'id_patient': id_patient })
    except:
        return redirect('new_doctor')

@login_required(login_url='/')
def new_appointment(request, id_patient, id_doctor):
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            print(appointment_form.cleaned_data['date'])
            messages.success(request, 'Novo Consulta criada com sucesso')
            return redirect('all_patient')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        appointments = Appointment.objects.filter(doctor=id_doctor).order_by('date')
        schedules = DoctorSchedule.objects.filter(doctor=id_doctor, available=True).order_by('hour', 'day')
        appointment_forms = {}
        start_date = datetime.date.today() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=7)
        daynames = []
        for single_date in daterange(start_date, end_date):
            daynames.append(gettext(single_date.strftime("%A")) + single_date.strftime(", %d/%m"))
        for hour in range(8, 18):
            position = str(datetime.time(hour).strftime("%H:%M"))
            appointment_forms[position] = []
            available_hour = schedules.filter(hour=datetime.time(hour))
            for single_date in daterange(start_date, end_date):
                weekday = single_date.weekday()
                available = available_hour.filter(day=weekday)
                if available:
                    appointment_forms[position].append(AppointmentForm(initial={
                        'date': str(single_date) + ' ' + position,
                        'doctor': id_doctor,
                        'patient': id_patient,
                        'attendant': available
                    }))
                else:
                    appointment_forms[position].append('noform')
    return render(request, 'appointments/new_appointment.html', { 'appointment_forms': appointment_forms, 'daynames': daynames })

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
