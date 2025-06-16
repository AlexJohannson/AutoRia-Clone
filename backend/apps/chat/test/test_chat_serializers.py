from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.chat.models import ChatRoomModel, MessageModel
from apps.chat.serializers import ChatRoomSerializer, MessageSerializer
from apps.user.models import ProfileModel

User = get_user_model()

class ChatSerializersTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password1',
            is_active=True
        )

        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password2',
            is_active=True
        )


        ProfileModel.objects.create(
            user=self.user1,
            name='User One',
            surname='Test',
            age=25,
            house=1,
            street='Test Street',
            city='Test City',
            region='Test Region',
            country='Test Country',
            gender='Male'
        )

        ProfileModel.objects.create(
            user=self.user2,
            name='User Two',
            surname='Test',
            age=30,
            house=2,
            street='Test Street',
            city='Test City',
            region='Test Region',
            country='Test Country',
            gender='Female'
        )

        self.room = ChatRoomModel.objects.create(name='Test Room')
        self.room.users.add(self.user1, self.user2)

        self.message1 = MessageModel.objects.create(
            room=self.room,
            user=self.user1,
            text='First message',
            user_role='admin'
        )

        self.message2 = MessageModel.objects.create(
            room=self.room,
            user=self.user2,
            text='Second message',
            user_role='user'
        )

    def test_message_serializer_output(self):
        serializer = MessageSerializer(self.message1)
        serialized_data = serializer.data

        expected_data = {
            'id': self.message1.id,
            'text': 'First message',
            'user_role': 'admin',
            'room': self.room.id
        }

        self.assertEqual(serialized_data['id'], expected_data['id'])
        self.assertEqual(serialized_data['text'], expected_data['text'])
        self.assertEqual(serialized_data['user_role'], expected_data['user_role'])
        self.assertEqual(serialized_data['room'], expected_data['room'])
        self.assertNotIn('user_name', serialized_data)

    def test_chat_room_serializer_output(self):
        serializer = ChatRoomSerializer(instance=self.room)
        data = serializer.data

        self.assertEqual(data['id'], self.room.id)
        self.assertEqual(data['name'], self.room.name)

        expected_participants = [
            {'name': 'User One', 'role': 'admin'},
            {'name': 'User Two', 'role': 'user'},
        ]

        serialized_participants = sorted(data['participants'], key=lambda x: x['name'])
        expected_participants = sorted(expected_participants, key=lambda x: x['name'])

        self.assertEqual(serialized_participants, expected_participants)

    def test_chat_room_serializer_participants_empty(self):
        empty_room = ChatRoomModel.objects.create(name='Empty Room')
        serializer = ChatRoomSerializer(instance=empty_room)
        self.assertEqual(serializer.data['participants'], [])

    def test_message_serializer_read_only_fields(self):
        serializer = MessageSerializer(data={
            'text': 'Attempted message',
            'user_name': 'Fake Name',
            'user_role': 'Fake Role',
            'room': self.room.id
        })
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertNotIn('user_name', validated_data)
        self.assertNotIn('user_role', validated_data)
