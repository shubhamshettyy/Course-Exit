from django.shortcuts import render

# Create your views here.


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

def html_to_pdf_view(request):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string('course/pdf_template.html', {'paragraphs': paragraphs})

    html = HTML(string=html_string)
    fs = FileSystemStorage('./')
    print(fs.location)
    html.write_pdf(target='./mypdf.pdf');
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response 

    return response