from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.db.models import Count
from .models import Appointment, Doctor, Attendant, Patient, DoctorSchedule, AppointmentExam, AppointmentMedicine
from .forms import AppointmentForm, AppointmentInProgressForm, AppointmentExamForm, AppointmentMedicineForm, DoctorScheduleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime as datetime
from datetime import timedelta, date
from django.utils.translation import gettext

@login_required(login_url='/')
def index(request):
    try:
        doctor = request.user.doctor.id
        appointments = Appointment.objects.filter(doctor=doctor, date__gte=datetime.date.today(), canceled=False).order_by('date')
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
    if appointment.attended:
        return redirect('details_appointment', id=appointment.id)
    patient_appointments = Appointment.objects.filter(date__lte=datetime.date.today(), canceled=False, patient=appointment.patient).order_by('-date')
    exam_forms = []
    medicine_forms = []
    if request.method == 'POST':
        formInvalid = False
        appointment_form = AppointmentInProgressForm(request.POST, instance=appointment)
        if not appointment_form.is_valid():
            formInvalid = True
        totalExams = int(request.POST.get('totalExams'))
        totalMedicines = int(request.POST.get('totalMedicines'))
        for index in range(0, totalExams):
            exam_forms.append(AppointmentExamForm(request.POST, prefix=str(index)))
            if not exam_forms[index].is_valid():
                formInvalid = True
        for index in range(0, totalMedicines):
            medicine_forms.append(AppointmentMedicineForm(request.POST, prefix=str(index)))
            if not medicine_forms[index].is_valid():
                formInvalid = True
        if not formInvalid:
            appointment_form.save()
            for index in range(0, totalExams):
                exam_forms[index].save()
            for index in range(0, totalMedicines):
                medicine_forms[index].save()
            messages.success(request, 'Consulta marcada com sucesso')
            return redirect('home')
        else:
            messages.error(request, 'Verifique os erros abaixo')
            return render(request, 'appointments/appointment.html', {'appointment': appointment, 'patient_appointments': patient_appointments, 'appointment_form': appointment_form, 'medicine_forms': medicine_forms, 'exam_forms': exam_forms })
    else:
        appointment_form = AppointmentInProgressForm(instance=appointment, initial={ 'attended': True })
        for index in range(0, 10):
            exam_forms.append(AppointmentExamForm(prefix=str(index), initial={ 'appointment': id }))
            medicine_forms.append(AppointmentMedicineForm(prefix=str(index), initial={ 'appointment': id }))
    return render(request, 'appointments/appointment.html', {'appointment': appointment, 'patient_appointments': patient_appointments, 'appointment_form': appointment_form, 'medicine_forms': medicine_forms, 'exam_forms': exam_forms })

@login_required(login_url='/')
def all_appointments(request):
    try:
        doctor = request.user.doctor.id
        appointments = Appointment.objects.filter(doctor=doctor, canceled=False).order_by('date')
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
    except:
        messages.error(request, 'Consulta não encontrada')
        return redirect('patient_appointments')
    exams = AppointmentExam.objects.filter(appointment=appointment.id)
    medicines = AppointmentMedicine.objects.filter(appointment=appointment.id)
    patient_appointments = Appointment.objects.filter(date__lte=datetime.date.today(), canceled=False, patient=appointment.patient).order_by('-date')
    return render(request, 'appointments/details_appointment.html', { 'appointment': appointment, 'exams': exams, 'medicines': medicines, 'patient_appointments': patient_appointments })

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def statistics(request):
    total_appointments = Appointment.objects.filter().count()
    total_attended = Appointment.objects.filter(attended=True).count()
    total_canceled = Appointment.objects.filter(canceled=True).count()
    total_doctors = Doctor.objects.filter().count()
    total_patients = Patient.objects.filter().count()
    total_attendants = Attendant.objects.filter().count()
    total_exams = AppointmentExam.objects.filter().count()
    total_medicines = AppointmentMedicine.objects.filter().count()
    topten_exams = AppointmentExam.objects.values('exam', 'exam__name').annotate(count=Count('exam')).order_by('-count')[:10]
    topten_medicines = AppointmentMedicine.objects.values('medicine', 'medicine__generic_name', 'medicine__factory_name').annotate(count=Count('medicine')).order_by('-count')[:10]
    topten_patients = Appointment.objects.values('patient', 'patient__name').annotate(count=Count('patient')).order_by('-count')[:10]
    topten_patients_cancel = Appointment.objects.filter(canceled=True).values('patient', 'patient__name').annotate(count=Count('patient')).order_by('-count')[:10]
    topten_doctors = Appointment.objects.values('doctor', 'doctor__name', 'doctor__speciality').annotate(count=Count('doctor')).order_by('-count')[:10]
    topten_specialitys = Appointment.objects.values('doctor__speciality').annotate(count=Count('doctor__speciality')).order_by('-count')[:10]
    context = {
        'total_appointments': total_appointments,
        'total_attended': total_attended,
        'total_canceled': total_canceled,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_attendants': total_attendants,
        'total_exams': total_exams,
        'total_medicines': total_medicines,
        'topten_exams': topten_exams,
        'topten_medicines': topten_medicines,
        'topten_patients': topten_patients,
        'topten_patients_cancel': topten_patients_cancel,
        'topten_doctors': topten_doctors,
        'topten_specialitys': topten_specialitys,
    }
    return render(request, 'appointments/statistics.html', context)

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
