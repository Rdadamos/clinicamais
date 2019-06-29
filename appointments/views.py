from django.shortcuts import render
from .models import Attendant

def index(request):
    latest_question_list = Attendant.objects.order_by('name')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'appointments/index.html', context)
