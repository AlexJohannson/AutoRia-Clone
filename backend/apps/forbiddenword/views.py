from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.forbiddenword.models import Forbiddenwords
from apps.forbiddenword.permissions import IsAdminOrSuperuser
from apps.forbiddenword.serializers import ForbiddenWordSerializer


class ForbiddenWordsCreateApiView(ListCreateAPIView):
    """
        get:
            get all forbidden words list
        post:
            create new forbidden words
    """

    queryset = Forbiddenwords.objects.all()
    serializer_class = ForbiddenWordSerializer
    permission_classes = [IsAdminOrSuperuser]


class ForbiddenWordsUpdateRetrieveDestroyApiView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get forbidden words detail by id
        put:
            full update forbidden words detail by id
        patch:
            partial update forbidden words detail by id
        delete:
            delete forbidden words detail by id
    """

    queryset = Forbiddenwords.objects.all()
    serializer_class = ForbiddenWordSerializer
    permission_classes = [IsAdminOrSuperuser]