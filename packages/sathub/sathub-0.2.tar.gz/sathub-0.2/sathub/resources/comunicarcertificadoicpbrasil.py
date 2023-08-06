# -*- coding: utf-8 -*-
#
# sathub/resources/comunicarcertificadoicpbrasil.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from flask.ext import restful

from ..comum.util import hexdump
from ..comum.util import instanciar_funcoes_sat
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('certificado',
        type=str,
        required=True,
        help=u'Conteúdo do certificado digital ICP-Brasil')


class ComunicarCertificadoICPBRASIL(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        certificado = args['certificado']

        fsat = instanciar_funcoes_sat(numero_caixa)
        retorno = fsat.comunicar_certificado_icpbrasil(certificado)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "ComunicarCertificadoICPBRASIL" '
                    '(numero_caixa=%s)\n%s', numero_caixa, hexdump(retorno))

        return dict(funcao='ComunicarCertificadoICPBRASIL', retorno=retorno)
