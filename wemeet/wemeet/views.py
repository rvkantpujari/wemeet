"""from django.shortcuts import render
from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render('404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response"""