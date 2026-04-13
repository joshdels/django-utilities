from django.contrib import admin
from .models import CaseStudy, CaseStudyBlock, CaseTag


class CaseStudyBlockInline(admin.TabularInline):
    model = CaseStudyBlock
    extra = 1
    ordering = ("order",)
    fields = ("block_type", "text", "image", "order")


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "money_tag", "created_at")
    inlines = [CaseStudyBlockInline]


@admin.register(CaseTag)
class CaseTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
