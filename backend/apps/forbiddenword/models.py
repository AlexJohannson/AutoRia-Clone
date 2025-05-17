from django.db import models


class Forbiddenwords(models.Model):
    class Meta:
        db_table = 'forbidden_words'

    word = models.CharField(max_length=200, unique=True)


