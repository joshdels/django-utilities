from django.contrib import admin
from .models import Project, ProjectFile, DatasetVersion, Layer


class LayerInline(admin.TabularInline):
    model = Layer
    extra = 0
    fields = ("name", "geometry_type", "is_active", "dataset_version")
    readonly_fields = ()


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0
    fields = ("name", "file")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "current_version", "created_at")
    inlines = [LayerInline, ProjectFileInline]


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


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "geometry_type", "is_active")
    list_filter = ("project", "is_active", "geometry_type")
    search_fields = ("name", "project__name")
    list_editable = ("is_active",)
    ordering = ("project", "name")
