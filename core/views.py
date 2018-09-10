from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from core.services import *


def acerca(request):
    return HttpResponse(":D")

def index(request):
    return HttpResponse(":D")

def download_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    data = []
    pdf = reports.pdf(data, "Testing info")
    response.write(pdf)
    return response

def download_excel_report(request):
    output = reports.excel()
    filename = 'reporte' + '.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def oracle(request):
    service = queries()
    cols = ["FIRST_NAME", "LAST_NAME", "SALARY"]
    data = [cols]
    filter_col = "HIRE_DATE"
    from_date = "01-01-1980"
    to_date = "01-01-2010"
    table = "EMPLOYEE"
    result = service.dateQuery(cols, filter_col, from_date, to_date, table)
    for row in result:
        data.append([row[0], row[1], row[2]])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    pdf = reports.pdf(data, "Testing info")
    response.write(pdf)
    return response
