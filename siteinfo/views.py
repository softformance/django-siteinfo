# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from siteinfo.models import SiteSettings


def set_redirect_stop(request):
    request.session['site_redirect_stop'] = True
    response = HttpResponseRedirect('/')
    return response

def test_offline_page(request):
    current = SiteSettings.objects.get_current()
    return render_to_response(['siteinfo/offline_page-%s.html' % current.site.domain,
                               'siteinfo/offline_page.html',],
                          {'text': current.inactive_text,
                           'image': current.inactive_image, 
                           'domain':current.site.domain},
                          context_instance=RequestContext(request))