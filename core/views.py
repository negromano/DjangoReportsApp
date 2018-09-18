from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from core.services import *


def acerca(request):
    return render(request, 'acerca.html')

def index(request):
    return render(request, 'index.html')

def download_pdf_report(request, result, data, template):
    if len(result) == 0: return render(request, template, {
        'message': 'No se encontraron datos',
    })
    for row in result:
        data.append([row[0], row[1], row[2]])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    pdf = reports.pdf(data, "Reportes Unibague")
    response.write(pdf)
    return response

def download_pdf_report_two_cols(request, result, data, template):
    print(result)
    if len(result) == 0: return render(request, template, {
        'message': 'No se encontraron datos',
    })
    for row in result:
        data.append([row[0], row[1]])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    pdf = reports.pdf(data, "Reportes Unibague")
    response.write(pdf)
    return response


def tabla_sencilla_tipo_1(request):
    if request.method == 'GET':
        return render(request, 'tabla-sencilla/tipo1.html')
    if request.method == 'POST':
        service = queries()
        pk = request.POST['llavePrimaria']
        cols = ["FIRST_NAME", "LAST_NAME", "SALARY"]
        data = [cols]
        filter_col = "EMPLOYEE_ID"
        table = "EMPLOYEE"
        result = service.firstQuery(cols, filter_col, pk, table)
        return download_pdf_report(request, result, data, 'tabla-sencilla/tipo1.html')

def tabla_sencilla_tipo_2(request):
    if request.method == 'GET':
        return render(request, 'tabla-sencilla/tipo2.html')
    if request.method == 'POST':
        service = queries()
        filter_val = request.POST['filtro'].upper()
        cols = ["EMPLOYEE_ID", "LAST_NAME", "SALARY"]
        data = [cols]
        filter_col = "FIRST_NAME"
        table = "EMPLOYEE"
        result = service.firstQuery(cols, filter_col, filter_val, table)
        return download_pdf_report(request, result, data, 'tabla-sencilla/tipo2.html')

def tabla_sencilla_tipo_3(request):
    if request.method == 'GET':
        return render(request, 'tabla-sencilla/tipo3.html')
    if request.method == 'POST':
        service = queries()
        from_date = request.POST['from'].replace("/", "-")
        to_date = request.POST['to'].replace("/", "-")
        print(from_date)
        print(to_date)
        cols = ["FIRST_NAME", "LAST_NAME", "SALARY"]
        data = [cols]
        filter_col = "HIRE_DATE"
        table = "EMPLOYEE"
        result = service.dateQuery(cols, filter_col, from_date, to_date, table)
        return download_pdf_report(request, result, data, 'tabla-sencilla/tipo3.html')

def tabla_funcion_tipo_1(request):
    if request.method == 'GET':
        return render(request, 'tabla-funcion/tipo1.html')
    if request.method == 'POST':
        service = queries()
        attribute = request.POST['col']
        data = [[attribute, "COUNT"]]
        table = "CUSTOMER"
        result = service.count_query(attribute, table)
        return download_pdf_report_two_cols(request, result, data, 'tabla-funcion/tipo1.html')

def tabla_funcion_tipo_2(request):
    if request.method == 'GET':
        return render(request, 'tabla-funcion/tipo2.html')
    if request.method == 'POST':
        service = queries()
        filter_val = request.POST['llavePrimaria']
        col = "FIRST_NAME"
        filter_col = "EMPLOYEE_ID"
        cols = ["FIRST_NAME", "SALARY SUM"]
        data = [cols]
        table = "EMPLOYEE"
        sum_col = "SALARY"
        result = service.sum_query(col, table, filter_col, filter_val, sum_col)
        return download_pdf_report_two_cols(request, result, data, 'tabla-funcion/tipo2.html')

def tabla_funcion_tipo_3(request):
    if request.method == 'GET':
        return render(request, 'tabla-funcion/tipo3.html')
    if request.method == 'POST':
        service = queries()
        col = request.POST['col']
        max_col = "CREDIT_LIMIT"
        cols = [col, "MAX"]
        data = [cols]
        table = "CUSTOMER"
        result = service.max_query(col, max_col, table)
        return download_pdf_report_two_cols(request, result, data, 'tabla-funcion/tipo3.html')

def dos_tablas_sencillas_tipo_1(request):
    if request.method == 'GET':
        return render(request, 'dos-tablas-sencillas/tipo1.html')
    if request.method == 'POST':
        service = queries()
        cols = ["FIRST NAME", "DEPARTMENT NAME", "JOB NAME"]
        data = [cols]
        result = service.third_query(None, None)
        return download_pdf_report(request, result, data, 'dos-tablas-sencillas/tipo1.html')

def dos_tablas_sencillas_tipo_2(request):
    if request.method == 'GET':
        return render(request, 'dos-tablas-sencillas/tipo2.html')
    if request.method == 'POST':
        service = queries()
        filter_col = "EMPLOYEE_ID"
        filter_val = request.POST['llavePrimaria']
        cols = ["FIRST NAME", "DEPARTMENT NAME", "JOB NAME"]
        data = [cols]
        result = service.third_query(filter_col, filter_val)
        return download_pdf_report(request, result, data, 'dos-tablas-sencillas/tipo2.html')

def dos_tablas_sencillas_tipo_3(request):
    if request.method == 'GET':
        return render(request, 'dos-tablas-sencillas/tipo3.html')
    if request.method == 'POST':
        service = queries()
        filter_col = "FIRST_NAME"
        filter_val = request.POST['filtro'].upper()
        cols = ["FIRST NAME", "DEPARTMENT NAME", "JOB NAME"]
        data = [cols]
        result = service.third_query(filter_col, filter_val)
        return download_pdf_report(request, result, data, 'dos-tablas-sencillas/tipo3.html')

def dos_tablas_funcion_tipo_1(request):
    if request.method == 'GET':
        return render(request, 'dos-tablas-funcion/tipo1.html')
    if request.method == 'POST':
        service = queries()
        pk = request.POST['llavePrimaria']
        cols = ["SUM", "PRODUCT DESCRIPTION"]
        data = [cols]
        result = service.two_tables_count(pk)
        return download_pdf_report_two_cols(request, result, data, 'dos-tablas-funcion/tipo1.html')

def dos_tablas_funcion_tipo_2(request):
    if request.method == 'GET':
        return render(request, 'dos-tablas-funcion/tipo2.html')
    if request.method == 'POST':
        service = queries()
        pk = request.POST['llavePrimaria']
        cols = ["COUNT", "JOB NAME"]
        data = [cols]
        result = service.two_tables_sum(pk)
        return download_pdf_report_two_cols(request, result, data, 'dos-tablas-funcion/tipo2.html')

def customer_function(request):
    if request.method == 'GET':
        return render(request, 'customer.html')
    if request.method == 'POST':
        service = queries()
        cols = ["CUSTOMER", "SUM"]
        data = [cols]
        result = service.customer_query()
        return download_pdf_report_two_cols(request, result, data, 'customer.html')

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
