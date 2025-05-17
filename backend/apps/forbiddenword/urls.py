from django.urls import path

from apps.forbiddenword.views import ForbiddenWordsCreateApiView, ForbiddenWordsUpdateRetrieveDestroyApiView

urlpatterns = [
    path('', ForbiddenWordsCreateApiView.as_view(), name='forbidden_word-create'),
    path('/<int:pk>', ForbiddenWordsUpdateRetrieveDestroyApiView.as_view(), name='forbidden_word-retrieve'),
]