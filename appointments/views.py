from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Appointment, Doctor, DoctorSchedule
from .forms import AppointmentForm, AppointmentInProgressForm, AppointmentExamForm, AppointmentMedicineForm, DoctorScheduleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime as datetime
from datetime import timedelta, date
from django.utils.translation import gettext

@login_required(login_url='/')
def index(request):
    try:
        doctor = request.user.doctor.id
        appointments = Appointment.objects.filter(doctor=doctor, date__gte=datetime.date.today()).order_by('date')
    except:
        appointments = Appointment.objects.filter(date__gte=datetime.date.today()).order_by('date')
    return render(request, 'appointments/index.html', { 'appointments': appointments })

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
    messages.info(request, 'Campos selecionados indicam que o médico atende nesse horário')
    return render(request, 'appointments/doctor_schedule.html', { 'schedule_forms': schedule_forms, 'doctor': doctor })

@login_required(login_url='/')
def appointment(request, id):
    try:
        appointment = get_object_or_404(Appointment, id=id)
    except:
        messages.error(request, 'Consulta não encontrada')
        return redirect('home')
    patient_appointments = Appointment.objects.filter(date__lte=datetime.date.today(), canceled=False).order_by('-date')
    if request.method == 'POST':
        pass
        # appointment_form = AppointmentInProgressForm(request.POST)
        # attendant_form = AttendantForm(request.POST)
        # if user_form.is_valid() and attendant_form.is_valid():
        #     saveUser(user_form, attendant_form)
        #     messages.success(request, 'Novo Atendente criado com sucesso')
        #     return redirect('all_attendant')
        # else:
        #     messages.error(request, 'Verifique os erros abaixo')
    else:
        appointment_form = AppointmentInProgressForm()
        exam_forms = []
        medicine_forms = []
        for index in range(0, 10):
            exam_forms.append(AppointmentExamForm(prefix=str(index), initial={ 'appointment': id }))
            medicine_forms.append(AppointmentMedicineForm(prefix=str(index), initial={ 'appointment': id }))
    return render(request, 'appointments/appointment.html', {'appointment': appointment, 'patient_appointments': patient_appointments, 'appointment_form': appointment_form, 'medicine_forms': medicine_forms, 'exam_forms': exam_forms })

@login_required(login_url='/')
def all_appointments(request):
    try:
        doctor = request.user.doctor.id
        appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
    except:
        appointments = Appointment.objects.order_by('date')
    return render(request, 'appointments/all_appointments.html', {'appointments': appointments})

@login_required(login_url='/')
def patient_appointments(request, id_patient):
    try:
        appointments = get_list_or_404(Appointment.objects.filter(patient=id_patient).order_by('date'))
        return render(request, 'appointments/patient_appointments.html', { 'appointments': appointments, 'id_patient': id_patient })
    except:
        messages.error(request, 'Nenhuma consulta cadastrada')
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
    daynames = []
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form.save()
            messages.success(request, 'Consulta marcada com sucesso')
        else:
            messages.error(request, 'Não foi possível marcar a consulta')
        return redirect('all_patient')
    else:
        start_date = datetime.date.today() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=7)
        appointments_period = Appointment.objects.filter(doctor=id_doctor, canceled=False, date__range=(start_date, end_date)).order_by('date')
        schedules = DoctorSchedule.objects.filter(doctor=id_doctor, available=True).order_by('hour', 'day')
        appointment_forms = {}
        for single_date in date_range(start_date, end_date):
            daynames.append(gettext(single_date.strftime("%A")) + single_date.strftime(", %d/%m"))
        for hour in range(8, 18):
            position = str(datetime.time(hour).strftime("%H:%M"))
            appointment_forms[position] = []
            available_hour = schedules.filter(hour=datetime.time(hour))
            appointments_hour = appointments_period.filter(date__hour=hour);
            for single_date in date_range(start_date, end_date):
                weekday = single_date.weekday()
                available = available_hour.filter(day=weekday)
                appointment = appointments_hour.filter(date__week_day=weekday+2)
                if available:
                    if not appointment:
                        appointment_forms[position].append(AppointmentForm(initial={
                            'date': str(single_date) + ' ' + position,
                            'doctor': id_doctor,
                            'patient': id_patient,
                            'attendant': request.user.attendant
                        }))
                    else:
                        appointment_forms[position].append('appointment')
                else:
                    appointment_forms[position].append('notavailable')
        messages.info(request, 'Clique duas vezes para agendar a consulta')
        return render(request, 'appointments/new_appointment.html', { 'appointment_forms': appointment_forms, 'daynames': daynames })

@login_required(login_url='/')
def details_appointment(request, id):
    try:
        appointment = get_object_or_404(Appointment, id=id)
        return render(request, 'appointments/details_appointment.html', {'appointment': appointment})
    except:
        messages.error(request, 'Consulta não encontrada')
        return redirect('patient_appointments')

@login_required(login_url='/')
def cancel_appointment(request, id):
    if request.method == 'POST':
        appointment = Appointment.objects.get(id=id)
        appointment.canceled = True
        appointment.save()
        messages.success(request, 'Consulta cancelada com sucesso')
        prev = request.POST.get('prev', '/')
        return redirect(prev)
    return redirect('home')

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
