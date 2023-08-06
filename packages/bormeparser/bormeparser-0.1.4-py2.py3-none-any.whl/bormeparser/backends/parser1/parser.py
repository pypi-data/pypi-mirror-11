#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .functions import crop_file, clean_file, parse_file, parse_file_anuncios, convert_to_text_file

from bormeparser.backends.base import BormeParserBackend

class Parser1(BormeParserBackend):
    """
    Parse using pyPdf + pdfminer
    """
    def _parse(self):
        crop_file(self.filename, self.filename + '-cropped.pdf')
        convert_to_text_file(self.filename + '-cropped.pdf', self.filename + '.1.txt')
        clean_file(self.filename + '.1.txt', self.filename + '.2.txt')
        parse_file(self.filename + '.2.txt', self.filename + '.json')
        return True

    def _parse_actos(self, rewrite=True):
        crop_file(self.filename, self.filename + '-cropped.pdf', rewrite)
        convert_to_text_file(self.filename + '-cropped.pdf', self.filename + '.1.txt', rewrite)
        clean_file(self.filename + '.1.txt', self.filename + '.2.txt', rewrite)
        actos, _ = parse_file_anuncios(self.filename + '.2.txt', rewrite)
        return actos
