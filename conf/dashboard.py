"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'whatyouknow.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _

from grappelli.dashboard import modules, Dashboard
# from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        # site_name = get_admin_site_name(context)
        # request = context['request']

        # append a model list module for "Applications"
        self.children.append(modules.ModelList(
            _('Blog'),
            column=1,
            collapsible=True,
            models=('apps.blog.*', 'apps.comments.*', 'apps.*'),
            exclude=('apps.profiles.*',),
        ))

        # append a group for "Administration"
        self.children.append(modules.Group(
            _('Administration'),
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    _('Authentication and Authorization'),
                    column=1,
                    collapsible=False,
                    models=('apps.profiles.*', 'django.contrib.auth.*', 'rest_framework.authtoken.*'),
                ),
                modules.AppList(
                    _('Dictionaries'),
                    collapsible=False,
                    column=1,
                    css_classes=('collapse closed',),
                    exclude=('apps.*',
                             'django.contrib.*',
                             'rest_framework.*',
                             ),
                )
            ],
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent actions'),
            limit=10,
            collapsible=False,
            column=2,
        ))
