from django.db import models

# Create your models here.

class BannerUpdate(models.Model):
    banner_image    = models.ImageField(blank = True,upload_to = 'banner_images')
    banner_name     = models.CharField(max_length=50)
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    is_active       = models.BooleanField()
    created_at      = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return self.banner_name
