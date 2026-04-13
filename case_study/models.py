from django.db import models


class CaseTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CaseStudy(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    main_image = models.ImageField(upload_to="case-study", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    money_tag = models.ForeignKey(
        CaseTag, on_delete=models.PROTECT, related_name="case_studies"
    )


class CaseStudyBlock(models.Model):
    case_study = models.ForeignKey(
        CaseStudy, on_delete=models.CASCADE, related_name="blocks"
    )

    BLOCK_TYPES = [
        ("image", "Image"),
        ("text", "Text"),
        ("quote", "Quote"),
        ("heading", "Heading"),
    ]

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="case-study/blocks/", blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
