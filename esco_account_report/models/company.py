# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

from num2words import num2words
from decimal import Decimal


class ResCompany(models.Model):
    _inherit = "res.company"

    def get_amount_in_words(self, amount, currency, lang='ar_001'):
        if lang == 'ar_001':
            currency = currency.with_context(lang=lang)
            return self.env['convert.num2word.arabic'].convert_arabic(amount, currency)
        else:
            # print('currency.amount_to_text(amount)...', currency.amount_to_text(amount))
            # print('str(self.english_amoount_in_words(amount, currency, lang)).capitalize()..',
            #       str(self.english_amoount_in_words(amount, currency, lang)).capitalize())
            return currency.with_context(lang=lang).amount_to_text(amount)

    def arabic_amount_in_words(self, amount, currency, lang):
        return self.env['convert.num2word'].convert_number2word(
            amount=amount, lang_c=lang, currency=currency.name)

    def english_amoount_in_words(self, amount, currency, lang):
        amount_decimal = int(amount * 100 % 100)
        print('amount_decimal....', amount_decimal)
        # try:
        if True:
            lang = self.env['res.lang'].search([('iso_code', '=', lang)], limit=1)
            print("Lang = ", lang.code)
            unit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                      ('src', '=', currency.currency_unit_label)],
                                                     limit=1)

            subunit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                         ('src', '=',
                                                          currency.currency_subunit_label)],
                                                        limit=1)
            if not unit:
                src = self.env['ir.translation'].search([
                    ('value', '=', currency.currency_unit_label)], limit=1).src

                unit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                          ('src', '=', src)],
                                                         limit=1)
                if not unit:
                    unit = self.env['ir.translation'].search([('src', '=', src)], limit=1)
            if not subunit:
                src = self.env['ir.translation'].search([
                    ('value', '=', currency.currency_subunit_label)], limit=1).src

                subunit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                             ('src', '=', src)],
                                                            limit=1)
                if not subunit:
                    subunit = self.env['ir.translation'].search([('src', '=', src)], limit=1)

            print("Units = ", currency.currency_unit_label,
                  currency.currency_subunit_label)
            print("Units 2 = ", subunit.value, subunit.src)
            if unit and subunit and unit.value and subunit.value:
                print('if...amount, amount_decimal.', amount, amount_decimal)
                if amount and amount_decimal:
                    return num2words(Decimal(str(int(amount))), lang=lang) + ' ' + \
                                                (unit.value or unit.src) + ', ' + num2words(
                        Decimal(str(amount_decimal)),
                        lang=lang) + ' ' + (subunit.value or subunit.src)
                elif amount or not amount:
                    return num2words(Decimal(str(amount)), lang=lang) + ' ' + \
                                                (unit.value or unit.src)
                elif amount_decimal:
                    return num2words(Decimal(str(amount_decimal)),
                                                          lang=lang) + ' ' + (
                                                            subunit.value or subunit.src)

            elif currency.currency_unit_label and currency.currency_subunit_label:
                print('elif....amount, amount_decimal.', amount, amount_decimal, type(amount_decimal))
                if amount and amount_decimal:
                    print('if....Decimal(str(amount_decimal).', Decimal(str(amount_decimal)),
                          num2words(Decimal(str(amount_decimal))))
                    print(num2words(Decimal(str(int(amount)))))
                    print(currency.currency_unit_label)
                    print(num2words(Decimal(str(amount_decimal))))
                    print(currency.currency_subunit_label)
                    return num2words(Decimal(str(int(amount)))) + ' ' + (currency.currency_unit_label) + ', ' + \
                           num2words(Decimal(str(amount_decimal))) + ' ' + (currency.currency_subunit_label)
                elif amount or not amount:
                    return num2words(Decimal(str(amount))) + ' ' + \
                                                (currency.currency_unit_label)
                elif amount_decimal:
                    return num2words(Decimal(str(amount_decimal))) + ' ' + (
                                                    currency.currency_subunit_label)


            else:
                print('else....')
                return num2words(Decimal(str(amount)),
                                                      lang=lang) + ' ' + str(
                    currency.symbol)
        # except Exception as e:
        #     print('error:  %s', e)
        #     return num2words(Decimal(str(amount)), lang='en') + ' ' + str(
        #         currency.symbol)
        # else:
        #     print("22222222222222222222222222222")
        # return num2words(Decimal(str(amount)), lang=lang) + ' ' + str(currency.symbol)
