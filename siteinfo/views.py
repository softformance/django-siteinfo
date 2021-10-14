import django
from django.http import HttpResponseRedirect
from django.shortcuts import render

from siteinfo.models import SiteSettings


def set_redirect_stop(request):
    request.session['site_redirect_stop'] = True
    response = HttpResponseRedirect('/')
    return response


def test_offline_page(request):
    current = SiteSettings.objects.get_current()
    templates = ['siteinfo/offline_page-%s.html' % current.site.domain, 'siteinfo/offline_page.html']
    context = {'text': current.inactive_text,
               'image': current.inactive_image,
               'domain': current.site.domain}
    return render(request, templates, context)
