from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Attendant, Doctor, Patient, User
from appointments.models import Appointment, DoctorSchedule
from .forms import AttendantForm, DoctorForm, PatientForm, UserPatientForm, UserForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import attendant_only
from datetime import datetime, date
import datetime as dt

# Attendant
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def all_attendant(request):
    try:
        attendants = get_list_or_404(Attendant)
        return render(request, 'users/all_attendant.html', {'attendants': attendants})
    except:
        messages.error(request, 'Nenhum atendente cadastrado')
        return redirect('new_attendant')

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def details_attendant(request, id):
    try:
        attendant = get_object_or_404(Attendant, id=id)
        return render(request, 'users/details_attendant.html', {'attendant': attendant})
    except:
        messages.error(request, 'Atendente não encontrado')
        return redirect('all_attendant')

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def new_attendant(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        attendant_form = AttendantForm(request.POST)
        if user_form.is_valid() and attendant_form.is_valid():
            saveUser(user_form, attendant_form)
            messages.success(request, 'Novo Atendente criado com sucesso')
            return redirect('all_attendant')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserForm()
        attendant_form = AttendantForm()
    return render(request, 'users/new.html', {'user_form': user_form, 'profile_form': attendant_form, 'userType': 'Atendente', 'url_all': 'all_attendant' })

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def update_attendant(request, id):
    attendant = Attendant.objects.get(user=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=attendant.user)
        attendant_form = AttendantForm(request.POST, instance=attendant)
        if user_form.is_valid() and attendant_form.is_valid():
            updateUser(user_form, attendant_form)
            messages.success(request, 'Atendente atualizado com sucesso')
            return redirect('all_attendant')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserForm(instance=attendant.user)
        attendant_form = AttendantForm(instance=attendant)
    return render(request, 'users/update.html', {'user_form': user_form, 'profile_form': attendant_form, 'userType': 'Atendente', 'url_all': 'all_attendant' })

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def delete_attendant(request, id):
    if request.method == 'POST':
        attendant = Attendant.objects.get(id=id)
        User.objects.filter(id=attendant.user.id).delete()
        Attendant.objects.filter(id=id).delete()
        messages.success(request, 'Atendente deletado com sucesso')
    return redirect('all_attendant')

# Doctor
@attendant_only
def all_doctor(request):
    try:
        doctors = get_list_or_404(Doctor)
        return render(request, 'users/all_doctor.html', {'doctors': doctors})
    except:
        messages.error(request, 'Nenhum médico cadastrado')
        return redirect('new_doctor')

@attendant_only
def details_doctor(request, id):
    try:
        doctor = get_object_or_404(Doctor, id=id)
        return render(request, 'users/details_doctor.html', {'doctor': doctor})
    except:
        messages.error(request, 'Médico não encontrado')
        return redirect('all_doctor')

@attendant_only
def new_doctor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            doctor = saveUser(user_form, doctor_form)
            # initial empty schedule
            for hour in range(8, 18):
                hourS = dt.time(hour)
                for day in range(0, 6):
                    schedule = DoctorSchedule(day=day, hour=hourS, doctor=doctor, available=False)
                    schedule.save()
            #
            messages.success(request, 'Novo Médico criado com sucesso')
            return redirect('all_doctor')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserForm()
        doctor_form = DoctorForm()
    return render(request, 'users/new.html', {'user_form': user_form, 'profile_form': doctor_form, 'userType': 'Médico', 'url_all': 'all_doctor' })

@attendant_only
def update_doctor(request, id):
    doctor = Doctor.objects.get(user=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=doctor.user)
        doctor_form = DoctorForm(request.POST, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            updateUser(user_form, doctor_form)
            messages.success(request, 'Médico atualizado com sucesso')
            return redirect('all_doctor')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserForm(instance=doctor.user)
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'users/update.html', {'user_form': user_form, 'profile_form': doctor_form, 'userType': 'Médico', 'url_all': 'all_doctor' })

@attendant_only
def delete_doctor(request, id):
    if request.method == 'POST':
        doctor = Doctor.objects.get(id=id)
        User.objects.filter(id=doctor.user.id).delete()
        Doctor.objects.filter(id=id).delete()
        messages.success(request, 'Médico deletado com sucesso')
    return redirect('all_doctor')

# Patient
@attendant_only
def all_patient(request):
    try:
        patients = get_list_or_404(Patient)
        return render(request, 'users/all_patient.html', {'patients': patients})
    except:
        messages.error(request, 'Nenhum paciente cadastrado')
        return redirect('new_patient')

@login_required(login_url='/')
def details_patient(request, id):
    try:
        patient = get_object_or_404(Patient, id=id)
    except:
        messages.error(request, 'Paciente não encontrado')
        return redirect('all_patient')
    patient_appointments = Appointment.objects.filter(date__lte=dt.date.today(), canceled=False, patient=patient).order_by('-date')
    return render(request, 'users/details_patient.html', { 'patient': patient, 'patient_appointments': patient_appointments})

@attendant_only
def new_patient(request):
    if request.method == 'POST':
        user_form = UserPatientForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            saveUser(user_form, patient_form)
            messages.success(request, 'Novo Paciente criado com sucesso')
            return redirect('all_patient')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserPatientForm(initial={'username': 'paciente' + datetime.now().strftime('%m%d%Y%H%M%S%f'), 'password': 'paciente'})
        patient_form = PatientForm()
    return render(request, 'users/new.html', {'user_form': user_form, 'profile_form': patient_form, 'userType': 'Paciente', 'url_all': 'all_patient' })

@attendant_only
def update_patient(request, id):
    patient = Patient.objects.get(user=id)
    if request.method == 'POST':
        user_form = UserPatientForm(request.POST, instance=patient.user)
        patient_form = PatientForm(request.POST, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            updateUser(user_form, patient_form)
            messages.success(request, 'Paciente atualizado com sucesso')
            return redirect('all_patient')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        user_form = UserPatientForm(instance=patient.user)
        patient_form = PatientForm(instance=patient)
    return render(request, 'users/update.html', {'user_form': user_form, 'profile_form': patient_form, 'userType': 'Paciente', 'url_all': 'all_patient' })

@attendant_only
def delete_patient(request, id):
    if request.method == 'POST':
        patient = Patient.objects.get(id=id)
        User.objects.filter(id=patient.user.id).delete()
        Patient.objects.filter(id=id).delete()
        messages.success(request, 'Paciente deletado com sucesso')
    return redirect('all_patient')

# User
def saveUser(user_form, profile_form):
    post_user = user_form.save(commit=False)
    profile_form = profile_form.save(commit=False)
    post_user.password = make_password(user_form.cleaned_data['password'])
    user_form.save()
    user = User.objects.get(username=post_user.username)
    profile_form.user = user
    profile_form.save()
    return profile_form

def updateUser(user_form, profile_form):
    post_user = user_form.save(commit=False)
    post_user.password = make_password(user_form.cleaned_data['password'])
    user_form.save()
    profile_form.save()
