
import logging
from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _
from leonardo.utils.compatibility import FEINCMS_2
from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'

LOG = logging.getLogger(__name__)


class Default(object):

    optgroup = 'Web'

    urls_conf = 'leonardo.module.web.urls'

    @property
    def page_extensions(self):
        if FEINCMS_2:
            return [
                'feincms.module.page.extensions.excerpt',
                'feincms.module.page.extensions.relatedpages',
                'feincms.module.page.extensions.navigation',
                'feincms.module.page.extensions.sites',
                'feincms.module.page.extensions.symlinks',
                'feincms.module.page.extensions.titles',
                'feincms.extensions.seo',
                'feincms.extensions.datepublisher',
                'feincms.extensions.translations',
                'feincms.extensions.changedate',
                'feincms.extensions.ct_tracker',
                'feincms.extensions.featured'
                ]

        return [
            'feincms.module.page.extensions.excerpt',
            'feincms.module.page.extensions.relatedpages',
            'feincms.module.page.extensions.navigation',
            'feincms.module.page.extensions.sites',
            'feincms.module.page.extensions.symlinks',
            'feincms.module.page.extensions.titles',
            'feincms.module.extensions.seo',
            'feincms.module.extensions.datepublisher',
            'feincms.module.extensions.translations',
            'feincms.module.extensions.changedate',
            'feincms.module.extensions.ct_tracker',
            'feincms.module.extensions.featured'
            ]

    @property
    def middlewares(self):

        middlewares = [
            'leonardo.module.web.middlewares.quickstart.QuickStartMiddleware', ]

        return middlewares + [
            'leonardo.module.web.middlewares.web.WebMiddleware',
            'leonardo.module.web.middlewares.horizon.HorizonMiddleware',
        ]

    @property
    def themes(self):
        """supported themes
        """
        return ['leonardo_theme_adminlte', 'leonardo_theme_bootswatch']

    @property
    def apps(self):

        INSTALLED_APPS = []
        for theme in self.themes:
            try:
                __import__(theme)
                INSTALLED_APPS += [theme]
            except ImportError:
                LOG.warning("you are missing available theme {}".format(theme))

        try:
            import sorl  # noqa
            INSTALLED_APPS += ['sorl.thumbnail']
        except Exception:
            pass

        try:
            import easy_thumbnails  # noqa
            INSTALLED_APPS += ['easy_thumbnails']
        except Exception:
            pass

        return INSTALLED_APPS + [
            'feincms',
            'mptt',
            'crispy_forms',
            'floppyforms',

            'dbtemplates',
            'leonardo.module',

            'feincms.module.page',  # noqa

            'leonardo.module.web',

            'markupfield',
        ]

    @property
    def context_processors(self):
        """return WEB Conent Type Processors
        """
        return [
            'leonardo.module.web.processors.page.add_page_if_missing',
        ]

    @property
    def widgets(self):
        return [
            ApplicationWidget,
            SiteHeadingWidget,
            MarkupTextWidget,
            FeedReaderWidget,
            HtmlTextWidget,
            PageTitleWidget,
            IconWidget,
        ]

    plugins = [
        ('leonardo.module.web.apps.horizon', _('Horizon'))
    ]

    js_files = [
        'extra/js/wow.min.js',
    ]

    css_files = [
        'extra/css/animate.css'
    ]

    config = {
        'META_KEYWORDS': ('', _('Site specific meta keywords')),
        'META_DESCRIPTION': ('', _('Site specific meta description')),
        'META_TITLE': ('', _('Site specific meta title')),
        'DEBUG': (True, _('Debug mode')),
    }

    module_actions = ['base/actions.html']


class WebConfig(AppConfig, Default):
    name = 'leonardo.module.web'
    verbose_name = "CMS"

    def ready(self):

        # register signals
        from leonardo.module.web.signals import save as template_save
        from dbtemplates.models import Template

        Template.save = template_save


default = Default()
