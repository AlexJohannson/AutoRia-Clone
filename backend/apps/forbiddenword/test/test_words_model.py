from django.db import IntegrityError
from django.test import TestCase

from apps.forbiddenword.models import Forbiddenwords


class ForbiddenwordsModelTest(TestCase):
    def setUp(self):
        self.word_text = "badword"

    def test_create_forbidden_word(self):
        word = Forbiddenwords.objects.create(word=self.word_text)
        self.assertEqual(word.word, self.word_text)

    def test_unique_constraint_on_word(self):
        Forbiddenwords.objects.create(word=self.word_text)
        with self.assertRaises(IntegrityError):
            Forbiddenwords.objects.create(word=self.word_text)
