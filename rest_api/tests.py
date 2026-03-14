from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class RestaurantsTestCase(TestCase):
    """
    Test Class for Testing GET Requests to a Django REST Framework RestaurantSearchView.
    Hits /api/v1/restaurants/search/ Endpoint
    """

    @classmethod
    def setUpTestData(cls):
        """
        Import the CSV File to Seed the Test Database
        """
        # Real world scenario, I would want to use fixtures instead. This is a sloppy way of loading data in Django
        call_command('load_restaurants', '--path=app/raw_data/restaurants.csv', verbosity=0)

    def setUp(self):
        """
        Initialize the API Client
        """
        self.client = APIClient()

    def test_get_request_1(self):
        """
        Test Successful GET Request to the Search Restaurant Endpoint.
        Saturday 10:30 (10:30am) - Expected 4 Results
        """
        expected = [
            'Dashi',
            'Mandolin',
            'Mez Mexican',
            'Tupelo Honey'
        ]
        url = reverse('restaurant-search', query={'datetime': '2026-02-14 10:30'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert Response Data Structure
        self.assertIn('count', data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

        # Assert Expectations
        self.assertEqual(data['count'], 4)
        self.assertEqual(data['datetime'], '2026-02-14 10:30')
        self.assertIsInstance(data['open_restaurants'], list)
        self.assertEqual(len(data['open_restaurants']), 4)

        for restaurant in data['open_restaurants']:
            self.assertIn(restaurant, expected)

    def test_get_request_2(self):
        """
        Test Successful GET Request to the Search Restaurant Endpoint.
        Saturday 15:30 (3:30pm) - Expected 37 Results
        """
        expected = [
            "42nd Street Oyster Bar",
            "Bida Manda",
            "Brewery Bhavana",
            "Caffe Luna",
            "Centro",
            "Char Grill",
            "Crawford and Son",
            "Dashi",
            "David's Dumpling",
            "El Rodeo",
            "Garland",
            "Glenwood Grill",
            "Gravy",
            "Gringo a Gogo",
            "Jose and Sons",
            "Mami Nora's",
            "Mandolin",
            "Mez Mexican",
            "Morgan St Food Hall",
            "Neomonde",
            "Oakleaf",
            "Page Road Grill",
            "Player's Retreat",
            "Provence",
            "Saltbox",
            "Second Empire",
            "Seoul 116",
            "Sitti",
            "Stanbury",
            "Taverna Agora",
            "Tazza Kitchen",
            "The Cheesecake Factory",
            "The Cowfish Sushi Burger Bar",
            "Top of the Hill",
            "Tupelo Honey",
            "Whiskey Kitchen",
            "Yard House"
        ]
        url = reverse('restaurant-search', query={'datetime': '2026-02-14 15:30'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert Response Data Structure
        self.assertIn('count', data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

        # Assert Expectations
        self.assertEqual(data['count'], 37)
        self.assertEqual(data['datetime'], '2026-02-14 15:30')
        self.assertIsInstance(data['open_restaurants'], list)
        self.assertEqual(len(data['open_restaurants']), 37)

        for restaurant in data['open_restaurants']:
            self.assertIn(restaurant, expected)

    def test_get_request_3(self):
        """
        Test Successful GET Request to the Search Restaurant Endpoint.
        Saturday 23:30 (11:30pm) - Expected 7 Results
        """
        expected = [
            "42nd Street Oyster Bar",
            "Bonchon",
            "Caffe Luna",
            "Seoul 116",
            "Stanbury",
            "Taverna Agora",
            "The Cheesecake Factory"
        ]
        url = reverse('restaurant-search', query={'datetime': '2026-02-14 23:30'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert Response Data Structure
        self.assertIn('count', data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

        # Assert Expectations
        self.assertEqual(data['count'], 7)
        self.assertEqual(data['datetime'], '2026-02-14 23:30')
        self.assertIsInstance(data['open_restaurants'], list)
        self.assertEqual(len(data['open_restaurants']), 7)

        for restaurant in data['open_restaurants']:
            self.assertIn(restaurant, expected)

    def test_get_request_4(self):
        """
        Test Successful GET Request to the Search Restaurant Endpoint.
        Thursday 5:30 (5:30am) - Expected Zero Results, Nothing Open
        """
        url = reverse('restaurant-search', query={'datetime': '2026-02-12 5:30'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert Response Data Structure
        self.assertIn('count', data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

        # Assert Expectations
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['datetime'], '2026-02-12 5:30')
        self.assertIsInstance(data['open_restaurants'], list)
        self.assertEqual(len(data['open_restaurants']), 0)

    def test_get_request_5(self):
        """
        Test Successful GET Request to the Search Restaurant Endpoint.
        Sunday 0:25 (12:25am - Midnight) - Expected 3 Results
        """
        expected = [
            "Bonchon",
            "Seoul 116",
            "The Cheesecake Factory"
        ]
        url = reverse('restaurant-search', query={'datetime': '2026-02-15 0:25'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert Response Data Structure
        self.assertIn('count', data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

        # Assert Expectations
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['datetime'], '2026-02-15 0:25')
        self.assertIsInstance(data['open_restaurants'], list)
        self.assertEqual(len(data['open_restaurants']), 3)

        for restaurant in data['open_restaurants']:
            self.assertIn(restaurant, expected)

    def test_get_request_no_parameter(self):
        """
        Test Failed GET Request to the Search Restaurant Endpoint.
        """
        url = reverse('restaurant-search')
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert Response Data Structure
        self.assertIn('Error', data)

        # Assert Expectations
        self.assertEqual(data['Error'], 'datetime Parameter Required')

    def test_get_request_invalid_parameter(self):
        """
        Test Failed GET Request to the Search Restaurant Endpoint. Invalid Parameter Entered
        """
        url = reverse('restaurant-search', query={'datetime': 'alf-02-15 0:25'})
        response = self.client.get(url)
        data = response.json()

        # Assert Response Status Code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert Response Data Structure
        self.assertIn('Error', data)

        # Assert Expectations
        self.assertEqual(data['Error'], 'Invalid datetime Format: Unable to Parse datetime String: alf-02-15 0:25')
