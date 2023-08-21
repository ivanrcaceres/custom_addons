odoo.define('pos_ruc_heredado', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var round_di = utils.round_decimals;
    var field_utils = require('web.field_utils');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var PosDb = require('point_of_sale.DB');

    models.load_fields('res.partner', ['rucdv', 'ruc', 'dv', 'ci']);


// var PosDB = core.Class.extend({
    PosDb.include({
        _partner_search_string: function (partner) {
            var str = partner.name;
            if (partner.barcode) {
                str += '|' + partner.barcode;
            }
            if (partner.address) {
                str += '|' + partner.address;
            }
            if (partner.phone) {
                str += '|' + partner.phone.split(' ').join('');
            }
            if (partner.mobile) {
                str += '|' + partner.mobile.split(' ').join('');
            }
            if (partner.email) {
                str += '|' + partner.email;
            }

            if (partner.rucdv) {
                str += '|' + partner.rucdv;

            }
            if (partner.ci) {
                str += '|' + partner.ci;

            }

            str = '' + partner.id + ':' + str.replace(':', '') + '\n';
            return str;

        },

        _product_search_string: function (product) {
            var str = product.display_name;
            if (product.barcode) {
                str += '|' + product.barcode;
            }
            if (product.default_code) {
                str += '|' + product.default_code;
            }
            if (product.description) {
                str += '|' + product.description;
            }
            if (product.description_sale) {
                str += '|' + product.description_sale;
            }
            str = product.id + ':' + str.replace(/:/g, '') + '\n';
            return str;
        },

    });

    models.Orderline = models.Orderline.extend({

        can_be_merged_with: function (orderline) {
            if (this.get_product().id !== orderline.get_product().id) {    //only orderline of the same product can be merged
                return false;
            } else if (!this.get_unit() || !this.get_unit().is_pos_groupable) {
                return false;
            } else if (this.get_product_type() !== orderline.get_product_type()) {
                return false;
            } else if (this.get_discount() > 0) {             // we don't merge discounted orderlines
                return false;
            } else if (!utils.float_is_zero(this.price - orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity()),
                this.pos.currency.decimals)) {
                console.log('mergeeee')
                if (this.get_unit().is_pos_groupable) {
                    return true;
                }

                return false;
            } else if (this.product.tracking == 'lot') {
                return false;
            } else {
                return true;
            }
        },
    });


});

