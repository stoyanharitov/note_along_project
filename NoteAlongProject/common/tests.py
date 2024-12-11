from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils import timezone


from NoteAlongProject.accounts.models import Profile
from NoteAlongProject.events.models import Concert, Festival
from NoteAlongProject.posts.models import Post

UserModel = get_user_model()

class SearchResultsViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(
            user=self.user,
            age=25,
            city='New York',
            is_musician=True
        )
        self.client.login(username='testuser', password='password')
        self.naive_datetime = timezone.datetime(2025, 12, 15, 20, 0, 0)
        self.aware_datetime = timezone.make_aware(self.naive_datetime, timezone.get_current_timezone())

    def test_search_users_by_username__result_contains_search_parameters(self):
        UserModel.objects.create_user(username='musician', first_name='John', last_name='Doe')
        response = self.client.get(reverse_lazy('general-search') + '?query=musician&category=users')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'musician')

    def test_search_posts_by_title__result_contains_search_parameters(self):
        post = Post.objects.create(
            title='Rock Concert', content='Great music', author=self.user
        )
        response = self.client.get(reverse_lazy('general-search') + '?query=roc&category=posts')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rock Concert')

    def test_search_concerts_by_location__result_contains_search_parameters(self):
        concert = Concert.objects.create(
            title='Classical Night',
            description='A classical music event.',
            location='New York',
            date=self.aware_datetime + timezone.timedelta(days=1),
            musician=self.user
        )
        response = self.client.get(reverse_lazy('general-search') + '?query=w york&category=concerts')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Classical Night')

    def test_search_concerts_by_location__results_do_not_match_search_term(self):
        concert = Concert.objects.create(
            title='Classical Night',
            description='A classical music event.',
            location='New York',
            date=self.aware_datetime + timezone.timedelta(days=1),
            musician=self.user
        )

        response = self.client.get(reverse_lazy('general-search') + '?query=Los Angeles&category=concerts')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Classical Night')

    def test_search_no_results_when_there_are_zero_filter_matches__returns_conditional_html(self):
        response = self.client.get(reverse_lazy('general-search') + '?query=Jazz&category=concerts')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results found', status_code=200)