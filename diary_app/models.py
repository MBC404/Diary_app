from django.db import models
from django.contrib.auth.models import User
import bcrypt

class DiaryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin_hash = models.CharField(max_length=128, blank=True, null=True)

    def set_pin(self, raw_pin: str):
        # raw_pin is a 4-digit string
        hashed = bcrypt.hashpw(raw_pin.encode(), bcrypt.gensalt())
        self.pin_hash = hashed.decode()

    def check_pin(self, raw_pin: str) -> bool:
        if not self.pin_hash:
            return False
        return bcrypt.checkpw(raw_pin.encode(), self.pin_hash.encode())

    def __str__(self):
        return f"DiaryProfile({self.user.username})"


class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.created_at})"
