from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import LeakPassword
from search.views import normalize_url
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LeakPasswordSerializer

import logging
from collections import defaultdict


@api_view(['POST'])
def search_api(request):
    """URL'larni qidirish va natijalarni qaytarish."""
    search_text = request.data.get('search_text', '').strip()
    user_token = request.data.get('user_token', '')

    if not search_text:
        return JsonResponse({"detail": "Qidiruv matni bo'sh bo'lmasligi kerak."}, status=status.HTTP_400_BAD_REQUEST)
    
    if user_token != "TI_Project":
        return JsonResponse({}, status=status.HTTP_200_OK)

    search_text_clean = normalize_url(search_text)
    matching_entries = []

    # Bazadagi barcha mos keluvchi yozuvlarni olish
    leak_entries = LeakPassword.objects.filter(url__icontains=search_text_clean)

    for entry in leak_entries:
        matching_entries.append({
            "url": entry.url,
            "username": entry.username,
            "password": entry.password,
            "time": entry.time,
        })

    return JsonResponse({"matching_entries": matching_entries}, status=status.HTTP_200_OK)

class LeakPasswordCreateView(APIView):
    def post(self, request):
        serializer = LeakPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Set up logging
logger = logging.getLogger(__name__)
class DomainLeakCountView(APIView):
    def get(self, request, domain):
        domain_cleaned = domain.strip('http://').strip('https://')

        try:
            # Query the database and filter LeakPassword objects that contain the domain
            leaks = LeakPassword.objects.filter(url__icontains=domain_cleaned)

            # Use defaultdict to group by year and month
            grouped_leaks = defaultdict(lambda: defaultdict(int))

            for leak in leaks:
                year = leak.time.year
                month = leak.time.month
                grouped_leaks[year][month] += 1

            # Prepare response data
            data = []
            for year, months in grouped_leaks.items():
                for month, count in months.items():
                    data.append({'year': year, 'month': month, 'count': count})

            # Order by year and month descending
            data = sorted(data, key=lambda x: (x['year'], x['month']), reverse=True)

            return Response(data)

        except Exception as e:
            logger.error(f"Error fetching and processing data: {e}")
            return Response({"error": str(e)}, status=500)
