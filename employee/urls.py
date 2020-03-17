from django.urls import path
from rest_framework.authtoken import views as login_views
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('login/', login_views.obtain_auth_token, name='login'),
    path('apply_vacation/', views.VacationCreateView.as_view(), name='vacation'),
    path('check/', views.WorkingDetailsCreateView.as_view(), name='check'),
    path('hours/', views.WorkingDetailsListView.as_view(), name='all_hours'),
    path('check_in/', views.check_in, name='check_in'),
    path('check_out/', views.check_out, name='check_out'),
    path('leave/', views.LeaveWorkCreateView.as_view(), name='leave'),
    path('week_hours/', views.employee_week_hours, name='week_hours'),
    path('month_hours/', views.employee_month_hours, name='month_hours'),
    path('year_hours/', views.employee_year_hours, name='year_hours'),
    path('quarter_hours/', views.employee_quarter_hours, name='quarter_hours'),
    path('avg_check_time/', views.avg_check_time, name='avg_check_time'),
    path('work_ratio/', views.work_ratio, name='work_ratio'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
