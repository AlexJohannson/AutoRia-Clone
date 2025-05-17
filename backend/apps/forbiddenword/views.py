from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.forbiddenword.models import Forbiddenwords
from apps.forbiddenword.permissions import IsAdminOrSuperuser
from apps.forbiddenword.serializers import ForbiddenWordSerializer


class ForbiddenWordsCreateApiView(ListCreateAPIView):
    queryset = Forbiddenwords.objects.all()
    serializer_class = ForbiddenWordSerializer
    permission_classes = [IsAdminOrSuperuser]


class ForbiddenWordsUpdateRetrieveDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Forbiddenwords.objects.all()
    serializer_class = ForbiddenWordSerializer
    permission_classes = [IsAdminOrSuperuser]