from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{ self.user.username }'

    def save(self, *args, **kwargs):
        # 1. Save the Profile object first, including the image file itself.
        super().save(*args, **kwargs)

        # 2. Open the image using the filesystem PATH, not the URL.
        img = Image.open(self.image.path)

        # 3. Perform resizing logic
        if img.height > 300 or img.width > 300:  # Use 'or' to check if *either* dimension is too large
            output_size = (300, 300)
            img.thumbnail(output_size)

            # 4. Save the resized image back to the same filesystem PATH.
            img.save(self.image.path)