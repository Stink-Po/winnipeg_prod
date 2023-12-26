from django.db import models


class OurProjects(models.Model):
    class TitleChoices(models.TextChoices):
        DUCT_CLEANING = "DC", "Duct Cleaning"
        FURNACE_INSTALLATION = "FI", "Furnace Installation"
        FURNACE_REPAIR = "FR", "Furnace Repair"
        FURNACE_CLEANING = "FC", "Furnace Cleaning"
        AIR_CONDITIONER_INSTALLATION = "AI", "Air Conditioner Installation"
        AIR_CONDITIONER_TUNE_UP = "AR", "Air Conditioner Tune Up"

    image = models.ImageField(upload_to="projects_images", null=True, blank=True)
    title = models.CharField(max_length=2, choices=TitleChoices)
    completed_at = models.DateTimeField(auto_now_add=True)

    def get_friendly_title(self):
        title_mapping = {
            'DC': 'Duct Cleaning',
            'FI': 'Furnace Installation',
            'FR': 'Furnace Repair',
            'FC': 'Furnace Cleaning',
            'AI': 'Air Conditioner Installation',
            'AR': 'Air Conditioner Tune Up',
        }
        return title_mapping.get(self.title, "")

    def __str__(self):
        return self.get_title_display()
