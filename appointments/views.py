from django.shortcuts import render
from .models import Attendant
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def index(request):
    latest_question_list = Attendant.objects.order_by('name')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'appointments/index.html', context)
