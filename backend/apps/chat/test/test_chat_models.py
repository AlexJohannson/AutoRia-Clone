from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.chat.models import ChatRoomModel, MessageModel

User = get_user_model()

class ChatRoomModelTest(TestCase):
    def setUp(self):
        
        self.user1 = User.objects.create_user(email='user1', password='password1')
        self.user2 = User.objects.create_user(email='user2', password='password2')


        self.room = ChatRoomModel.objects.create(name='Test Room', is_private=True)

    def test_chat_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertTrue(self.room.is_private)
        self.assertEqual(str(self.room), 'Test Room')

    def test_add_users_to_room(self):
        self.room.users.add(self.user1, self.user2)
        self.assertIn(self.user1, self.room.users.all())
        self.assertIn(self.user2, self.room.users.all())
        self.assertEqual(self.room.users.count(), 2)

    def test_create_message_in_room(self):
        self.room.users.add(self.user1)

        message = MessageModel.objects.create(
            room=self.room,
            user=self.user1,
            text='Hello, this is a test message!',
            user_role='admin'
        )

        self.assertEqual(message.text, 'Hello, this is a test message!')
        self.assertEqual(message.user_role, 'admin')
        self.assertEqual(message.user, self.user1)
        self.assertEqual(message.room, self.room)

    def test_message_related_name(self):
        self.room.users.add(self.user1)

        message = MessageModel.objects.create(
            room=self.room,
            user=self.user1,
            text='Message for related name test',
            user_role='user'
        )

        self.assertIn(message, self.room.messages.all())
        self.assertIn(message, self.user1.messages.all())

    def test_many_to_many_relationship(self):
        self.room.users.add(self.user1)
        user_rooms = self.user1.chat_rooms.all()
        self.assertIn(self.room, user_rooms)
