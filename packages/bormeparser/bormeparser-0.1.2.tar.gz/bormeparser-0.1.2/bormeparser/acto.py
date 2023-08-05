#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# seccion.py -
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

#from .utils import remove_accents
import six


class ACTO:
    NOMBRAMIENTOS = 1
    REVOCACIONES = 2
    CESES_DIMISIONES = 3
    MODIFICACIONES_ESTATUTARIAS = 4
    CAMBIO_DE_OBJETO_SOCIAL = 5
    CAMBIO_DE_DENOMINACION_SOCIAL = 6
    CAMBIO_DE_DOMICILIO_SOCIAL = 7
    AMPLIACION_DEL_OBJETO_SOCIAL = 8
    SOCIEDAD_UNIPERSONAL = 9
    DISOLUCION = 10
    REELECCIONES = 11
    CONSTITUCION = 12
    ARTICULO_378_5_DEL_RRM = 13
    OTROS_CONCEPTOS = 14
    AMPLIACION_DE_CAPITAL = 15
    REDUCCION_DE_CAPITAL = 16
    SITUACION_CONCURSAL = 17
    FUSION_POR_ABSORCION = 18
    SUSPENSION_DE_PAGOS = 19
    TRANSFORMACION_DE_SOCIEDAD = 20
    CANCELACIONES_DE_OFICIO_DE_NOMBRAMIENTOS = 21
    DESEMBOLSO_DE_DIVIDENDOS_PASIVOS = 22
    PAGINA_WEB_DE_LA_SOCIEDAD = 23
    PRIMERA_SUCURSAL_DE_SOCIEDAD_EXTRANJERA = 24
    SOCIEDAD_UNIPERSONAL = 25
    EXTINCION = 26
    DECLARACION_DE_UNIPERSONALIDAD = 27
    PERDIDA_DEL_CARACTER_DE_UNIPERSONALIDAD = 28
    REAPERTURA_HOJA_REGISTRAL = 29
    ADAPTACION_LEY_2_95 = 30
    CIERRE_PROVISIONAL_HOJA_REGISTRAL_POR_BAJA_EN_EL_INDICE_DE_ENTIDADES_JURIDICAS = 31
    CIERRE_PROVISIONAL_DE_LA_HOJA_REGISTRAL_POR_REVOCACION_DEL_NIF = 32
    REACTIVACION_DE_LA_SOCIEDAD = 32
    CAMBIO_DE_IDENTIDAD_DEL_SOCIO_UNICO = 33
    FE_DE_ERRATAS = 34
    SOCIO_UNICO = 35
    DATOS_REGISTRALES = 36

    # Palabras clave con argumentos
    _arg_keywords = {
        u'Nombramientos': NOMBRAMIENTOS,
        u'Revocaciones': REVOCACIONES,
        u'Ceses/Dimisiones': CESES_DIMISIONES,
        u'Modificaciones estatutarias': MODIFICACIONES_ESTATUTARIAS,
        u'Cambio de objeto social': CAMBIO_DE_OBJETO_SOCIAL,
        u'Cambio de denominación social': CAMBIO_DE_DENOMINACION_SOCIAL,
        u'Cambio de domicilio social': CAMBIO_DE_DOMICILIO_SOCIAL,
        u'Ampliacion del objeto social': AMPLIACION_DEL_OBJETO_SOCIAL,
        u'Sociedad unipersonal': SOCIEDAD_UNIPERSONAL,
        u'Disolución': DISOLUCION,
        u'Reelecciones': REELECCIONES,
        u'Constitución': CONSTITUCION,
        u'Articulo 378.5 del Reglamento del Registro Mercantil': ARTICULO_378_5_DEL_RRM,
        u'Otros conceptos': OTROS_CONCEPTOS,
        u'Ampliación de capital': AMPLIACION_DE_CAPITAL,
        u'Reducción de capital': REDUCCION_DE_CAPITAL,
        u'Situación concursal': SITUACION_CONCURSAL,
        u'Fusión por absorción': FUSION_POR_ABSORCION,
        u'Suspensión de pagos': SUSPENSION_DE_PAGOS,
        u'Transformación de sociedad': TRANSFORMACION_DE_SOCIEDAD,
        u'Cancelaciones de oficio de nombramientos': CANCELACIONES_DE_OFICIO_DE_NOMBRAMIENTOS,
        u'Desembolso de dividendos pasivos': DESEMBOLSO_DE_DIVIDENDOS_PASIVOS,
        u'Página web de la sociedad': PAGINA_WEB_DE_LA_SOCIEDAD,
        u'Primera sucursal de sociedad extranjera': PRIMERA_SUCURSAL_DE_SOCIEDAD_EXTRANJERA
    }

    # Palabras clave sin argumentos
    _noarg_keywords = {
        u'Sociedad unipersonal': SOCIEDAD_UNIPERSONAL,
        u'Extinción': EXTINCION,
        u'Declaración de unipersonalidad': DECLARACION_DE_UNIPERSONALIDAD,
        u'Pérdida del caracter de unipersonalidad': PERDIDA_DEL_CARACTER_DE_UNIPERSONALIDAD,
        u'Reapertura hoja registral': REAPERTURA_HOJA_REGISTRAL,
        u'Adaptación Ley 2/95': ADAPTACION_LEY_2_95,
        u'Cierre provisional hoja registral por baja en el índice de Entidades Jurídicas': CIERRE_PROVISIONAL_HOJA_REGISTRAL_POR_BAJA_EN_EL_INDICE_DE_ENTIDADES_JURIDICAS,
        u'Cierre provisional de la hoja registral por revocación del NIF': CIERRE_PROVISIONAL_DE_LA_HOJA_REGISTRAL_POR_REVOCACION_DEL_NIF,
        u'Reactivación de la sociedad (Art. 242 del Reglamento del Registro Mercantil)': REACTIVACION_DE_LA_SOCIEDAD
    }

    # Palabras clave seguidas por :
    _colon_keywords = {
        u'Cambio de identidad del socio único': CAMBIO_DE_IDENTIDAD_DEL_SOCIO_UNICO,
        u'Fe de erratas': FE_DE_ERRATAS,
        u'Socio único': SOCIO_UNICO
    }

    # Palabra clave
    _ending_keywords = {
        'Datos registrales': DATOS_REGISTRALES
    }

    ARG_KEYWORDS = list(six.viewkeys(_arg_keywords))
    NOARG_KEYWORDS = list(six.viewkeys(_noarg_keywords))
    COLON_KEYWORDS = list(six.viewkeys(_colon_keywords))
    ENDING_KEYWORDS = list(six.viewkeys(_ending_keywords))
    ALL_KEYWORDS = ARG_KEYWORDS + NOARG_KEYWORDS + COLON_KEYWORDS + ENDING_KEYWORDS

    # Palabras clave que tienen asociado una serie de cargos con nombres
    CARGOS_KEYWORDS = ['Nombramientos', 'Revocaciones', 'Ceses/Dimisiones', 'Reelecciones']

