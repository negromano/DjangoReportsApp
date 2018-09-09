import io
import json
import time
from io import BytesIO

from django.shortcuts import render
from PIL import Image
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template.defaultfilters import center
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import xlsxwriter
from reportlab.platypus import Table, TableStyle, Paragraph
from core.models import Flows, FlowTypes, Devices, Stations, Record
from collections import namedtuple
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
    queries = queries()
    cols = ["FIRST_NAME", "LAST_NAME", "SALARY"]
    filter_col = "EMPLOYEE_ID"
    filter_val = "7839"
    table = "EMPLOYEE"
    result = queries.firstQuery(cols, filter_col, filter_val, table)
    return HttpResponse("It works!")
