###
# Copyright (c) 2006-2009, Jared Kuolt, chbrown, Maik Lustenberger 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the SuperJared.com nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###

import re

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from siteinfo.compatibility import is_anonymous
from siteinfo.models import SiteSettings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class RequireLoginMiddleware(MiddlewareMixin):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication for all urls except 
    those defined in PUBLIC_URLS in settings.py. PUBLIC_URLS should be a tuple of regular 
    expresssions for the urls you want anonymous users to have access to. If PUBLIC_URLS 
    is not defined, it falls back to LOGIN_URL or failing that '/accounts/login/'.  
    Requests for urls not matching PUBLIC_URLS get redirected to LOGIN_URL with next set 
    to original path of the unauthenticted request. 
    Any urls statically served by django are excluded from this check. To enforce the same
    validation on these set SERVE_STATIC_TO_PUBLIC to False.
    """

    def __init__(self, *args, **kwargs):
        super(RequireLoginMiddleware, self).__init__(*args, **kwargs)

        self.login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        public_urls = []

        if hasattr(settings, 'PUBLIC_URLS'):
            public_urls = [re.compile(url) for url in settings.PUBLIC_URLS]
        public_urls += [(re.compile("^%s$" % self.login_url[1:]))]
        # Todo: problem with root_urlconf.urls.patterns: 
        # AttributeError: 'module' object has no attribute 'urlpatterns' (or 'urls')
        if False and getattr(settings, 'SERVE_STATIC_TO_PUBLIC', True):
            root_urlconf = __import__(settings.ROOT_URLCONF)
            public_urls.extend([re.compile(url.regex)
                                for url in root_urlconf.urls.urlpatterns
                                if url.__dict__.get('_callback_str') == 'django.views.static.serve'
                                ])
        self.public_urls = tuple(public_urls)

    def process_request(self, request):
        """
        Redirect anonymous users to login_url from non public urls

        If an anonymous user requests a page, he/she is redirected to the login
        page set by LOGIN_URL depending on the DB setting require_login of
        SiteSettings model.
        """
        if getattr(settings, 'IS_DEV_SERVER', False) or \
                request.META.get('REMOTE_ADDR', '*') in getattr(settings, 'INTERNAL_IPS', []):
            return None
        try:
            current = SiteSettings.objects.get_current()
            if current:
                require_login = current.require_login
            else:
                require_login = False
            if require_login:
                for url in self.public_urls:
                    if url.match(request.path[1:]):
                        return None
                if is_anonymous(request.user) or require_login == 'staff' and not request.user.is_staff:
                    if request.POST:
                        return LoginView.as_view()(request)
                    else:
                        return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))
        except AttributeError:
            return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))
