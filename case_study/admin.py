from django.contrib import admin
from .models import CaseStudy, CaseStudyBlock, CaseTag


class CaseStudyBlockInline(admin.TabularInline):
    model = CaseStudyBlock
    extra = 1
    ordering = ("order",)
    fields = ("block_type", "text", "image", "order")


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "display_tags", "created_at")
    inlines = [CaseStudyBlockInline]

    filter_horizontal = ("tags",)

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags"


@admin.register(CaseTag)
class CaseTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
