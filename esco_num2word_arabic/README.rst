================
esco_num2word_arabic
================


This module lets you convert amount to arabic

An example of XLSX report for partners on a module called `module_name`:

__________________________________________________
Example:
__________________________________________________

    def get_amount_in_words(self, amount, currency, lang='ar_001'):
        if lang == 'ar_001':
            currency = currency.with_context(lang=lang)
            return self.env['convert.num2word.arabic'].convert_arabic(amount, currency.name)

