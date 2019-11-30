from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Medicine
from .forms import MedicineForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def all_medicine(request):
    try:
        medicines = get_list_or_404(Medicine)
        return render(request, 'medicines/all_medicine.html', {'medicines': medicines})
    except:
        messages.error(request, 'Nenhum medicamento cadastrado')
        return redirect('new_medicine')

@login_required(login_url='/')
def details_medicine(request, id):
    try:
        medicine = get_object_or_404(Medicine, id=id)
        return render(request, 'medicines/details_medicine.html', {'medicine': medicine})
    except:
        messages.error(request, 'Medicamento não encontrado')
        return redirect('all_medicine')

@login_required(login_url='/')
def new_medicine(request):
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)
        if medicine_form.is_valid():
            medicine_form.save()
            messages.success(request, 'Novo medicamento cadastrado com sucesso')
            return redirect('all_medicine')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        medicine_form = MedicineForm()
    return render(request, 'medicines/new.html', {'medicine_form': medicine_form })

@login_required(login_url='/')
def update_medicine(request, id):
    medicine = Medicine.objects.get(id=id)
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST, instance=medicine)
        if medicine_form.is_valid():
            medicine_form.save()
            messages.success(request, 'Medicamento atualizado com sucesso')
            return redirect('all_medicine')
        else:
            messages.error(request, 'Verifique os erros abaixo')
    else:
        medicine_form = MedicineForm(instance=medicine)
    return render(request, 'medicines/update.html', {'medicine_form': medicine_form })

@login_required(login_url='/')
def delete_medicine(request, id):
    if request.method == 'POST':
        Medicine.objects.filter(id=id).delete()
        messages.success(request, 'Medicamento deletado com sucesso')
    return redirect('all_medicine')
