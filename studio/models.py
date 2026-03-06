from django.db import models


class Episode(models.Model):
    MODE_PODCAST = "podcast"
    MODE_VIDEO = "video"
    MODE_CHOICES = [
        (MODE_PODCAST, "Podcast"),
        (MODE_VIDEO, "Video"),
    ]

    title = models.CharField(max_length=200)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    script = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Section(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("episode", "name")
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.episode.title} - {self.name}"


class Question(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    position = models.PositiveIntegerField(default=1)
    section = models.CharField(max_length=120, default="عام")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self) -> str:
        return f"{self.episode.title} - {self.position}"
