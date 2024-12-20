from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string  # Import render_to_string
from weasyprint import HTML
from .models import Certificate
from tests.models import Practice

# Sertifikatni olish
def get_certificate(request, pk):
    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Foydalanuvchi va praktikaga tegishli sertifikatlarni olish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user)
    print(certificate_data)

    # Sertifikatlar topilmasa
    if not certificate_data:
        return render(request, 'certificate/error.html', {'error_message': 'No certificates found for this practice.'})

    # Sertifikatlarni template-ga jo'natish
    return render(request, 'certificate/certificate_list.html', {
        'certificate_data': certificate_data,
        'id': pk,
        })


# Rangslarni olish
def ranks(request, pk):
    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Foydalanuvchi va praktikaga tegishli sertifikatlar bo'yicha tartiblash
    users = Certificate.objects.filter(practice=practice, user=request.user).order_by('-overall')

    # Sertifikatlar topilmasa
    if not users:
        return render(request, 'certificate/error.html', {'error_message': 'No certificates found for this practice.'})

    # Sertifikatlarni ranks.html template-ga jo'natish
    return render(request, 'certificate/ranks.html', {'users': users})


# Sertifikatni PDF sifatida yuklab olish
def download_certificate(request, pk):
    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Foydalanuvchi va praktikaga tegishli sertifikatni olish
    certificate = Certificate.objects.filter(practice=practice, user=request.user).first()  # .first() orqali faqat bitta sertifikatni olish
    print(certificate)

    if not certificate:
        return render(request, 'certificate/error.html', {'error_message': 'No certificate found for this practice.'})

    # HTML faylini yaratish
    html_content = render_to_string('certificate/certificate_download.html', {
        'certificate': certificate
    })

    # HTMLni PDFga aylantirish
    pdf_file = HTML(string=html_content).write_pdf()

    # PDF faylini foydalanuvchiga yuborish
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sat_scores_{certificate.user.username}.pdf"'

    return response
