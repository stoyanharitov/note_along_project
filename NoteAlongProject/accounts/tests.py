from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group
from .models import Profile

UserModel = get_user_model()


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='musician', password='password')
        self.profile = Profile.objects.create(
            user=self.user,
            age=25,
            city='Sofia',
            is_musician=True
        )
        self.musician_group = Group.objects.get(name='Musician_admin')

    def test_musician_group_assignment__assigns_proper_admin_group_and_makes_a_staff_member(self):
        self.assertIn(self.musician_group, self.user.groups.all())
        self.assertTrue(self.user.is_staff)

    def test_save_profile_is_musician_removal__removes_admin_group_and_makes_is_staff_false(self):
        self.profile.is_musician = False
        self.profile.save()

        self.assertNotIn(self.musician_group, self.user.groups.all())
        self.assertFalse(self.user.is_staff)