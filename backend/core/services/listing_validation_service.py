from apps.forbiddenword.models import Forbiddenwords


def contains_forbidden_word(text):
    forbidden_words = Forbiddenwords.objects.values_list('word', flat=True)

    for word in forbidden_words:
        if word.lower() in text.lower():
            return True

    return False


