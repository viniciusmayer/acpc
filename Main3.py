'''
Created on 8 de jun de 2018

@author: eleonorvinicius
'''

import glob
import sys

from PyPDF2 import PdfFileWriter, PdfFileReader


if __name__ == '__main__':
    origem = 'files/'
    for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
        try:
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            for numeroPagina in range(arquivo.getNumPages()):
                w_in_user_space_units = pdfFile.mediaBox.getWidth()
                h_in_user_space_units = pdfFile.mediaBox.getHeight()
                print('w units: {0}'.format(w_in_user_space_units, h_in_user_space_units))
                
                # 1 user space unit is 1/72 inch
                # 1/72 inch ~ 0.352 millimeters
                
                w = float(pdfFile.mediaBox.getWidth()) * 0.352
                h = float(pdfFile.mediaBox.getHeight()) * 0.352
                print('w millimeters: {0}'.format(w_in_user_space_units, h_in_user_space_units))
                print()
            
        except:
            print('ERROR reading file: {0}'.format(arquivo))
            print(sys.exc_info())
