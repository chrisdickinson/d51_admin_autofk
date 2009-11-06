from django import forms
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
import os

MEDIA_JQUERY = getattr(settings, 'D51_ADMIN_AUTOFK_JQUERY', "http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js")
MEDIA_D51AUTO_JS = os.path.join(getattr(settings, 'D51_ADMIN_AUTOFK_MEDIA', 'd51autofk'), 'js/jquery.d51auto.js')
MEDIA_D51AUTO_CSS = os.path.join(getattr(settings, 'D51_ADMIN_AUTOFK_MEDIA', 'd51autofk'), 'css/jquery.d51auto.css')

class AutocompleteWidget(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super(AutocompleteWidget, self).value_from_datadict(data, files, name)
        if value is not None and value != '':
            pk = None
            try:
                query = {'%s__exact'%self.name_field:value}
                obj = self.model.objects.get(**query)
                pk = obj.pk
            except self.model.DoesNotExist:
                if isinstance(self.instantiate_fn, self.value_from_datadict.__class__):
                    pk = self.instantiate_fn(data, name)
                else:
                    pk = self.instantiate_fn(self, data, name)
            return pk
        return None

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        real_value = None
        if value is not None:
            try:
                real_value = self.model.objects.get(pk__exact=value)
                real_value = getattr(real_value, self.name_field)
            except self.model.DoesNotExist:
                real_value = ''

        reversed_url = reverse(self.target_url, args=('json',))
        output = """
            %s
            <script type="text/javascript">
                $(function(){
                    $('input[name=%s]').autocomplete({
                            'url':"%s",
                            'query_functions':%s
                    });
                });
            </script>
        """
        output = output % (
            super(AutocompleteWidget, self).render(name, real_value, attrs),
            name,
            reversed_url,
            simplejson.dumps(self.js_methods),
        )
        return mark_safe(output)

    class Media:
        js = (MEDIA_JQUERY,MEDIA_D51AUTO_JS)
        css =  {'all': (MEDIA_D51AUTO_CSS,)}
