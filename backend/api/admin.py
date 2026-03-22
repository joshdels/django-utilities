from django.contrib import admin
from .models import Project, Asset, Node, Pipe


for model in [Project, Asset, Node, Pipe]:
    admin.site.register(model)
