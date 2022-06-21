from asyncio import events
from datetime import datetime, timedelta, date
from multiprocessing.spawn import import_main_path
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .models import *
from .utils import Calendar
from .forms import EventForm
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class=EventSerializer
    queryset=Event.objects.all()
    def list(self,request):
        print('--------------------------------1212')
        events=Event.objects.filter(user=self.request.user)
        print(events)
        serializer= EventSerializer(events, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        id=pk
        if id is not None:
            event=Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
    def create(self, request):
        serializer= EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg: Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk):
        id=pk
        event=Event.objects.get(pk=id)
        serializer= EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg: Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk):
        id = pk
        event= Event.objects.get(pk=id)
        event.delete()
        return Response({'msg: Complete Data Deleted'})

        
def index(request):
    return HttpResponse('hello')

def register(request):
    print('Register view')
    if request.method== 'POST':
        fullname= request.POST.get('name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        user_obj= User(username=username, email=email, first_name= fullname) 
        user_obj.set_password(password)
        user_obj.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        
        return redirect('calendar/!')
    return render(request,'User/register.html')
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/calendar/!')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        if user:
            username = user.username
            user = authenticate(request, username=username, password=password) # check password

        if user is not None:
            login(request, user)
            return redirect('/calendar/!')	
        
    return render(request,'User/login.html',)
def logoutUser(request):
    print('1212122')
    logout(request)
    return redirect('/')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(request=self.request.user,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        new=form.save()
        new.user= request.user
        new.save()
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})


    # Rest FrameWork