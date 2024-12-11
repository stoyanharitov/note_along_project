from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from NoteAlongProject.accounts.models import Profile, Genre
from NoteAlongProject.events.models import Concert


UserModel = get_user_model()



class ConcertsDashboardViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(
            user=self.user,
            age=25,
            city='Sofia',
            is_musician=True
        )

        self.genre_rock = Genre.objects.create(name='Rockzz')
        self.genre_jazz = Genre.objects.create(name='Jazzzzz')

        self.naive_datetime = timezone.datetime(2025, 12, 15, 20, 0, 0)
        self.aware_datetime = timezone.make_aware(self.naive_datetime, timezone.get_current_timezone())

        self.profile.music_genre_preferences.add(self.genre_rock)
        self.future_concert = Concert.objects.create(
            title='Rock Night',
            location='Sozopol',
            date=self.aware_datetime + timezone.timedelta(days=1),
            musician=self.user
        )

        self.future_concert.genres.add(self.genre_rock)
        self.url = reverse_lazy('concert-dashboard')

    def test_concerts_dashboard_view_not_authenticated__redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse_lazy("login")}?next={self.url}')

    def test_get_context_data_user_profile__should_in_the_context(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)

        # Check if profile is included in the context
        self.assertIn('profile', response.context)
        self.assertEqual(response.context['profile'], self.profile)

    def test_empty_concerts_for_non_matching_genre__returns_conditional_html_template(self):
        self.profile.music_genre_preferences.clear()
        self.client.login(username='testuser', password='password')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No concerts match")

    def test_non_musician_creating_a_concert__raises_validation_error(self):
        self.user2 = UserModel.objects.create_user(username='testuser2', password='password2')
        self.profile2 = Profile.objects.create(
            user=self.user2,
            age=25,
            city='Sofia',
            is_musician=False
        )
        self.client.login(username='testuser2', password='password2')

        with self.assertRaises(ValidationError) as vae:
            self.future_concert = Concert.objects.create(
                title='Lo-fi fun',
                location='Atina',
                date=self.aware_datetime + timezone.timedelta(days=1),
                musician=self.user2
            )

        self.assertEqual(str(vae.exception), '["The user \'testuser2\' is not a musician."]')




