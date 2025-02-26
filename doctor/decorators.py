from functools import wraps
from django.shortcuts import render
from django.urls import reverse

def specialist_check(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_specialist:
             return function(request, *args, **kwargs)
        else:
            return render(request, 'doctor/not_allowed.html')

  return wrap