from django.db import models


class TheBlog(models.Model):
    title = models.CharField(max_length=120, blank=False)
    content = models.TextField(blank=False)
    author = models.TextField(blank=False)
    
    def __str__(self):
        return self.title