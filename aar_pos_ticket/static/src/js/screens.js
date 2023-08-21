
/*
    License: OPL-1
    author: farooq@aarsol.com
*/
odoo.define('aar_pos_ticket.screens', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var _t = core._t;
    var gui = require('point_of_sale.gui');
    var qweb = core.qweb;

    var calculado;
    var recuperado;



    screens.ActionpadWidget.include({
        renderElement: function() {
            var self = this;
            this._super();




//                console.log(data)
//            });
            this.$('.pay').click(function(){


                console.log('hola desde pay');



                var order = self.pos.get_order();
                var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                    return line.has_valid_product_lot();
                });
                if(!has_valid_product_lot){
                    self.gui.show_popup('confirm',{
                        'title': _t('Empty Serial/Lot Number'),
                        'body':  _t('One or more product(s) required serial/lot number.'),
                        confirm: function(){
                            self.gui.show_screen('payment');
                        },
                    });
                }else{
                    self.gui.show_screen('payment');
                }
            });
            this.$('.set-customer').click(function(){
                self.gui.show_screen('clientlist');
            });

        }

    });

    screens.PaymentScreenWidget.include({

        renderElement: function() {
            var self = this;
            this._super();

            //var numpad = this.render_numpad();
            //numpad.appendTo(this.$('.payment-numpad'));



            this.render_paymentlines();

            this.$('.back').click(function(){
                self.click_back();
            });

            this.$('.next').click(function(){

                console.log('holaaa desde js');

                var ivan = "ivan";

                var order = self.pos.get('name');

                var id_cliente = "";




                self.validate_order();





            });

            this.$('.js_set_customer').click(function(){
                self.click_set_customer();
            });

            this.$('.js_tip').click(function(){
                self.click_tip();
            });
            this.$('.js_invoice').click(function(){
                self.click_invoice();
            });

            this.$('.js_cashdrawer').click(function(){
                self.pos.proxy.open_cashbox();
            });

        },

    });

    screens.ReceiptScreenWidget.include({

        renderElement: function () {


            var self = this;
            this._super();

            this.$('.button.print').click(function(){
                console.log('puta puta puta');

            });

            this.$('.back_order').click(function () {
                var order = self.pos.get_order();
                if (order) {
                    self.pos.gui.show_screen('products');
                }
            });
        },
        format_currency_2: function(amount){
            return amount.toFixed();

        },
        format_currency_puntos: function(amount){
            return amount;

        },
        format_currency_3: function(name,numfact){

            $.ajax({
                    type: 'GET',

                    data: {},
                    contextType: "application/json;charset=utf-8",
                    dateType: "json",
                    url: '/prueba/'+name+'/'+numfact,
                    success: function (response) {

                    }
                });

            return '';

        },

        format_currency_4: function(){
            var variable;
            $.ajax({


                    type: 'GET',

                    data: {},
                    contextType: "application/json;charset=utf-8",
                    dateType: "json",
                    url: '/prueba4/',
                    success: function (response) {

                    }
                });

            return '';

        },

        format_currency_5: function(){
            var variable;
            $.ajax({
                    type: 'GET',
                    data: {},
                    contextType: "application/json;charset=utf-8",
                    dateType: "json",
                    url: '/prueba5/',
                    success: function (response) {
                        variable = response
                        calculado = response
                    }

                });

            //return '';

        },
        get_numero_fac: function(numfact){
            var variable;
            console.log(" numfact - numfact - numfact");
            console.log(numfact);
            $.ajax({
                type: 'GET',
                data: {},
                contextType: "application/json;charset=utf-8",
                dateType: "json",
                url: '/prueba2023/'+numfact,
                success: function (response) {
                    variable = response
                }
            });
            return '';
        },
        get_numero_fac_2: function(numfact){
            var variable;
            console.log(" numfact - numfact - numfact");
            console.log(numfact);


            $.ajax({
                type: 'GET',
                data: {},
                contextType: "application/json;charset=utf-8",
                dateType: "json",
                url: '/prueba20232/'+numfact,
                success: function (response) {
                    if(response.enlatabla === false ){
                        console.log('entro response.enlatabla = false');
                        var facturanumeroynumero = 'Num. de Fact.:' + response.calculado;
                        document.getElementById('numerodefactura').innerHTML  = facturanumeroynumero;
                        //document.getElementById('numerodefactura').innerHTML  = response.calculado;
                        console.log(response.calculado);
                    } else {
                        console.log('entro else response.enlatabla = false');
                        var facturanumeroynumero = 'Num. de Fact.:' + response.enlatabla;
                        document.getElementById('numerodefactura2').innerHTML  = facturanumeroynumero;
                        //document.getElementById('numerodefactura2').innerHTML  = response.enlatabla;
                        console.log(response.enlatabla);
                    }



                }
            });
            //return '';
        },
        show: function () {
            this._super();
            try {
                JsBarcode("#barcode", this.pos.get('selectedOrder').ean13, {
                    format: "EAN13",
                    displayValue: true,
                    fontSize: 20
                });


                var a = document.getElementById('tttt');
                var b = document.getElementById('nana');

                $.ajax({
                    type: 'GET',
                    // data: {'valor': JSON.stringify(hola1)},
                    // data: {'valor': hola1 },
                    //data: {'valor': JSON.stringify(hola1)},
                    data: {},
                    contextType: "application/json;charset=utf-8",
                    dateType: "json",
                    url: '/prueba/'+a+'/'+b,
                    success: function (response) {
                        console.log('dentro del ajax');
                        console.log(response);
                        console.log('######');

                    }
                });

            } catch (error) {
            }
        },

    });

});
