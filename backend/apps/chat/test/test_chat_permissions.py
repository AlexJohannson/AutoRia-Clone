from unittest import TestCase
from unittest.mock import MagicMock

from apps.chat.permissions import IsMessageOwnerOrAdmin, IsParticipantOrAdmin


class TestPermissions(TestCase):

    def setUp(self):
        self.participant_permission = IsParticipantOrAdmin()
        self.message_owner_permission = IsMessageOwnerOrAdmin()


    def test_participant_user_is_staff(self):
        mock_user = MagicMock(is_staff=True, is_superuser=False)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock()

        self.assertTrue(self.participant_permission.has_object_permission(mock_request, None, mock_obj))

    def test_participant_user_is_superuser(self):
        mock_user = MagicMock(is_staff=False, is_superuser=True)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock()

        self.assertTrue(self.participant_permission.has_object_permission(mock_request, None, mock_obj))

    def test_participant_user_is_participant(self):
        mock_user = MagicMock(is_staff=False, is_superuser=False)
        mock_request = MagicMock(user=mock_user)

        mock_messages = MagicMock()
        mock_messages.filter.return_value.exists.return_value = True

        mock_obj = MagicMock(messages=mock_messages)

        self.assertTrue(self.participant_permission.has_object_permission(mock_request, None, mock_obj))
        mock_messages.filter.assert_called_with(user=mock_user)

    def test_participant_user_is_not_participant(self):
        mock_user = MagicMock(is_staff=False, is_superuser=False)
        mock_request = MagicMock(user=mock_user)

        mock_messages = MagicMock()
        mock_messages.filter.return_value.exists.return_value = False

        mock_obj = MagicMock(messages=mock_messages)

        self.assertFalse(self.participant_permission.has_object_permission(mock_request, None, mock_obj))
        mock_messages.filter.assert_called_with(user=mock_user)


    def test_message_user_is_staff(self):
        mock_user = MagicMock(is_staff=True, is_superuser=False)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock(user=MagicMock())

        self.assertTrue(self.message_owner_permission.has_object_permission(mock_request, None, mock_obj))

    def test_message_user_is_superuser(self):
        mock_user = MagicMock(is_staff=False, is_superuser=True)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock(user=MagicMock())

        self.assertTrue(self.message_owner_permission.has_object_permission(mock_request, None, mock_obj))

    def test_message_user_is_owner(self):
        mock_user = MagicMock(is_staff=False, is_superuser=False)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock(user=mock_user)

        self.assertTrue(self.message_owner_permission.has_object_permission(mock_request, None, mock_obj))

    def test_message_user_is_not_owner(self):
        mock_user = MagicMock(is_staff=False, is_superuser=False)
        mock_request = MagicMock(user=mock_user)
        mock_obj = MagicMock(user=MagicMock())

        self.assertFalse(self.message_owner_permission.has_object_permission(mock_request, None, mock_obj))



