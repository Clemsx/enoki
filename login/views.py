from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.http.response import JsonResponse

from django.shortcuts import render, redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings

from datetime import datetime, timedelta
from jours_feries_france import JoursFeries

import numpy as np


class IndexView(TemplateView):
    template_name = "index.html"
    
    def get(self, request, *args, **kwargsuest):
    
        context = {}

        return render(request, self.template_name, context)
    
class CalendarView(TemplateView):
    template_name = "calendar.html"
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargsuest):

        context = {
            'username': request.user.username,
        }

        return render(request, self.template_name, context)
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargsuest):
        
        if self.request.is_ajax():
            
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            holidays = {}
            holidays['weekday'] = []
            holidays['sunday'] = []

            res = {}
            res['holiday_weekday'] = 0
            res['holiday_sunday'] = 0
                         
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            
            # Convert str to datetime
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date += timedelta(days=1)
            
            # Get only the date, we don't need the time
            start_date = start_date.date()
            end_date = end_date.date()
            
            if start_date > end_date:
                return JsonResponse({'date_error': 'La date de départ ne doit pas être supérieur à la date de fin'}, status=400)
                        
            for day in weekdays:
                count = np.busday_count(start_date, end_date, weekmask=day)
                res[day.lower()] = int(count)
            
            # Number of year
            nb_year = end_date.year - start_date.year
            
            for i in range(nb_year + 1):
                days = JoursFeries.for_year(start_date.year + i)
                
                for name, date in days.items():
                    
                    # Separate weekday and sunday                   
                    if date.weekday() < 6:
                        holidays['weekday'].append(date)
                    else:
                        holidays['sunday'].append(date)
            
            # We check if holidays date are between selected date by the user
            for days in holidays:
                for date in holidays[days]:
                    if (start_date <= date < end_date) and (days == "weekday"):
                        res['holiday_weekday'] = res['holiday_weekday'] + 1
                    elif (start_date <= date < end_date) and (days == "sunday"):
                        res['holiday_sunday'] = res['holiday_sunday'] + 1
            
            return JsonResponse(res, status=200)
