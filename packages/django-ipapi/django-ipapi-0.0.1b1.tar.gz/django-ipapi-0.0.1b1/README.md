About
=====

django-ip-com is a django app for http://ip-api.com/

WARNING: This is BETA app! See LICENSE.

Usage
=====

- Install: pip install django-ipapi    
- Add 'ipapi' to INSTALLED_APPS
- Add 'ipapi.middleware.CheckCountryCodeMiddleware' to MIDDLEWARE_CLASSES
- Set IPAPI_ALLOWED_COUNTRIES = ['your iso-country-code',]     
- Test on localhost: http://localhost:8000/pl/?__ipapi__=208.80.152.201