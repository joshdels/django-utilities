from django.contrib import admin
from .models import Project, ProjectFile, Asset, Node, Pipe


for model in [Project, ProjectFile, Asset, Node, Pipe]:
    admin.site.register(model)
