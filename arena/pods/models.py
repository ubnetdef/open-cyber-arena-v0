from django.db import models

from arena.pods import utils


class Pod(models.Model):
    # VMware MOID without leading 'group-v'
    folder_id = models.IntegerField()
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.name} (group-v{self.folder_id})'

    def save(self, *args, **kwargs):
        folder = utils.get_folder(self.folder_id)
        self.name = folder.name
        return super().save(*args, **kwargs)
