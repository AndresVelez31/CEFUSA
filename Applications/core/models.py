from django.db import models


class LandingPage(models.Model):
	"""Modelo que representa la configuración general de la página de aterrizaje."""
	title = models.CharField(max_length=200, default='Bienvenido a CEFUSA')
	subtitle = models.CharField(max_length=255, blank=True)
	background = models.ImageField(upload_to='landing/', blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Landing Page'
		verbose_name_plural = 'Landing Pages'

	def __str__(self):
		return f"LandingPage ({self.pk}) - {self.title}"


class LandingSlide(models.Model):
	SECTION_CHOICES = [
		('news', 'Noticias'),
		('tournaments', 'Torneos'),
		('matches', 'Partidos'),
	]

	page = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='slides')
	section = models.CharField(max_length=32, choices=SECTION_CHOICES, default='news')
	title = models.CharField(max_length=200, blank=True)
	subtitle = models.CharField(max_length=255, blank=True)
	content = models.TextField(blank=True)
	image = models.ImageField(upload_to='landing/slides/', blank=True, null=True)
	order = models.PositiveIntegerField(default=0)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['section', 'order']
		verbose_name = 'Landing Slide'
		verbose_name_plural = 'Landing Slides'

	def __str__(self):
		return f"{self.get_section_display()} - {self.title or 'Slide'} ({self.pk})"
