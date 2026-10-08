from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Reports"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['report_type', 'format', 'status']
    ordering_fields = ['created_at', 'generated_at']
