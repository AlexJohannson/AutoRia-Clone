from django.test import TestCase

from apps.forbiddenword.models import Forbiddenwords
from apps.forbiddenword.serializers import ForbiddenWordSerializer


class ForbiddenWordSerializerTest(TestCase):
    def setUp(self):
        self.word_data = {'word': 'badword'}

    def test_serialization(self):
        word = Forbiddenwords.objects.create(**self.word_data)
        serializer = ForbiddenWordSerializer(word)
        expected_data = {
            'id': word.id,
            'word': 'badword',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization_valid(self):
        serializer = ForbiddenWordSerializer(data=self.word_data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.word, 'badword')

    def test_deserialization_invalid_empty(self):
        serializer = ForbiddenWordSerializer(data={'word': ''})
        self.assertFalse(serializer.is_valid())
        self.assertIn('word', serializer.errors)
