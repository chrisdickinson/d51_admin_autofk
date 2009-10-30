from django.db import models
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms
import os

MEDIA_JQUERY = getattr(settings, 'D51_ADMIN_AUTOFK_JQUERY', "http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js")
MEDIA_D51AUTO_JS = os.path.join(getattr(settings, 'D51_ADMIN_AUTOFK_MEDIA', 'd51autofk'), 'js/jquery.d51auto.js')
MEDIA_D51AUTO_CSS = os.path.join(getattr(settings, 'D51_ADMIN_AUTOFK_MEDIA', 'd51autofk'), 'css/jquery.d51auto.css')

def fail_instantiate(widget, post_dict, formfield_name):
    return None

def attempt_instantiate(widget, post_dict, formfield_name):
    if name not in datadict.keys():
        return None
    return widget.model(**{widget.name_field:datadict.get(name)})

class ForeignKey(models.ForeignKey):
    def __init__(self, to,
                target_url, 
                js_methods, 
                instantiate_fn=None, 
                name_field=None, 
                *args, **kwargs):
        self.instantiate_fn = instantiate_fn 

        def instantiate_wrapper(fn):
            def inner(*args, **kwargs):
                obj = fn(*args, **kwargs)
                obj.save()
                return obj.pk
            return inner

        if self.instantiate_fn is None:
            self.instantiate_fn = attempt_instantiate
        self.instantiate_fn = instantiate_wrapper(self.instantiate_fn)
        self.name_field = name_field 
        if self.name_field is None:
            self.name_field = 'name' 
            
        self.target_url = target_url
        self.js_methods = js_methods
        return super(self.__class__, self).__init__(to, *args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = self.generate_autocomplete_widget() 
        return super(ForeignKey, self).formfield(*args, **kwargs)

    def generate_autocomplete_widget(self):
        """
            trickiness abounds: this creates a closure-class
            that'll render our widget the way we want
        """
        class AutocompleteWidget(forms.TextInput):
            def __init__(w_self, *args, **kwargs):
                w_self.target_url = self.target_url
                w_self.js_methods = self.js_methods
                w_self.model = self.related
                w_self.instantiate_fn = self.instantiate_fn
                return super(w_self.__class__, w_self).__init__(*args, **kwargs)

            def value_from_datadict(w_self, data, files, name):
                value = super(w_self.__class__, w_self).value_from_datadict(data, files, name)
                if value is not None and value != '':
                    pk = None
                    try:
                        query = {'%s__exact'%self.name_field:value}
                        obj = self.model.objects.get(**query)
                        pk = obj.pk
                    except w_self.model.DoesNotExist:
                        pk = w_self.instantiate_fn(self, data, name)
                    return pk
                return None

            def render(w_self, name, value, attrs=None):
                if attrs is None:
                    attrs = {}
                real_value = None
                if value is not None:
                    try:
                        real_value = model.objects.get(pk__exact=value)
                        real_value = getattr(real_value, w_self.name_field)
                    except w_self.model.DoesNotExist:
                        real_value = ''
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
                    super(w_self.__class__, w_self).render(name, value, attrs),
                    name,
                    reverse(w_self.target_url),
                    simplejson.dumps(w_self.js_methods),
                )
                return mark_safe(output)

            class Media:
                js = (MEDIA_JQUERY,MEDIA_D51AUTO_JS)
                css =  {'all': (MEDIA_D51AUTO_CSS,)}
        return AutocompleteWidget
