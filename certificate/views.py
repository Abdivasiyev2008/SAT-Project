from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string  # Import render_to_string
from weasyprint import HTML
from .models import Certificate
from tests.models import Practice
from django.templatetags.static import static
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage



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
        'user': request.user.username,
        })


def ranks(request, pk):
    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Praktikaga tegishli barcha foydalanuvchilarni sertifikatlari bo'yicha tartiblash
    users = Certificate.objects.filter(practice=practice).order_by('-overall')

    # Agar sertifikatlar bo'lmasa ham ranks.html ni render qilish
    return render(request, 'certificate/ranks.html', {'users': users})


def download_certificate(request, pk, username):
    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)
    image_url = request.build_absolute_uri(static('images/main/logo1.jpg'))

    # Username orqali foydalanuvchini olish
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    # Foydalanuvchi va praktikaga tegishli sertifikatni olish
    certificate = Certificate.objects.filter(practice=practice, user=user).first()

    if not certificate:
        return render(request, 'certificate/error.html', {'error_message': 'No certificate found for this practice.'})

    # QR code yaratish
    qr_data = f"https://theteacher.uz/tests/{pk}/certificate/download/{username}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = BytesIO()
    qr.make_image(fill='black', back_color='white').save(qr_image)
    qr_image.seek(0)

    # QR kodni base64 formatga o‘tkazish
    qr_code_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')
    qr_code_data = f"data:image/png;base64,{qr_code_base64}"

    # HTML faylini yaratish
    html_content = render_to_string('certificate/certificate_download.html', {
        'certificate': certificate,
        'qr_code': qr_code_data,
        'image_url': image_url,
    })

    # HTMLni PDFga aylantirish
    pdf_file = HTML(string=html_content).write_pdf(stylesheets=['static/css/certificate_pdf.css'])

    # PDF faylini foydalanuvchiga yuborish
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sat_scores_{certificate.user.username}.pdf"'

    return response
