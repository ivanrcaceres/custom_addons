# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    ruc = fields.Char(size=8, string="RUC")
    dv = fields.Char(string="DV", size=1)
    # nivel = fields.Integer(size=1)
    # nombre_fantasia = fields.Char(string="Nombre de fantasía")
    ci = fields.Char(string="CI")
    rucdv = fields.Char(string="RUC")
    # Retenciones para ficha de cliente
    # iva_retencion_10 = fields.Integer(string="Porcentaje de retención sobre el IVA 10%")
    # iva_retencion_5 = fields.Integer(string="Porcentaje de retención sobre el IVA 5%")

    # Timbrado de facturas para proveedores y vencimiento
    # timbrado = fields.Char(size=8, string="Timbrado")
    # vencimiento_timbrado = fields.Date(string="Vencimiento")
    # fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    # sexo = fields.Selection([('f', 'Femenino'), ('m', 'Masculino')])
    # digitointer = fields.Integer(string="RUC Internacional")
    # esinternacional = fields.Boolean()
    _sql_constraints = [

        # ('fantasia_unique',
        #  'UNIQUE(nombre_fantasia)',
        #  "El nombre de fantasía ya existe"),
        # ('ruc_unique',
        #  'UNIQUE(rucdv)',
        #  "El ruc ya existe"),
        ('ci_unique',
         'UNIQUE(ci)',
         "El nro de CI ya existe"),
    ]

    # @api.onchange('country_id')
    # def verificar_pais(self):
    #
    #     if (self.env.user.company_id.country_id != self.country_id):
    #         self.esinternacional = True
    #     else:
    #         self.esinternacional = False
    #
    #     if not (self.country_id):
    #         self.esinternacional = False

    @api.model
    def create(self, vals):
        if vals.get('ruc'):
            vals['ruc'] = vals.get('ruc').strip()
            ruc = vals.get('ruc').strip()
            dv = self.obtener_dv(ruc)
            vals['dv'] = self.obtener_dv(ruc)

            # if not vals.get('dv'):
            #     dv = self.obtener_dv(ruc)
            # else:
            #     dv = vals.get('dv')
            vals['rucdv'] = str(ruc) + '-' + str(dv)

        rec = super(Partner, self).create(vals)
        return rec

    @api.multi
    def write(self, vals):
        for partner in self:
            if vals.get('ruc'):
                vals['ruc'] = vals.get('ruc').strip()
                ruc = vals.get('ruc').strip()
                dv = self.obtener_dv(ruc)
                vals['dv'] = dv
            else:
                if partner.ruc:
                    ruc = partner.ruc
                    dv = self.obtener_dv(ruc)

            # if vals.get('dv'):
            #     dv= vals.get('dv')
            # else:
            #     if partner.dv:
            #         dv = partner.dv

        if vals.get('ruc'):
            vals['rucdv'] = str(ruc) + '-' + str(dv)

        rec = super(Partner, self).write(vals)
        return rec

    @api.onchange('ruc')
    def rucsi(self):
        if self.ruc:
            self.ruc = self.ruc.strip()
            self.dv = self.obtener_dv(self.ruc)

    @api.constrains('ruc')
    def verificar_duplicados(self):
        if self.ruc == '99999901' or self.ruc == '77777701' or not self.ruc:
            a = 1
        else:
            rucs = self.env['res.partner'].search([('ruc', '=', self.ruc)])
            if len(rucs) > 1:
                raise ValidationError('Ya se encuentra cargado un registro con ese RUC. Verifique datos')

    @api.multi
    def obtener_dv(self, ruc_c):

        ruc = ruc_c.strip()
        # ruc = '99999901'
        # lista1 = map(int, str(ruc))
        # lista = list(lista1)
        lista = list(str(ruc))
        # print(lista)
        k = 2
        suma = 0
        lista_final = list()

        for b in lista:
            if b == '-':
                raise ValidationError('Debe cargar RUC sin - o DV verificador')
            cod_as = ord(str.upper(b))
            if cod_as < 48 or cod_as > 57:
                for nume in list(str(cod_as)):
                    lista_final.append(nume)
            else:
                lista_final.append(b)

        # print(lista_final)
        for a in reversed(lista_final):
            # print(a)
            numero = int(a)
            suma += numero * k
            k += 1

        resto = suma % 11
        if resto > 1:
            dv = 11 - resto
        else:
            dv = 0

        return dv

        #
    # @api.onchange('ruc')
    # def _nivel_usu(self):
    #     if self.env.user.nivel == 5:
    #         self.nivel = self.env.user.nivel
    #     else:
    #         self.nivel = 2
    #
    # @api.constrains('ruc')
    # def _check_ruc(self):
    #     ruc = self.ruc;
    #     if not ruc[0] == "-":
    #         if len(ruc) <= 4:  # 4480040-1 347626-1 80012246-1
    #             raise exceptions.ValidationError("Favor verificar cantidad de digitos del RUC")
    #         else:
    #             if len(ruc) == 8:
    #                 if not ruc[6] == "-":
    #                     raise exceptions.ValidationError("No se ingreso correctamente el caracter '-' en el RUC")
    #             elif len(ruc) == 9:
    #                 if not ruc[7] == "-":
    #                     raise exceptions.ValidationError("No se ingreso correctamente el caracter '-' en el RUC")
    #             else:
    #                 if len(ruc) > 11:
    #                     raise exceptions.ValidationError("Cantidad de caracteres del RUC no puede ser mayor a 10")
    #                 else:
    #                     if len(ruc) == 10:
    #                         if not ruc[0] == "8":
    #                             raise exceptions.ValidationError("El primer digito del RUC debe empezar con 8")
    #                         elif not ruc[8] == "-":
    #                             raise exceptions.ValidationError(
    #                                 "No se ingreso correctamente el caracter '-' en el RUC")
    #     else:
    #         raise exceptions.ValidationError("No puede ser negativo")
    #
