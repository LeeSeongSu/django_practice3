from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from appname.models import CustomUser
from shop.models import Item
class RecipientView(TemplateView):
    template_name = 'core/chat.html'
    def get(self,request,name):
        ctx = {}
        recipient = get_object_or_404(CustomUser,username=name)
        ctx['recipient'] = recipient
        return self.render_to_response(ctx)