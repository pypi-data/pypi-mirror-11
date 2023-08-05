#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .acto import ACTO
#from .download import download_pdf
from .download import get_url_pdf
#from .exceptions import BormeInvalidActoException
from .exceptions import BormeAlreadyDownloadedException, BormeAnuncioNotFound
from .regex import is_acto_cargo
#from .parser import parse as parse_borme
#from .seccion import SECCION
#from .provincia import PROVINCIA
import datetime
import logging
import json
import os
import six

from collections import OrderedDict

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.WARN)


class BormeActo(object):
    """
    Representa un Acto del Registro Mercantil. Instanciar BormeActoTexto o BormeActoCargo
    """
    def __init__(self, name, value):
        logger.debug('new %s(%s): %s' % (self.__class__.__name__, name, value))
        if name not in ACTO.ALL_KEYWORDS:
            logger.warning('Invalid acto found: %s' % name)
            #raise BormeInvalidActoException('Invalid acto found: %s' % acto_nombre)
        self._set_name(name)
        self._set_value(value)

    # TODO: @classmethod para elegir automaticamente el tipo?

    def _set_name(self, name):
        raise NotImplementedError

    def _set_value(self, value):
        raise NotImplementedError

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<%s(%s): %s>" % (self.__class__.__name__, self.name, self.value)


class BormeActoTexto(BormeActo):
    """
    Representa un Acto del Registro Mercantil con atributo de cadena de texto.
    """

    def _set_name(self, name):
        if is_acto_cargo(name):
            raise ValueError
        self.name = name

    def _set_value(self, value):
        if not isinstance(value, six.string_types):
            raise ValueError('value must be str: %s' % value)
        self.value = value


class BormeActoCargo(BormeActo):
    """
    Representa un Acto del Registro Mercantil con atributo de lista de cargos y nombres.
    """

    def _set_name(self, name):
        if not is_acto_cargo(name):
            raise ValueError
        self.name = name

    def _set_value(self, value):
        if not isinstance(value, dict):
            raise ValueError('value must be dict: %s' % value)

        for _, v in value.items():
            if not isinstance(v, set):
                raise ValueError('v must be set: %s' % v)

        self.value = value

    @property
    def cargos(self):
        return self.value

    def get_nombres_cargos(self):
        return list(self.value.keys())


class BormeAnuncio(object):
    """
    Representa un anuncio con un conjunto de actos mercantiles (Constitucion, Nombramientos, ...)
    """

    # TODO: Hay que copiar (copy()) mas atributos?? :|
    def __init__(self, id, empresa, actos):
        logger.debug('new BormeAnuncio(%s) %s' % (id, empresa))
        self.id = id
        self.empresa = empresa
        self.datos_registrales = ""
        self._set_actos(actos.copy())

    def _set_actos(self, actos):
        self.actos = []
        for acto_nombre, valor in actos.items():
            if acto_nombre == 'Datos registrales':
                self.datos_registrales = actos[acto_nombre]
                continue

            if is_acto_cargo(acto_nombre):
                a = BormeActoCargo(acto_nombre, valor)
                self.actos.append(a)
            else:
                a = BormeActoTexto(acto_nombre, valor)
                self.actos.append(a)

        try:
            del actos['Datos registrales']
        except KeyError:
            pass

    def get_borme_actos(self):
        return self.actos

    def get_actos(self):
        for acto in self.actos:
            if isinstance(acto, BormeActoTexto):
                yield acto.name, acto.value
            else:
                yield acto.name, acto.cargos

    def __repr__(self):
        return "<BormeAnuncio(%d) %s (%d)>" % (self.id, self.empresa, len(self.actos))


class BormeXML(object):
    pass


# TODO: Iterador de anuncios
# TODO: Info
# TODO: Create instance directly from filename
class Borme(object):

    def __init__(self, date, seccion, provincia, num, cve, anuncios=None, filename=None):
        if isinstance(date, tuple):
            date = datetime.date(year=date[0], month=date[1], day=date[2])
        self.date = date
        self.seccion = seccion
        self.provincia = provincia
        self.num = num
        self.cve = cve
        self.filename = filename
        self._parsed = False
        self.info = {}
        self._set_anuncios(anuncios)
        self._set_url()

    @classmethod
    def from_file(cls, filename):
        raise NotImplementedError

    def _set_anuncios(self, anuncios):
        self.anuncios = {}
        for anuncio in anuncios:
            self.anuncios[anuncio.id] = anuncio

    def _set_url(self):
        self.url = get_url_pdf(self.date, self.seccion, self.provincia)

    def get_info(self):
        #borme['info'] = {'pages': 5, 'anuncios': 38, 'fromanuncio': 12222, 'toanuncio': 12260}
        #return self.info
        raise NotImplementedError

    def get_anuncio(self, anuncio_id):
        try:
            return self.anuncios[anuncio_id]
        except KeyError:
            raise BormeAnuncioNotFound('Anuncio %d not found in BORME %s' % (anuncio_id, str(self)))

    def get_anuncios_ids(self):
        """
        [BormeAnuncio]
        """
        return list(self.anuncios.values())

    def get_anuncios(self):
        """
        [BormeAnuncio]
        """
        return list(self.anuncios.values())

    def download(self, filename):
        if self.filename is not None:
            raise BormeAlreadyDownloadedException(filename)
        downloaded = download_pdf(self.date, filename, self.seccion, self.provincia)
        if downloaded:
            self.filename = filename
        return downloaded

    def _to_json(self, filename):
        def set_default(obj):
            """ serialize Python sets as lists
                http://stackoverflow.com/a/22281062
            """
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        d = OrderedDict()
        d['cve'] = self.cve
        d['date'] = self.date.isoformat()
        d['seccion'] = self.seccion
        d['provincia'] = self.provincia
        d['num'] = self.num
        d['url'] = self.url
        d['filename'] = self.filename
        d['info'] = self.info
        d['anuncios'] = {}

        for id, anuncio in self.anuncios.items():
            d['anuncios'][anuncio.id] = OrderedDict()
            d['anuncios'][anuncio.id]['empresa'] = anuncio.empresa
            d['anuncios'][anuncio.id]['datos registrales'] = anuncio.datos_registrales
            d['anuncios'][anuncio.id]['actos'] = {}
            for acto in anuncio.actos:
                d['anuncios'][anuncio.id]['actos'][acto.name] = acto.value

        logger.debug(d)
        with open(filename, 'w') as fp:
            fp.write(json.dumps(d, default=set_default, indent=2))

    def to_json(self, filename, overwrite=True):
        if os.path.isfile(filename) and not overwrite:
            return False

        self._to_json(filename)
        return True

    @classmethod
    def from_json(self, filename):
        raise NotImplementedError

    def __repr__(self):
        return "<Borme(%s) seccion:%s provincia:%s>" % (self.date, self.seccion, self.provincia)
