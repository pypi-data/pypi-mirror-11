#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# cargo.py -
# Copyright (C) 2015 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import six


class CARGO:
    PRESIDENTE = 1
    VICEPRESIDENTE = 2
    CONSEJERO = 3
    SECRETARIO = 4
    VICESECRETARIO = 5
    CONS_DEL_MAN = 6
    ADM_UNICO = 7
    MIE_CONS_REC = 8
    PRE_CONS_REC = 9
    SEC_CONS_REC = 10
    ADM_SOLID = 11
    APODERADO = 12
    SOC_PROF = 13
    APO_MAN_SOLI = 14
    APO_MANC = 15
    APO_SOL = 16
    ADM_MANCOM = 17
    CO_DE_MA_SO = 18
    CONS_DEL_SOL = 19
    REPRESENTANTE = 20
    CONS_DELEGADO = 21
    APOD_SOL_MAN = 22
    LIQUISOLI = 23
    LIQUIDADOR = 24
    APODERADO_SOL = 25
    REPR_143_RRM = 26
    AUD_C_CON = 27
    SECRE_NO_CONSEJ = 28
    CONS_DEL_M_S = 29
    VSECR_NO_CONSJ = 30
    AUDITOR = 31
    ADM_CONCURS = 32
    REP_ADM_CONC = 33
    AUD_SUPL = 34

    _keywords = {'Presidente': PRESIDENTE,
                 'Vicepresid': VICEPRESIDENTE,
                 'Consejero': CONSEJERO,
                 'Secretario': SECRETARIO,
                 'Vicesecret': VICESECRETARIO,
                 'Cons.Del.Man': CONS_DEL_MAN,
                 'Mie.Cons.Rec': MIE_CONS_REC,
                 'Pre.Cons.Rec': PRE_CONS_REC,
                 'Sec.Cons.Rec': SEC_CONS_REC,
                 'Adm. Unico': ADM_UNICO,
                 'Adm. Solid.': ADM_SOLID,
                 'ADM.CONCURS': ADM_CONCURS,
                 'Adm. Mancom': ADM_MANCOM,
                 'Apoderado': APODERADO,
                 'Apo.Man.Soli': APO_MAN_SOLI,
                 'Apo.Manc': APO_MANC,
                 'Apo.Sol': APO_SOL,
                 'APODERAD.SOL': APODERADO_SOL,
                 'APOD.SOL/MAN': APOD_SOL_MAN,
                 'Soc.Prof': SOC_PROF,
                 'Co.De.Ma.So': CO_DE_MA_SO,
                 'Cons.Del.Sol': CONS_DEL_SOL,
                 'Representan': REPRESENTANTE,
                 'Con.Delegado': CONS_DELEGADO,
                 'Liquidador': LIQUIDADOR,
                 'LiquiSoli': LIQUISOLI,
                 'LiqSolid': LIQUISOLI,
                 'REPR.143 RRM': REPR_143_RRM,
                 'CONSEJERO': CONSEJERO,
                 'CONS.DEL.M/S': CONS_DEL_M_S,
                 'CONS. DELEG.': CONS_DELEGADO,
                 'SecreNoConsj': SECRE_NO_CONSEJ,
                 'VsecrNoConsj': VSECR_NO_CONSJ,
                 'Auditor': AUDITOR,
                 'Aud.C.Con.': AUD_C_CON,
                 'Aud.Supl.': AUD_SUPL,
                 'REP.ADM.CONC': REP_ADM_CONC
                 }
    KEYWORDS = list(six.viewkeys(_keywords))

    @staticmethod
    def from_string(string):
        return CARGO._keywords[string]
