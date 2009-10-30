from piston.handler import BaseHandler
from piston.resource import Resource
from models import SimpleModel

class SimpleModelHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = SimpleModel
    fields = ('pk', 'name', 'date_added')

    def read(self, request, query):
        return SimpleModel.objects(name__startswith=query)

simplemodel_resource = Resource(handler=SimpleModelHandler)
