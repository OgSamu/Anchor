from django.db import models
from user.models import User
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_file_size(file):
    max_size_kb = 153600
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Max file size is {max_size_kb}KB")


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User, related_name="goal_user", on_delete=models.CASCADE, db_index=True
    )

    # Fields set to be optional
    metrics = models.JSONField(null=True, blank=True)  # To store an array of metrics
    progress = models.FloatField(null=True, blank=True)
    milestones = models.JSONField(
        null=True, blank=True
    )  # Assuming milestones are a list of objects

    video = models.FileField(
        upload_to="videos_uploaded",
        null=True,
        blank=True,  # Allow both null and blank for FileField
        validators=[
            FileExtensionValidator(
                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
            ),
            validate_file_size,
        ],
    )
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
        ("group", "Group"),
    ]
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="private"
    )
