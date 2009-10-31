from django.db import models
from widgets import AutocompleteWidget

def fail_instantiate(widget, post_dict, formfield_name):
    return None

def attempt_instantiate(widget, post_dict, formfield_name):
    if formfield_name not in post_dict.keys():
        return None
    return widget.model(**{widget.name_field:post_dict.get(formfield_name)})

class ForeignKey(models.ForeignKey):
    def __init__(self, to,
                target_url=None, 
                js_methods=None, 
                instantiate_fn=None, 
                name_field=None, 
                *args, **kwargs):
        self.model = to 
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

        self.target_url = target_url
        if self.target_url is None:
            info = self.model._meta.app_label, self.model._meta.module_name
            self.target_url = 'admin:admin-piston-%s-%s' % info
        
        self.js_methods = js_methods
        if self.js_methods is None:
            self.js_methods = ['startswith_json',]

        self.name_field = name_field 
        if self.name_field is None:
            self.name_field = 'name' 
        return super(self.__class__, self).__init__(to, *args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = self.generate_autocomplete_widget() 
        return super(ForeignKey, self).formfield(*args, **kwargs)

    def generate_autocomplete_widget(self):
        """
            trickiness abounds: this creates a closure-class
            that'll render our widget the way we want
        """
        new_class = type(object)('ForeignKeyACWidget', (AutocompleteWidget,), {
            'target_url':self.target_url,
            'js_methods':self.js_methods,
            'model':self.model,
            'name_field':self.name_field,
            'instantiate_fn':self.instantiate_fn
        })
        return new_class
