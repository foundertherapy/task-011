from rest_framework import serializers
from employee.models import WorkingDetails, LeavingTime


class WorkingDetailsSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        start = attrs['check_in']
        end = attrs['check_out']
        date = attrs['date']
        vacation = attrs['vacation']
        if start >= end:
            raise serializers.ValidationError({'error': "start time is larger than end time"})
        date_error = WorkingDetails.objects.filter(date=date, user=self.context['request'].user)
        if date_error:
            raise serializers.ValidationError({'error': "We have a different leave conflict with this"})
        return attrs

    class Meta:
        model = WorkingDetails
        fields = ['date', 'check_in', 'check_out', 'vacation']


class LeavingTimeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        start = attrs['start']
        end = attrs['end']
        leaving_date = attrs['date']
        if start >= end:
            raise serializers.ValidationError({'error': "start time is larger than end time"})
        range_error = LeavingTime.objects.filter(start__lt=end, end__gt=start, date=leaving_date, user=self.context['request'].user)
        if range_error:
            raise serializers.ValidationError({'error': "We have a different leave conflict with this"})
        return attrs

    class Meta:
        model = LeavingTime
        fields = ['start', 'end', 'date']


class VacationDateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        vacation = attrs['vacation']
        if vacation != True:
            raise serializers.ValidationError({'error': "Vacation must be True"})
        return attrs

    class Meta:
        model = WorkingDetails
        fields = ['date', 'vacation']