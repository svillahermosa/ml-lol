import json
import os

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import hashlib
from functools import wraps

import logging
import copy
from django.template.loader import render_to_string


def base(request, *args, **kwargs):
    return render(request, "base.html")


