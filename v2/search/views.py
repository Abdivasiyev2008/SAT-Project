import re
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from leak.models import LeakPassword  # LeakPassword modelini import qilamiz
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def stats(request):
    """Vaqtga qarab URL'larni saralash va hisobini olish, statistikani hisoblash."""
    current_time = timezone.now()

    # 3 oylik, 6 oylik va 1 yillik muddatlar
    three_months_ago = current_time - timedelta(days=90)
    six_months_ago = current_time - timedelta(days=180)
    one_year_ago = current_time - timedelta(days=365)

    # Har bir muddat uchun URL'larni hisoblash
    three_months_count = LeakPassword.objects.filter(time__gte=three_months_ago).count()
    last_three_months_count = LeakPassword.objects.filter(time__lt=three_months_ago, time__gte=six_months_ago).count()

    six_months_count = LeakPassword.objects.filter(time__gte=six_months_ago).count()
    last_six_months_count = LeakPassword.objects.filter(time__lt=six_months_ago, time__gte=one_year_ago).count()

    one_year_count = LeakPassword.objects.filter(time__gte=one_year_ago).count()
    prev_one_year_count = LeakPassword.objects.filter(time__lt=one_year_ago, time__gte=(one_year_ago - timedelta(days=365))).count()

    # Foizlarni hisoblash
    def calculate_percentage(current, previous):
        if previous > 0:
            return round((current - previous) / previous * 100, 2)
        return 0  # Oldingi davrda ma'lumot yo‘q bo‘lsa, o‘sish 0% bo‘ladi

    return Response({
        'three_months_count': three_months_count,
        'three_months_percentage': calculate_percentage(three_months_count, last_three_months_count),
        'six_months_count': six_months_count,
        'six_months_percentage': calculate_percentage(six_months_count, last_six_months_count),
        'one_year_count': one_year_count,
        'one_year_percentage': calculate_percentage(one_year_count, prev_one_year_count),
    })

def normalize_url(url):
    """URL prefikslarini olib tashlash va to'liq URL qismini qaytarish."""
    # http:// yoki https:// prefikslarini olib tashlash
    parsed_url = re.sub(r'^https?://', '', url)
    
    # Port raqamlarini olib tashlash va faqat domenni saqlash
    parsed_url = parsed_url.split('/')[0]
    return parsed_url.lower()

def search_urls_in_db(search_text):
    """Bazadagi URL'larni qidirish va mos keladigan kirishlarni chiqarish."""
    search_text_clean = normalize_url(search_text)

    if search_text_clean != '.uz' or search_text_clean != 'uz':
        matching_entries = []

        # Bazadagi barcha ma'lumotlarni olish
        leak_entries = LeakPassword.objects.all()

        for entry in leak_entries:
            # Har bir URL'ni normalize qilib solishtiramiz
            url_part = normalize_url(entry.url)
            
            # Agar qidiruv matni URL ichida bo'lsa, ma'lumotni qo'shamiz
            if search_text_clean in url_part:
                matching_entries.append(f"{entry.url}:{entry.username}:{entry.password}")

        return matching_entries

@require_http_methods(["GET", "POST"])
def search_form(request):
    """Foydalanuvchi matnni qidirish va natijani ko'rsatish."""
    if request.method == "POST":
        search_text = request.POST.get('search_text', '').strip()

        if search_text:
            # URL'ni qidirish
            matching_entries = search_urls_in_db(search_text)

            # Natijalarni ko'rsatish
            if matching_entries:
                return render(request, 'results.html', {'matching_entries': matching_entries})
            else:
                return render(request, 'results.html', {'message': 'Matn topilmadi!'})

    return render(request, 'search_form.html')
