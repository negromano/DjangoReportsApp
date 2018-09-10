import io
import time
from io import BytesIO

from PIL import Image
from django.template.defaultfilters import center
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import xlsxwriter
from reportlab.platypus import Table, TableStyle, Paragraph
from django.db import connection
from collections import namedtuple


class queries:

    def firstQuery(self, cols, filter_col, filter_val, table):
        with connection.cursor() as cursor:
            cursor.execute("SELECT "+cols[0]+", "+cols[1]+", "+cols[2]+" FROM "+table+" WHERE "+filter_col+" = "+filter_val)
            result = self.namedtuplefetchall(cursor)
        return result

    def dateQuery(self, cols, date_col, from_date, to_date, table):
        with connection.cursor() as cursor:
            cursor.execute("SELECT "+cols[0]+", "+cols[1]+", "+cols[2]+" FROM "+table+" WHERE "+date_col+
                           " BETWEEN TO_DATE('"+from_date+"', 'DD-MM-YYYY') AND TO_DATE('"+to_date+"', 'DD-MM-YYYY')")
            result = self.namedtuplefetchall(cursor)
        return result

    def namedtuplefetchall(self, cursor):
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

class reports:

    @staticmethod
    def pdf(data, description):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        path = "core/assets/unibague.png"
        i = Image.open(path)
        i_w, i_h = i.size
        p_w, p_h = A4

        # Encabezados
        c.drawImage(path, p_w / 10, p_h * 0.9, i_w / 5, i_h / 5)
        c.setFont('Helvetica-Bold', 15)
        c.setLineWidth(.3)
        c.drawString(p_w / 10, p_h * 0.83, description)
        c.setFont('Helvetica', 15)
        c.drawString(p_w * 0.70, p_h * 0.83, time.strftime("%d/%m/%Y"))

        # Header de Tabla
        styles = getSampleStyleSheet()
        styleH = styles["Normal"]
        styleH.fontName = "Helvetica-bold"
        styleH.alignment = TA_CENTER
        styleH.fontSize = 10
        t_height = (p_h - (1*0.6*cm))*0.2
        t_width = (p_w -(len(data[0])*2.7*cm))/2

        # Contenido de la Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        data=(["1","2","3"])
        # Dibujo de la tabla
        table = Table(data, colWidths=[2.7 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm],
                      rowHeights=0.6 * cm)
        table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
        table.wrapOn(c, p_w, p_h)
        table.drawOn(c, t_width, t_height)
        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    @staticmethod
    def excel():
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 7, 20)
        data = []
        header_format = workbook.add_format({'border': True, 'bold': True})
        header = ["Profundidad", "P. Corregida", "Área", "Velocidad", "Q", "Q Corregida", "Error"]
        for x in range(0, 7):
            worksheet.write(0, x, header[x], header_format)
        for i in range(0, 45):
            data.append(["1", "2", "3", "4", "5", "6", "7"])
        cell_format = workbook.add_format({'border': True})
        for row_num, columns in enumerate(data):
            for col_num, cell_data in enumerate(columns):
                worksheet.write(row_num + 1, col_num, cell_data, cell_format)
        workbook.close()
        output.seek(0)
        return output
