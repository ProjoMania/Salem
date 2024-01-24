from odoo import models, fields, api

ones = [
    "", 
    "واحد ", 
    "اثنان ", 
    "ثلاثة ", 
    "اربعة ", 
    "خمسة ", 
    "ستة ", 
    "سبعة ", 
    "ثمانية ", 
    "تسعة ", 
    "عشرة ", 
    "احدي عشرة ",
    "اثنا عشرة ", 
    "ثلاثة عشرة ", 
    "أربعة عشرة ", 
    "خمسة عشرة ", 
    "ستة عشرة ", 
    "سبعة عشرة ", 
    "ثمانية عشرة ", 
    "تسعة عشرة "
]
ones_2 = [
    "", 
    "", 
    "", 
    "ثلاث", 
    "اربع", 
    "خمس", 
    "ست", 
    "سبع", 
    "ثماني", 
    "تسع"
]
twenties = [
    "", 
    "", 
    "عشرون ", 
    "ثلاثون ", 
    "اربعون ",
    "خمسون ", 
    "ستون ", 
    "سبعون ", 
    "ثمانون ", 
    "تسعون "
]
thousands = [
    "", 
    "الف ", 
    "مليون ", 
    "بليون ", 
    "تريليون "
]

def num2word(n):
    c = n % 10  # singles digit
    b = ((n % 100) - c) / 10  # tens digit
    a = ((n % 1000) - (b * 10) - c) / 100  # hundreds digit
    t = ""
    h = ""
    if a != 0 and b == 0 and c == 0:
        if ones[int(a)] == ones[1]:
            t = ones_2[int(a)] + "مائه "
        elif ones[int(a)] == ones[2]:
            t = "مئتان "
        else:
            t = ones_2[int(a)] + "مائه "

    elif a != 0:
        if ones[int(a)] == ones[1]:
            t = "مائه و "
        elif ones[int(a)] == ones[2]:
            t = "مئتان و "
        else:
            t = ones_2[int(a)] + "مائه و "
    if b <= 1:
        h = ones[n % 100]
    elif b > 1:
        if ones[int(c)]:
            h = ones[int(c)] + ' و ' + twenties[int(b)]
        else:
            h = twenties[int(b)]
    st = t + h
    return st


class ConvertNum2wordArabic(models.Model):
    _name = "convert.num2word.arabic"
    _description = 'Convert Num2word Arabic'

    def convert_arabic(self, input, currency):
        num = int(input)
        if num == 0: return 'صفر'
        i = 3
        n = str(num)
        word = ""
        k = 0
        while(i == 3):
            nw = n[-i:]
            n = n[:-i]
            if int(nw) == 0:
                word = num2word(int(nw)) + thousands[int(nw)] + word
            else:
                first_num = num2word(int(nw))
                if num < 11:
                    word = first_num
                elif first_num == ones[1] and k < 2:
                    if word:
                        word = ' و ' + word
                    word = thousands[int(k)] + word
                elif first_num == ones[2] and k < 2:
                    if word:
                        word = ' و ' + word
                    word = 'الفان ' + word
                elif first_num in ones[3:11] and k < 2:
                    if word:
                        word = ' و ' + word
                    word = first_num + 'آلاف ' + word
                else:
                    if word:
                        word = ' و ' + word
                    word = first_num + thousands[int(k)] + word
            if n == '':
                i = i+1
            k += 1

        input_fraction = input - num
        input_fraction = round(input_fraction,2)
        input_fraction = str(input_fraction)
        input_fraction = input_fraction[2:]
        word = ' فقط ' + word[:-1] + ' ' + str(currency.currency_unit_label)
        if input_fraction and int(input_fraction) != 0:
            input_fraction = ' و ' + num2word(int(input_fraction))
            return word + input_fraction +  str(currency.currency_subunit_label) + ' لاغير '  #  ' سنت ' +
        else:
            return word + ' لاغير '
