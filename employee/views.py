from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .api.serializers import WorkingDetailsSerializer, LeavingTimeSerializer, VacationDateSerializer
from .models import WorkingDetails
from rest_framework.decorators import api_view
from datetime import datetime, timedelta, time
from .database_handler import DatabaseHandler
from django.db.models import Avg
time_zero = timedelta(hours=0, minutes=0, seconds=0)


# /employee/check
class WorkingDetailsCreateView(CreateAPIView):
    serializer_class = WorkingDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# /employee/hours
class WorkingDetailsListView(ListAPIView):
    serializer_class = WorkingDetailsSerializer

    def get_queryset(self):
        queryset = WorkingDetails.objects.filter(user=self.request.user)
        return queryset


# employee/leave
class LeaveWorkCreateView(CreateAPIView):
    serializer_class = LeavingTimeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# employee/vacation
class VacationCreateView(CreateAPIView):
    serializer_class = VacationDateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# This api and the next one build auto check in and chek out functionality 
# /employee/check_in
# crate WaorkingDetails entry and auto calculate check in time 
@api_view(['POST'])
def check_in(request):
    today = datetime.now().date()
    current_user = request.user
    working_details = WorkingDetails.objects.filter(user=current_user, date=today)
    if not working_details:
        new_entry = WorkingDetails()
        new_entry.user = current_user
        new_entry.date = today
        new_entry.check_in = datetime.now().time()
        new_entry.save()
        return Response({"message": "check in done"})
    else:
        return Response({"message": "already checked in"})


# /employee/check_out
# Auto calculate check_out time and add it the entry that have checked in 
@api_view(['POST'])
def check_out(request):
    today = datetime.now().date()
    current_time = datetime.now().time()
    current_user = request.user
    working_details = WorkingDetails.objects.filter(user=current_user, date=today)
    if working_details:
        entry = working_details.first()
        if entry.vacation:
            return Response({"message": "Today is vacation"})
        if isinstance(entry.check_out, type(None)):
            entry.check_out = current_time
            entry.save()
            return Response({"message": "check out done"})
        else:
            return Response({"message": "already checked out"})
    else:
        return Response({"message": "User is not checked in"})


# /employee/week_hours
@api_view(['GET'])
def employee_week_hours(request):
    total_time = DatabaseHandler.get_week_total(request.user)
    return Response({"duration": str(total_time)})


# /employee/month_hours
@api_view(['GET'])
def employee_month_hours(request):
    total_time = DatabaseHandler.get_month_total(request.user)
    return Response({"duration": str(total_time)})


# /employee/year_hours
@api_view(['GET'])
def employee_year_hours(request):
    total_time = DatabaseHandler.get_year_total(request.user)
    return Response({"duration": str(total_time)})


# /employee/quarter_hours
@api_view(['GET'])
def employee_quarter_hours(request):
    total_time = DatabaseHandler.get_quarter_total(request.user)
    return Response({"duration": str(total_time)})


# /employee/avg_check_time
@api_view(['GET'])
def avg_check_time(request):
    avg_check_in = DatabaseHandler.get_avg_check_in_or_out(request.user, True)
    avg_check_out = DatabaseHandler.get_avg_check_in_or_out(request.user, False)
    return Response({"Avg check_in": str(avg_check_in), "Avg check_out": str(avg_check_out)})


# /employee/work_ratio
@api_view(['GET'])
def work_ratio(request):
    ratio = DatabaseHandler.whole_team_work_ratio()
    return Response({"Work hour / leave hour": str(ratio)})
