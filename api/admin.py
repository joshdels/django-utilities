from django.contrib import admin
from .models import Project, ProjectFile, DatasetVersion


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "current_version", "created_at")


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project")


@admin.register(DatasetVersion)
class DatasetVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "version", "is_active", "created_at")
    list_filter = ("project", "is_active")

    def asset_count(self, obj):
        return obj.asset_set.count()

    asset_count.short_description = "Assets"
