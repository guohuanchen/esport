"""
this file tests all functionality of the app.
"""
from django.test import TestCase
from django.utils import timezone
from .models import Signup, Reviews
from django.core.urlresolvers import reverse
import urlparse
# from mock import Mock, ANY
from django.conf import settings

# Create your tests here.

def create_signup(email, username, name, skype, mmr, server, hero, rating, reputation,
                  students, pricerate, coach_id):
    """
    setup.
    """
    return Signup.objects.create(email=email, username=username, name=name,
                                 mmr=mmr, server=server, skype=skype,
                                 hero=hero, rating=rating, reputation=reputation,
                                 students=students, pricerate=pricerate, id=coach_id)

class SignupMethodTests(TestCase):
    def test_list_of_coaches_with_no_users(self):
        """
        testing that there are no users in databse.
        """
        response = self.client.get(reverse('sideapp:list_of_coaches'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No coaches available.")
        self.assertQuerysetEqual(response.context['coaches'], [])

    def test_list_of_coaches_with_users(self):
        """
        testing that there are users in databse.
        """
        create_signup(email="testemail@mail.com", username="testbot", name="bot", mmr=123,
                      server="Europe", skype="mySkype" ,hero="myHero", rating=10, reputation=50,
                      students=20, pricerate=30, coach_id=2)
        response = self.client.get(reverse('sideapp:list_of_coaches'))
        self.assertQuerysetEqual(response.context['coaches'][0],
                                 ["u'testbot'", '123', "u'Europe'", "u'myHero'",
                                  '10', '50', '20', '30.0', '2'])

    # def test_tutorselected_with_no_user(self):
    #     """
    #     Testing website with no users.
    #     """
    #     response = self.client.get(reverse('sideapp:tutorselected', args=("testbot",)))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['coach'], [])

    def test_tutorselected_with_users(self):
        """
        Testing that the returned object is the expected one and the average is correct.
        """
        create_signup(email="testemail@mail.com", username="testbot", name="bot", mmr=123,
                      server="Europe", skype="mySkype" ,hero="myHero", rating=10, reputation=50,
                      students=20, pricerate=30, coach_id=5)
        response = self.client.get(reverse('sideapp:tutorselected', args=("testbot",)))
        self.assertEqual(response.context['coach'].username, "testbot")
        self.assertEqual(response.context['coach'].mmr, 123)
        self.assertEqual(response.context['coach'].id, 5)
        self.assertEqual(response.context['coach'].skype, "mySkype")
        self.assertEqual(response.context['final_avg_review'], 0)


# class testViews(TestCase):
#     def testHome(self):
#         response = self.client.get(reverse('sideapp:home'))
#         self.assertEqual(response.status_code, 200)

    # def testLogout(self):
    #     response = self.client.get(reverse('sideapp:logout'))
    #     self.assertEqual(response.status_code, 200)

    # def testContact(self):
    #     response = self.client.get(reverse('sideapp:contact'))
    #     self.assertEqual(response.status_code, 200)

    # def testSignup(self):
    #     response = self.client.get(reverse('sideapp:signup'))
    #     self.assertEqual(response.status_code, 200)

    # def testFindCoach(self):
    #     response = self.client.get(reverse('sideapp:findcoach'))
    #     self.assertEqual(response.status_code, 200)

    # def testListCoach(self):
    #     response = self.client.get(reverse('sideapp:list_of_coaches'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def testTutorSelect(self):
    #     response = self.client.get(reverse('sideapp:tutorselected'))
    #     self.assertEqual(response.status_code, 200)

# class testStripe(TestCase):
#     def test_making_a_donation_and_getting_the_callback(self):
#         """These two tests must live together because they need to be done sequentially.
#
#         First, we place a donation using the client. Then we send a mock callback to our
#         webhook, to make sure it accepts it properly.
#         """
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         # Create a stripe token (this would normally be done via javascript in the front
#         # end when the submit button was pressed)
#         token = stripe.Token.create(
#             card={
#                 'number': '4242424242424242',
#                 'exp_month': '6',
#                 'exp_year': str(datetime.today().year + 1),
#                 'cvc': '123',
#             }
#         )
#
#         # Place a donation as an anonymous (not logged in) person using the
#         # token we just got
#         r = self.client.post('/checkout/', data={
#             'first_name': 'Justin',
#             'last_name': 'Timberlake',
#             'address1': '1600 Pennsylvania Ave.',
#             'address2': 'The Whitehouse',
#             'city': 'DC',
#             'state': 'DC',
#             'zip_code': '20500',
#             'email': 'justin@timnberlake.org',
#             'referrer': 'footer',
#             'stripeToken': token.id,
#         })
