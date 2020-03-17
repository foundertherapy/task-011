from .models import WorkingDetails, LeavingTime
import datetime


class DatabaseHandler:
    @staticmethod
    def get_total_hours_working_or_leaving(model, date_from=None, date_to=None, user=None):
        time_zero = datetime.timedelta(hours=0, minutes=0, seconds=0)
        hours = time_zero
        if user:
            entries = model.objects.filter(user=user, date__range=[date_from, date_to])
        else:
            entries = model.objects.all()
        for entry in entries:
            duration = entry.duration()
            if duration is not None:
                hours = hours + duration
        return hours

    @staticmethod
    def get_total_worked_hours(user, start_date, end_date):
        time_zero = datetime.timedelta(hours=0, minutes=0, seconds=0)
        working_hours = DatabaseHandler.get_total_hours_working_or_leaving(WorkingDetails, start_date, end_date, user)
        leaving_hours = DatabaseHandler.get_total_hours_working_or_leaving(LeavingTime, start_date, end_date, user)
        if working_hours > time_zero:
            total_time = working_hours - leaving_hours
        else:
            total_time = time_zero
        return total_time

    @staticmethod
    def get_avg_check_in_or_out(user, check_in):
        check_type = 'check_in'
        if not check_in:
            check_type = 'check_out'
        times = WorkingDetails.objects.filter(user=user, vacation=False, check_out__isnull=False).values_list(check_type, flat=True)
        seconds = map(lambda time: time.hour * 60 * 60 + time.minute * 60.0 + time.second, times)
        check_in_avg_seconds = sum(seconds) / len(times)
        return str(datetime.timedelta(seconds=check_in_avg_seconds))

    @staticmethod
    def whole_team_work_ratio():
        time_zero = datetime.timedelta(hours=0, minutes=0, seconds=0)
        working_hours = DatabaseHandler.get_total_hours_working_or_leaving(WorkingDetails)
        leaving_hours = DatabaseHandler.get_total_hours_working_or_leaving(LeavingTime)
        percent_worked = 0
        if working_hours > time_zero:
            total_time = working_hours - leaving_hours
        else:
            total_time = time_zero
        if leaving_hours > time_zero:
            percent_worked = total_time / leaving_hours
        return percent_worked

    @staticmethod
    def get_week_total(user):
        today = datetime.datetime.now().date()
        today_week_day = today.weekday()

        last_week_start_date = today - datetime.timedelta(days=today.weekday() + 1)
        if today_week_day != 6:
            last_week_start_date = today - datetime.timedelta(days=today.weekday() + 8)
        last_week_end_date = last_week_start_date + datetime.timedelta(days=4)

        total_time = DatabaseHandler.get_total_worked_hours(user, last_week_start_date, last_week_end_date)
        print(str(last_week_start_date) + '    ' + str(last_week_end_date))
        return total_time

    @staticmethod
    def get_month_total(user):
        today = datetime.datetime.now().date()

        month_first_day_date = today.replace(day=1)
        last_month_first_day_date = month_first_day_date.replace(month=today.month - 1, day=1)
        last_month_last_day_date = month_first_day_date - datetime.timedelta(days=1)

        total_time = DatabaseHandler.get_total_worked_hours(user, last_month_first_day_date, last_month_last_day_date)
        print(str(last_month_first_day_date) + '    ' + str(last_month_last_day_date))
        return total_time

    @staticmethod
    def get_year_total(user):
        today = datetime.datetime.now().date()

        last_year_last_day_date = today.replace(day=1, month=1) - datetime.timedelta(days=1)
        last_year_first_day_date = last_year_last_day_date.replace(day=1, month=1)

        total_time = DatabaseHandler.get_total_worked_hours(user, last_year_first_day_date, last_year_last_day_date)
        print(str(last_year_first_day_date) + '    ' + str(last_year_last_day_date))
        return total_time

    @staticmethod
    def get_quarter_total(user):
        today = datetime.datetime.now().date()
        month = today.month

        quarter = 0
        for i in range(3):
            month = month - 3
            if month <= 0:
                break
            quarter = quarter + 1

        last_quarter_last_date = today.replace(day=1, month=quarter * 3 + 1) - datetime.timedelta(days=1)
        last_quarter_start_date = last_quarter_last_date.replace(day=1, month=last_quarter_last_date.month - 2)

        total_time = DatabaseHandler.get_total_worked_hours(user, last_quarter_start_date, last_quarter_last_date)
        print(str(quarter) + '     ' + str(last_quarter_start_date) + '    ' + str(last_quarter_last_date))
        return total_time
