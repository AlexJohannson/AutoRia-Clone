from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.chat.models import ChatRoomModel
from apps.user.models import ProfileModel, UserModel


class ChatApiIntegrationTest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@test.com',
            password='password',
            is_active=True
        )

        ProfileModel.objects.create(
            user=self.user,
            name='User',
            surname='Test',
            age=30,
            house=1,
            street='Street',
            city='City',
            region='Region',
            country='Country',
            gender='Male'
        )

        self.other_user = UserModel.objects.create_user(
            email='other@test.com',
            password='password',
            is_active=True
        )

        ProfileModel.objects.create(
            user=self.other_user,
            name='Other',
            surname='User',
            age=25,
            house=2,
            street='Street',
            city='City',
            region='Region',
            country='Country',
            gender='Female'
        )

    def create_chat_room(self, participants):
        room = ChatRoomModel.objects.create(name='Test Room')
        for user in participants:
            room.messages.create(user=user, text='Hello')
        return room

    def test_chat_room_list_as_participant(self):
        chat_room = self.create_chat_room([self.user, self.other_user])

        self.client.force_authenticate(user=self.user)
        url = reverse('chat-room-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('data', response.data)
        self.assertIsInstance(response.data['data'], list)
        self.assertGreater(len(response.data['data']), 0)
        self.assertEqual(response.data['data'][0]['name'], chat_room.name)


    def test_chat_room_list_as_non_participant(self):
        self.create_chat_room([self.user, self.other_user])

        new_user = UserModel.objects.create_user(
            email='new@test.com',
            password='password',
            is_active=True
        )

        ProfileModel.objects.create(
            user=new_user,
            name='New',
            surname='User',
            age=28,
            house=4,
            street='New',
            city='City',
            region='Region',
            country='Country',
            gender='Female'
        )

        self.client.force_authenticate(user=new_user)
        url = reverse('chat-room-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('data', response.data)
        self.assertIsInstance(response.data['data'], list)
        self.assertEqual(len(response.data['data']), 0)

    def test_chat_room_detail_as_participant(self):
        chat_room = self.create_chat_room([self.user, self.other_user])

        self.client.force_authenticate(user=self.user)
        url = reverse('chat-room-detail', kwargs={'pk': chat_room.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('room_id', response.data)
        self.assertIn('room_name', response.data)
        self.assertIn('messages', response.data)
        self.assertEqual(response.data['room_name'], chat_room.name)
        self.assertTrue(isinstance(response.data['messages'], list))
        self.assertGreater(len(response.data['messages']), 0)

    def test_chat_room_detail_as_non_participant(self):
        chat_room = self.create_chat_room([self.user, self.other_user])

        new_user = UserModel.objects.create_user(
            email='new2@test.com',
            password='password',
            is_active=True
        )

        ProfileModel.objects.create(
            user=new_user,
            name='New2',
            surname='User',
            age=29,
            house=5,
            street='New2',
            city='City',
            region='Region',
            country='Country',
            gender='Male'
        )

        self.client.force_authenticate(user=new_user)
        url = reverse('chat-room-detail', kwargs={'pk': chat_room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_chat_room_as_participant(self):
        chat_room = self.create_chat_room([self.user, self.other_user])

        self.client.force_authenticate(user=self.user)
        url = reverse('chat-room-delete', kwargs={'pk': chat_room.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ChatRoomModel.DoesNotExist):
            ChatRoomModel.objects.get(pk=chat_room.id)

    def test_delete_chat_room_as_non_participant(self):
        chat_room = self.create_chat_room([self.user, self.other_user])

        new_user = UserModel.objects.create_user(
            email='new3@test.com',
            password='password',
            is_active=True
        )

        ProfileModel.objects.create(
            user=new_user,
            name='New3',
            surname='User',
            age=27,
            house=6,
            street='New3',
            city='City',
            region='Region',
            country='Country',
            gender='Female'
        )

        self.client.force_authenticate(user=new_user)
        url = reverse('chat-room-delete', kwargs={'pk': chat_room.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





