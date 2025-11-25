from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


User = get_user_model()


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True)
	website = models.URLField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Profile({self.user})"


class Plan(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title

	def get_absolute_url(self):
		return reverse('plan-detail', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			base = slugify(self.title)[:180]
			slug = base
			counter = 1
			while Plan.objects.filter(slug=slug).exists():
				slug = f"{base}-{counter}"
				counter += 1
			self.slug = slug
		super().save(*args, **kwargs)


# Signals: create Profile automatically when a new user is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	else:
		# ensure profile exists; if user created elsewhere without signal, this avoids crashes
		Profile.objects.get_or_create(user=instance)
