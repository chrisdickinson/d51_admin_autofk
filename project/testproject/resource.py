from piston.resource import Resource
from piston.handler import BaseHandler
from models import SimpleModel

class SimpleModelHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = SimpleModel
    fields = ('pk', 'name', 'date_added')

    def read(self, request):
        query = request.GET.get('query', None)
        return SimpleModel.objects(name__startswith=query)

simplemodel_resource = Resource(handler=SimpleModelHandler)