"""
    DICT_KEYWORDS = {kw: remove_accents(kw).replace(' del ', ' ').replace(' por ', ' ').replace(' de ', ' ')
                 .replace(' ', '_').replace('/', '_').replace('.', '_').lower() for kw in ALL_KEYWORDS}

>>> DICT_KEYWORDS.values()
[u'revocaciones', u'cambio_objeto_social', u'reelecciones', u'otros_conceptos', u'fe_erratas', u'sociedad_unipersonal', u'declaracion_unipersonalidad', u'constitucion', u'suspension_pagos', u'
perdida_caracter_unipersonalidad', u'cancelaciones_oficio_nombramientos', u'datos_registrales', u'cambio_domicilio_social', u'disolucion', u'ampliacion_objeto_social', u'cierre_provisional_hoj
a_registral_baja_en_el_indice_entidades_juridicas', u'ceses_dimisiones', u'nombramientos', u'situacion_concursal', u'modificaciones_estatutarias', u'ampliacion_capital', u'adaptacion_ley_2_95'
, u'cambio_denominacion_social', u'extincion', u'reduccion_capital', u'cambio_identidad_socio_unico', u'transformacion_sociedad', u'reapertura_hoja_registral', u'socio_unico', u'articulo_378_5
_reglamento_registro_mercantil', u'fusion_absorcion']
"""
