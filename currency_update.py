#! /usr/bin/env python
# -*-  coding: utf-8 -*-
import os,sys
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from applicationinstance import ApplicationInstance


from places.models import Currency


import logging
log = logging.getLogger('genel')










if __name__ == '__main__':
    o = None
    inst = None
    try:
        inst = ApplicationInstance( '/tmp/update_currency.pid' )

        Currency.updateRates()
        if inst:
            inst.exitApplication()
    except SystemExit:
        if inst:
            inst.exitApplication()
        pass
    except:
        if inst:
            inst.exitApplication()
        log.exception('beklenmeyen hata')

