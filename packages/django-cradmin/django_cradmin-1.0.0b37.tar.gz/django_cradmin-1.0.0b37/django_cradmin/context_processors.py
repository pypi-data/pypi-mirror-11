from django.conf import settings


def get_setting(settingvariable, fallback=None):
    return getattr(settings, settingvariable, fallback)


def cradmin(request):
    return {
        'DJANGO_CRADMIN_THEME_PATH': get_setting(
            'DJANGO_CRADMIN_THEME_PATH',
            'django_cradmin/dist/css/cradmin_theme_default/theme.css'),
        'DJANGO_CRADMIN_CSS_ICON_LIBRARY_PATH': get_setting(
            'DJANGO_CRADMIN_CSS_ICON_LIBRARY_PATH',
            'django_cradmin/dist/vendor/fonts/fontawesome/css/font-awesome.min.css'),
    }
