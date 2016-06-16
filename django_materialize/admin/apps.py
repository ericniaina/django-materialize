import warnings
from importlib import import_module
from django.apps import AppConfig
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import RegexURLResolver, Resolver404
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.module_loading import module_has_submodule


class ModuleMatchName(str):
    pass


class ModuleURLResolver(RegexURLResolver):
    def __init__(self, *args, **kwargs):
        self._module = kwargs.pop('module')
        super(ModuleURLResolver, self).__init__(*args, **kwargs)

    def resolve(self, *args, **kwargs):
        result = super(ModuleURLResolver, self).resolve(*args, **kwargs)

        if result and not getattr(self._module, 'installed', True):
            raise Resolver404({'message': 'Module not installed'})

        result.url_name = ModuleMatchName(result.url_name)
        result.url_name.module = self._module

        return result


class ModuleMixin(object):
    """
    Extension for the django AppConfig. Makes django app pluggable at runtime.
    - Application level user permission access
    - Runtime app installation/deinstallation
    - Autodiscovery for <app_module>/urls.py
    - Collect common website menu from `<app_label>/menu.html`
    Example::
        class Sales(ModuleMixin, AppConfig):
            name = 'sales'
            icon = '<i class="material-icons">call</i>'
    The application have to have <app_module>/urls.py file, with
    a single no-parametrized url with name='index', ex::
        urlpatterns = [
            url('^$', generic.TemplateView.as_view(template_name="sales/index.html"), name="index"),
        ]
    All AppConfigs urls will be included into material.frontend.urls automatically under /<app_label>/ prefix
    The AppConfig.label, used for the urls namespace.
    The menu.html sample::
        <ul>
            <li><a href="{% url 'sales:index' %}">Dashboard</a></li>
            <li><a href="{% url 'sales:customers' %}">Customers</a></li>
            {% if perms.sales.can_add_lead %}<li><a href="{% url 'sales:leads' %}">Leads</a></li>{% endif %}
        </ul>
    In all application templates, the current application config
    instance would be available as `current_module` template variable
    """
    order = 10
    icon = '<i class="material-icons">receipt</i>'

    @property
    def verbose_name(self):
        return self.label.title()

    @property
    def installed(self):
        from .models import Module as DbModule
        return DbModule.objects.installed(self.label)

    def description(self):
        return (self.__doc__ or "").strip()

    def has_perm(self, user):
        return True

    def get_urls(self):
        if module_has_submodule(self.module, 'urls'):
            urls_module_name = '%s.%s' % (self.name, 'urls')
            urls_module = import_module(urls_module_name)
            if hasattr(urls_module, 'urlpatterns'):
                return urls_module.urlpatterns

        warnings.warn('Module {} have not urls.py submodule or `urlpatterns` in it'.format(self.label))
        return []

    @property
    def urls(self):
        base_url = r'^{}/'.format(self.label)
        return ModuleURLResolver(base_url, self.get_urls(), module=self, app_name=self.label, namespace=self.label)

    def index_url(self):
        return reverse('{}:index'.format(self.label))

    def menu(self):
        try:
            return get_template('{}/menu.html'.format(self.label))
        except TemplateDoesNotExist:
            return Template('')


class MaterialAdminConfig(ModuleMixin, AppConfig):
    name = 'django_materialize.admin'
    label = "django_materialize_admin"

    icon = '<i class="material-icons">settings_application</i>'
    verbose_name = _("Administration")
    order = 1000

    @property
    def urls(self):
        return ModuleURLResolver(r'^admin/', admin.site.urls[0], namespace='admin', module=self)

    def index_url(self):
        return reverse('admin:index'.format(self.label))

    def has_perm(self, user):
        return user.is_staff
