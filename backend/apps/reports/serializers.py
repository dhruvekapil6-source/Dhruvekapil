from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'report_type', 'format', 'title', 'description',
                  'start_date', 'end_date', 'filters', 'file_path',
                  'generated_by', 'total_records', 'status', 'created_at', 'generated_at')
        read_only_fields = ('id', 'created_at', 'file_path', 'generated_at')
