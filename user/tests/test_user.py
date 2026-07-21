from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import UserProfile

User = get_user_model()

class SignupViewTests(TestCase):
    # تست ثبت نام
    def test_sign_up(self):
        response = self.client.post(
            "/user/signup/",
            {
                "email": "testt@gmail.com",
                "password": "testtesttesttest",
                "confirm_password" : "testtesttesttest"
            }
        )

        self.assertEqual(response.status_code, 302)

class LoginViewTests(TestCase):
    # تست لاگین
    def setUp(self):
        User.objects.create_user(email="testt@gmail.com" , username="testtest" , password="testtesttesttest")
        User

    def test_login(self):
        response = self.client.post(
            "/user/login/",
            {
                "email": "testt@gmail.com",
                "password": "testtesttesttest"
            }
        )

        self.assertEqual(response.status_code, 302)

class ChangePasswordViewTests(TestCase):
    # تست تغییر رمز عبور
    def setUp(self):
        User.objects.create_user(email="testt@gmail.com" , username="testtest" , password="testtesttesttest")

        self.client.post(
                    "/user/login/",
                    {
                        "email": "testt@gmail.com",
                        "password": "testtesttesttest"
                    }
                )

    def test_change_password(self):
        response = self.client.post(
                    "/user/change-password/",
                    {
                        "old_password" : "testtesttesttest",
                        "new_password" : "testtesttesttest2",
                        "confirm_password" : "testtesttesttest2"
                    }
                )
        
        self.assertEqual(response.status_code, 302)

class ChangeInfoViewTests(TestCase):
    # تست تغییر اطلاعات
    def setUp(self):
        User.objects.create_user(email="testt@gmail.com" , username="testtest" , password="testtesttesttest")

        self.client.post(
                    "/user/login/",
                    {
                        "email": "testt@gmail.com",
                        "password": "testtesttesttest"
                    }
                )

    def test_change_info(self):
        response = self.client.post(
                    "/user/edit/",
                    {
                        "avatar": "2",
                        "username" : "testtest2",
                        "school_name" : "مدرسه تستی",
                        "grade" : "هشتم"
                    }
                )
        
        self.assertEqual(response.status_code, 302)

class DeleteAccountViewTests(TestCase):
    # تست حذف حساب کاربری
    def setUp(self):
        User.objects.create_user(email="testt@gmail.com" , username="testtest" , password="testtesttesttest")

        self.client.post(
                    "/user/login/",
                    {
                        "email": "testt@gmail.com",
                        "password": "testtesttesttest"
                    }
                )

    def test_delete_account(self):
        response = self.client.post(
            "/user/delete/",
            {
                "reason": "تست",
            }
        )

        self.assertEqual(response.status_code, 302)
