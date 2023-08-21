# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Car(models.Model):
    _name = 'odoo_model_advanced.car'
    _description = 'Coche'

    name = fields.Char(string='Modelo')
    number_plate = fields.Char(string='Matrícula')
    cv = fields.Float(string='CV')
    colour = fields.Char(string='Color')
    fuel_litres = fields.Float(string='Litros')

    def validate(self):
        if True: #Condición que deben cumplir los datos introducidos por el usuario
            raise exceptions.RedirectWarning('Se deberá especificar la matrícula del vehículo')













