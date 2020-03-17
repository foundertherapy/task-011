from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import WorkingDetails, LeavingTime


class LoginTokenTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.check_in_url = reverse("check_in")
        self.check_out_url = reverse("check_out")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)

    def test_error_login_without_token(self):
        response = self.client.post(self.check_in_url)
        self.assertEqual(401, response.status_code)

    def test_success_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response = self.client.post(self.check_in_url)
        self.assertEqual(200, response.status_code)


class VacationCreateViewTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.vacation_url = reverse("vacation")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_success_vacation(self):
        response = self.client.post(self.vacation_url, {'vacation': 'True', 'date': '2020-03-17'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(WorkingDetails.objects.count(), 1)

    def test_error_vacation(self):
        response = self.client.post(self.vacation_url, {'vacation': 'False', 'date': '2020-03-17'})
        self.assertEqual(400, response.status_code)
        self.assertEqual(WorkingDetails.objects.count(), 0)


class WorkingDetailsAutoCheckTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.check_in_url = reverse("check_in")
        self.check_out_url = reverse("check_out")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_success_check(self):
        response = self.client.post(self.check_in_url)
        response2 = self.client.post(self.check_out_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response2.status_code)
        self.assertEqual(response.data['message'], 'check in done')
        self.assertEqual(response2.data['message'], 'check out done')
        self.assertEqual(WorkingDetails.objects.count(), 1)

    def test_double_check_in(self):
        response = self.client.post(self.check_in_url)
        response2 = self.client.post(self.check_in_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response2.status_code)
        self.assertEqual(response.data['message'], 'check in done')
        self.assertEqual(response2.data['message'], 'already checked in')
        self.assertEqual(WorkingDetails.objects.count(), 1)

    def test_check_out_without_check_in(self):
        response = self.client.post(self.check_out_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['message'], "User is not checked in")
        self.assertEqual(WorkingDetails.objects.count(), 0)

    def test_double_check_out(self):
        response = self.client.post(self.check_in_url)
        response2 = self.client.post(self.check_out_url)
        response3 = self.client.post(self.check_out_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response2.status_code)
        self.assertEqual(200, response3.status_code)
        self.assertEqual(response.data['message'], 'check in done')
        self.assertEqual(response2.data['message'], 'check out done')
        self.assertEqual(response3.data['message'], 'already checked out')
        self.assertEqual(WorkingDetails.objects.count(), 1)


class WorkingDetailsTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.check_url = reverse("check")
        self.list_url = reverse("all_hours")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)

    def test_success_check(self):
        response = self.client.post(self.check_url, {'check_in': '01:07:01', 'check_out': '03:07:01', 'date': '2020-03-7', 'vacation': 'False'})
        self.assertEqual(201, response.status_code)

    def test_error_range_check(self):
        response = self.client.post(self.check_url, {'check_in': '04:07:01', 'check_out': '03:07:01', 'date': '2020-03-7', 'vacation': 'False'})
        self.assertEqual(400, response.status_code)

    def test_error_double_check_same_date(self):
        response = self.client.post(self.check_url, {'check_in': '01:00:00', 'check_out': '02:00:00', 'date': '2020-03-7', 'vacation': 'True'})
        response2 = self.client.post(self.check_url, {'check_in': '03:00:00', 'check_out': '04:00:00', 'date': '2020-03-7', 'vacation': 'False'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)


class LeaveTimeCheckTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.check_url = reverse("leave")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_success_check(self):
        response = self.client.post(self.check_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-03-7'})
        self.assertEqual(201, response.status_code)

    def test_error_range_check(self):
        response = self.client.post(self.check_url, {'start': '04:00:00', 'end': '03:30:00', 'date': '2020-03-7'})
        self.assertEqual(400, response.status_code)

    def test_error_conflict_time(self):
        response = self.client.post(self.check_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-03-7'})
        response2 = self.client.post(self.check_url, {'start': '12:00:00', 'end': '01:30:00', 'date': '2020-03-7'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)

    def test_error_conflict_time_two(self):
        response = self.client.post(self.check_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-03-7'})
        response2 = self.client.post(self.check_url, {'start': '2:00:00', 'end': '04:00:00', 'date': '2020-03-7'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)

    def test_error_conflict_time_three(self):
        response = self.client.post(self.check_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-03-7'})
        response2 = self.client.post(self.check_url, {'start': '1:30:00', 'end': '02:20:00', 'date': '2020-03-7'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)


class FunctionalityTest(APITestCase):
    def setUp(self):
        self.username = 'test_user_name'
        self.email = 'test@test.com'
        self.password = 'test_user_name'

        self.check_url = reverse("check")
        self.leave_url = reverse("leave")

        self.week_url = reverse("week_hours")
        self.month_url = reverse("month_hours")
        self.year_url = reverse("year_hours")
        self.quarter_url = reverse("quarter_hours")

        self.avg_check_url = reverse("avg_check_time")
        self.percent_worked_hours = reverse("work_ratio")

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_week_hours(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '17:00:00', 'date': '2020-03-9', 'vacation': 'False'})
        response_leave = self.client.post(self.leave_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-03-9'})
        response_check_two = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '11:00:00', 'date': '2020-03-16', 'vacation': 'False'})
        response_total_week_time = self.client.get(self.week_url)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_leave.status_code)
        self.assertEqual(201, response_check_two.status_code)
        self.assertEqual(200, response_total_week_time.status_code)
        self.assertEqual(response_total_week_time.data['duration'], '7:00:00')

    def test_month_hours(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '17:00:00', 'date': '2020-02-9', 'vacation': 'False'})
        response_leave = self.client.post(self.leave_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2020-02-9'})
        response_check_two = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '11:00:00', 'date': '2020-03-10', 'vacation': 'False'})
        response_total_month_time = self.client.get(self.month_url)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_leave.status_code)
        self.assertEqual(201, response_check_two.status_code)
        self.assertEqual(200, response_total_month_time.status_code)
        self.assertEqual(response_total_month_time.data['duration'], '7:00:00')

    def test_year_hours(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '17:00:00', 'date': '2019-02-9', 'vacation': 'False'})
        response_leave = self.client.post(self.leave_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2019-02-9'})
        response_check_two = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '11:00:00', 'date': '2020-03-10', 'vacation': 'False'})
        response_total_year_time = self.client.get(self.year_url)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_leave.status_code)
        self.assertEqual(201, response_check_two.status_code)
        self.assertEqual(200, response_total_year_time.status_code)
        self.assertEqual(response_total_year_time.data['duration'], '7:00:00')

    def test_quarter_hours(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '17:00:00', 'date': '2019-11-9', 'vacation': 'False'})
        response_leave = self.client.post(self.leave_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2019-11-9'})
        response_check_two = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '11:00:00', 'date': '2019-03-10', 'vacation': 'False'})
        response_total_quarter_time = self.client.get(self.quarter_url)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_leave.status_code)
        self.assertEqual(201, response_check_two.status_code)
        self.assertEqual(200, response_total_quarter_time.status_code)
        self.assertEqual(response_total_quarter_time.data['duration'], '7:00:00')

    def test_avg_check_time(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '10:00:00', 'date': '2019-11-9', 'vacation': 'False'})
        response_check_two = self.client.post(self.check_url, {'check_in': '04:00:00', 'check_out': '12:00:00', 'date': '2020-03-10', 'vacation': 'False'})
        avg_check_time = self.client.get(self.avg_check_url)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_check_two.status_code)
        self.assertEqual(200, avg_check_time.status_code)
        self.assertEqual(avg_check_time.data['Avg check_in'], '6:00:00')
        self.assertEqual(avg_check_time.data['Avg check_out'], '11:00:00')

    def test_work_ratio(self):
        response_check = self.client.post(self.check_url, {'check_in': '08:00:00', 'check_out': '16:00:00', 'date': '2019-11-9', 'vacation': 'False'})
        response_leave = self.client.post(self.leave_url, {'start': '01:00:00', 'end': '03:00:00', 'date': '2019-11-9'})
        work_ratio = self.client.get(self.percent_worked_hours)
        self.assertEqual(201, response_check.status_code)
        self.assertEqual(201, response_leave.status_code)
        self.assertEqual(200, work_ratio.status_code)
        self.assertEqual(work_ratio.data['Work hour / leave hour'], '3.0')
