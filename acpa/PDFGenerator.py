#!/usr/bin/env python
from reportlab.pdfgen import canvas

point = 1
inch = 72
TEXT = '{0}/{1}'

def make_pdf_file(output_filename, np):
    c = canvas.Canvas(output_filename, pagesize=(8.5 * inch, 11 * inch))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12 * point)
    for pn in range(1, np + 1):
        v = 10 * inch
        for subtline in (TEXT.format(pn, np)).split('\n'):
            c.drawString(1 * inch, v, subtline)
            v -= 12 * point
        c.showPage()
    c.save()

if __name__ == "__main__":
    filename = 'sample.pdf'
    make_pdf_file(filename, 250)
    print ("Wrote", filename)
    