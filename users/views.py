from django.shortcuts import redirect, render
from .models import Attendant, User
from .forms import UserForm, AttendantForm

def attendant(request):
    latest_question_list = Attendant.objects.order_by('name')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'appointments/index.html', context)

def new_attendant(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        attendant_form = AttendantForm(request.POST)
        if user_form.is_valid() and attendant_form.is_valid():
            user_form.save()
            post_user = user_form.save(commit=False)
            post_attendant = attendant_form.save(commit=False)
            user = User.objects.get(username=post_user.username)
            post_attendant.user = user
            attendant_form.save()
            # messages.success(request, _('Your attendant was successfully updated!'))
            return redirect('home')
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm()
        attendant_form = AttendantForm()
    return render(request, 'users/new_attendant.html', {
        'user_form': user_form,
        'attendant_form': attendant_form
    })


def update_attendant(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        attendant_form = AttendantForm(request.POST, instance=request.user.attendant)
        if user_form.is_valid() and attendant_form.is_valid():
            user_form.save()
            attendant_form.save()
            # messages.success(request, _('Your attendant was successfully updated!'))
            # return redirect('settings:attendant')
            # return render(request, 'appointments/index.html')
            return redirect('home')
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        attendant_form = AttendantForm(instance=request.user.attendant)
    return render(request, 'users/update_attendant.html', {
        'user_form': user_form,
        'attendant_form': attendant_form
    })
