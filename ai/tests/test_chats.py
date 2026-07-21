from django.test import TestCase
from django.contrib.auth import get_user_model
import uuid

from ai.models import Chat, Message, Memory
from ai.repositories.chat_repository import (
    create_new_chat,
    get_chat_by_uuid,
    add_to_memory,
    get_memory_context,
    create_new_message,
    delete_chat_by_uuid,
    get_chat_messages,
)

User = get_user_model()


class ChatRepositoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="hossein",
            email="hossein@test.com",
            password="password123"
        )

        chat_uuid = uuid.uuid4()

        cls.chat = Chat.objects.create(
            user=cls.user,
            uuid=chat_uuid
        )

    # تست ایجاد گفتگوی جدید
    def test_create_new_chat(self):

        chat = create_new_chat(self.user.username)

        self.assertIsNotNone(chat)
        self.assertEqual(chat.user, self.user)

    # تست ایجاد گفتگو برای کاربر نامعتبر
    def test_create_new_chat_invalid_user(self):

        chat = create_new_chat("unknown")

        self.assertIsNone(chat)

    # تست دریافت گفتگو با شناسه
    def test_get_chat_by_uuid(self):

        chat = get_chat_by_uuid(
            self.user.username,
            self.chat.uuid
        )

        self.assertEqual(chat.id, self.chat.id)

    # تست دریافت گفتگوی نامعتبر
    def test_get_invalid_chat(self):

        chat = get_chat_by_uuid(
            self.user.username,
            "invalid"
        )

        self.assertIsNone(chat)

    # تست افزودن پیام به حافظه
    def test_add_to_memory(self):

        message = Message.objects.create(
            chat=self.chat,
            text="سلام",
            is_ai=False
        )

        add_to_memory(self.user, message)

        memory = Memory.objects.get(user=self.user)

        self.assertEqual(
            memory.context.count(),
            1
        )

    # تست جلوگیری از ثبت پیام تکراری
    def test_duplicate_memory(self):

        message = Message.objects.create(
            chat=self.chat,
            text="سلام",
            is_ai=False
        )

        add_to_memory(self.user, message)
        add_to_memory(self.user, message)

        memory = Memory.objects.get(user=self.user)

        self.assertEqual(
            memory.context.count(),
            1
        )

    # تست دریافت متن حافظه
    def test_get_memory_context(self):

        message = Message.objects.create(
            chat=self.chat,
            text="سلام",
            is_ai=False
        )

        add_to_memory(self.user, message)

        context = get_memory_context(
            self.user.username
        )

        self.assertIn(
            "سلام",
            context
        )

    # تست ساخت پیام جدید
    def test_create_new_message(self):

        message = create_new_message(
            self.chat.uuid,
            False,
            "تست"
        )

        self.assertIsNotNone(message)

        self.assertEqual(
            message.text,
            "تست"
        )

    # تست حذف گفتگو
    def test_delete_chat(self):

        delete_chat_by_uuid(
            self.user.username,
            self.chat.uuid
        )

        self.assertFalse(
            Chat.objects.filter(
                id=self.chat.id
            ).exists()
        )

    # تست دریافت پیام‌های گفتگو
    def test_get_chat_messages(self):

        Message.objects.create(
            chat=self.chat,
            text="اول",
            is_ai=False
        )

        Message.objects.create(
            chat=self.chat,
            text="دوم",
            is_ai=True
        )

        messages = get_chat_messages(
            self.chat.uuid
        )

        self.assertEqual(
            len(messages),
            2
        )

        self.assertEqual(
            messages[0].text,
            "اول"
        )

        self.assertEqual(
            messages[1].text,
            "دوم"
        )