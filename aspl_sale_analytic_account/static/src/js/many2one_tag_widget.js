odoo.define("aspl_sale_analytic_account.Many2OneTag", function (require) {
  "use strict";

  const field_registry = require("web.field_registry");
  const relational_fields = require("web.relational_fields");
  var core = require('web.core');
  var _t = core._t; 
  var qweb = core.qweb;

  const Many2OneTag = relational_fields.FieldMany2One.extend({

    _renderValueLines: function (needFirstLine) {
        const escapedValue = _.escape((this.m2o_value || "").trim());
        const lines = escapedValue.split('\n');
        if (!needFirstLine) {
            lines.shift();
        }
        return lines.map((line) => line ? qweb.render('aspl_sale_analytic_account.Many2oneColourTag', {line: line, color: this.record.data.color_anytic}) : `<span>${line}</span>`).join('<br/>');
    },

  });

  field_registry.add("many2one_tag", Many2OneTag);

  return Many2OneTag;
});
