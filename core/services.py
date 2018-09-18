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
            cursor.execute("SELECT "+cols[0]+", "+cols[1]+", "+cols[2]+" FROM "+table+" WHERE "+filter_col+" = '"+filter_val+"'")
            result = self.namedtuplefetchall(cursor)
        return result

    def dateQuery(self, cols, date_col, from_date, to_date, table):
        with connection.cursor() as cursor:
            cursor.execute("SELECT "+cols[0]+", "+cols[1]+", "+cols[2]+" FROM "+table+" WHERE "+date_col+
                           " BETWEEN TO_DATE('"+from_date+"', 'MM-DD-YYYY') AND TO_DATE('"+to_date+"', 'MM-DD-YYYY')")
            result = self.namedtuplefetchall(cursor)
        return result

    def count_query(self, col, table):
        with connection.cursor() as cursor:
            cursor.execute("SELECT "+col+", COUNT (*) AS COUNT FROM "+ table  +" GROUP BY " + col)
            result = self.namedtuplefetchall(cursor)
        return result

    def sum_query(self,col, table, filter_col, filter_val, sum_col):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM "+
                "(SELECT "+col+" FROM "+ table+" WHERE "+filter_col+" = "+filter_val+") A,"+
                "(SELECT SUM("+sum_col+") AS SUM FROM "+table+") B")
            result = self.namedtuplefetchall(cursor)
        return result

    def max_query(self, col, max_col, table):
        with connection.cursor() as cursor:
            cursor.execute("SELECT "+col+", MAX("+max_col+") AS MAX FROM "+ table  +" GROUP BY " + col);
            result = self.namedtuplefetchall(cursor)
        return result

    def third_query(self, filter_col, filter_val):
        if filter_col is None and filter_val is None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT EMPLOYEE.FIRST_NAME, DEPARTMENT.NAME, JOB.FUNCTION "
                    +"FROM JOB, EMPLOYEE, DEPARTMENT "
                    +"WHERE EMPLOYEE.JOB_ID = JOB.JOB_ID "
                    +"AND DEPARTMENT.DEPARTMENT_ID = EMPLOYEE.DEPARTMENT_ID")
                result = self.namedtuplefetchall(cursor)
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT EMPLOYEE.FIRST_NAME, DEPARTMENT.NAME, JOB.FUNCTION "
                               + "FROM JOB, EMPLOYEE, DEPARTMENT "
                               + "WHERE EMPLOYEE.JOB_ID = JOB.JOB_ID "
                               + "AND DEPARTMENT.DEPARTMENT_ID = EMPLOYEE.DEPARTMENT_ID"
                               + " AND EMPLOYEE."+filter_col+" = '"+filter_val+"'")
                result = self.namedtuplefetchall(cursor)
        return result

    def two_tables_sum(self, pk):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM"
            +" (SELECT SUM(QUANTITY) AS SUM FROM ITEM WHERE ITEM.PRODUCT_ID = "+pk+") A,"
            +" (SELECT PRODUCT.DESCRIPTION FROM PRODUCT WHERE PRODUCT_ID = "+pk+") B")
            result = self.namedtuplefetchall(cursor)
        return result

    def two_tables_count(self, pk):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM "
            +" (SELECT COUNT (*) AS COUNT FROM EMPLOYEE WHERE EMPLOYEE.JOB_ID = "+pk+") A,"
            +" (SELECT FUNCTION FROM JOB WHERE JOB_ID = "+pk+") B")
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
        min_data = data

        if len(data)>30:
            min_data = data[:30]
            rest_data = data[30:]


        if len(data[0])==3:
            t_height = (p_h * 0.75) - (len(min_data) * 0.6 * cm)
            t_width = (p_w - (len(min_data[0]) * 5 * cm)) / 2
        else:
            t_height = (p_h * 0.75) - (len(min_data) * 0.6 * cm)
            t_width = 156

        # Contenido de la Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        # Dibujo de la tabla
        table = Table(min_data, colWidths=[5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm],
                      rowHeights=0.6 * cm)
        table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
        table.wrapOn(c, p_w, p_h)
        table.drawOn(c, t_width, t_height)
        c.showPage()


        if len(data)>30:
            pages = int(len(rest_data)/30)
            if len(rest_data)%30 != 0:
                pages = pages+1
            for i in range(0, pages):
                min_data = rest_data[:30]
                rest_data = rest_data[30:]
                t_height = (p_h * 0.9) - (len(min_data) * 0.6 * cm)
                t_width = (p_w - (len(min_data[0]) * 5 * cm)) / 2

                # Contenido de la Tabla
                styleN = styles["BodyText"]
                styleN.alignment = TA_CENTER
                styleN.fontSize = 7
                # Dibujo de la tabla
                table = Table(min_data,
                              colWidths=[5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm],
                              rowHeights=0.6 * cm)
                table.setStyle(TableStyle(
                    [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                     ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
                table.wrapOn(c, p_w, p_h)
                table.drawOn(c, t_width, t_height)
                c.showPage()

        c.save()

        pdf = buffer.getvalue()
        buffer.close()
        return pdf
