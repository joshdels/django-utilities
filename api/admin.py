from django.contrib import admin
from .models import Project, ProjectFile, Asset, Node, Line


for model in [Project, ProjectFile, Asset, Node, Line]:
    admin.site.register(model)
