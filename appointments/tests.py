from django.test import TestCase
from django.contrib.auth.models import User

from .testutils import RestApiClient
from .models import Range, Appointment


class ClientApiTest(TestCase):

    def setUp(self):
        self.api_client = RestApiClient(
            self.client, '/api/v1/')
        self.user = User.objects.create_user(
            'test_user', 'test_user@example.com', 'test_user')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.user.username,
                          password='test_user')

    def test_appointments_get(self):
        response = self.api_client.get('appointments')
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(response.content_json['meta']['total_count'], 0)
        self.assertEqual(response.content_json['objects'], [])

        range1 = Range.objects.create(
            date='2017-04-19',
            start_time='09:00:00',
            end_time='10:00:00')

        range2 = Range.objects.create(
            date='2017-04-20',
            start_time='08:00:00',
            end_time='09:00:00')

        app = Appointment.objects.create(
            name='Testing appointment',
            description='Custom description',
            add_info='Additional information')

        app.ranges.add(range1, range2)

        response = self.api_client.get('appointments')
        self.assertEqual(response.content_json['objects'], [
            {
                u'id': app.pk,
                u'name': app.name,
                u'description': app.description,
                u'add_info': app.add_info,
                u'ranges': [
                    {u'id': range1.pk, u'date': range1.date, u'start_time': range1.start_time,
                        u'end_time': range1.end_time, u'resource_uri': u'/api/v1/ranges/%d/' % range1.pk},
                    {u'id': range2.pk, u'date': range2.date, u'start_time': range2.start_time,
                        u'end_time': range2.end_time, u'resource_uri': u'/api/v1/ranges/%d/' % range2.pk}
                ],
                u'resource_uri': u'/api/v1/appointments/%d/' % app.pk,
            }
        ])

    def test_appointments_post(self):

        response = self.api_client.post('ranges', {
            'date': '2017-04-15',
            'start_time': '15:00:00',
            'end_time': '16:00:00',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Range.objects.count(), 1)

        response = self.api_client.get('ranges')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_json['objects'], [
            {
                u'id': 3,
                u'date': u'2017-04-15',
                u'start_time': u'15:00:00',
                u'end_time': u'16:00:00',
                u'resource_uri': u'/api/v1/ranges/3/'
            }
        ])

        response = self.api_client.post('appointments', {
            'name': 'Test Appointment',
            'description': 'Test Description',
            'add_info': 'Test Additional info',
            'ranges': ["/api/v1/ranges/3/"]
        })
        self.assertEqual(response.status_code, 201, msg=response.content)
        self.assertEqual(Appointment.objects.count(), 1)

        response = self.api_client.get('appointments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_json['objects'], [
            {
                u'id': 2,
                u'name': u'Test Appointment',
                u'description': u'Test Description',
                u'add_info': u'Test Additional info',
                u'resource_uri': u'/api/v1/appointments/2/',
                u'ranges': [
                    {
                        u'id': 3,
                        u'date': u'2017-04-15',
                        u'start_time': u'15:00:00',                    
                        u'end_time': u'16:00:00',
                        u'resource_uri': u'/api/v1/ranges/3/'
                    }
                ]
		    }
		])
