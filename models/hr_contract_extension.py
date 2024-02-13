from odoo import models, fields
from datetime import datetime


class HrContract(models.Model):
    _inherit = "hr.contract"

    lawyer_name = fields.Char("Nombre del notario", help="The name of the lawyer.")
    lawyer_rnc = fields.Char("Carnet Del Notario", help="The RNC of the lawyer.")

    def day_to_spanish_word(self, day):
        # Basic mapping of numbers to their Spanish word equivalents
        words = {
            1: "uno",
            2: "dos",
            3: "tres",
            4: "cuatro",
            5: "cinco",
            6: "seis",
            7: "siete",
            8: "ocho",
            9: "nueve",
            10: "diez",
            11: "once",
            12: "doce",
            13: "trece",
            14: "catorce",
            15: "quince",
            16: "dieciséis",
            17: "diecisiete",
            18: "dieciocho",
            19: "diecinueve",
            20: "veinte",
            21: "veintiuno",
            22: "veintidós",
            23: "veintitrés",
            24: "veinticuatro",
            25: "veinticinco",
            26: "veintiséis",
            27: "veintisiete",
            28: "veintiocho",
            29: "veintinueve",
            30: "treinta",
            31: "treinta y uno",
        }
        return words.get(day, "")

    def get_formatted_wage(self):
        # Assuming 'wage' is a field on hr.contract, format it as needed
        return "{:,.2f}".format(self.wage)

    def number_to_words_es(self, number):
        def convert_hundred(number):
            units = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
            teens = ["diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve"]
            tens = ["", "diez", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
            hundreds = ["", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]

            if number < 10:
                return units[number]
            elif 10 <= number <= 19:
                return teens[number - 10]
            elif 20 <= number < 100:
                if number % 10 == 0:
                    return tens[number // 10]
                else:
                    return f"{tens[number // 10]} y {units[number % 10]}"
            elif 100 <= number < 1000:
                if number == 100:
                    return "cien"
                else:
                    return f"{hundreds[number // 100]} {convert_hundred(number % 100)}".strip()

        def convert_thousand(number):
            if number < 1000:
                return convert_hundred(number)
            elif 1000 <= number < 2000:
                return f"mil {convert_hundred(number % 1000)}".strip()
            elif 2000 <= number < 1000000:
                return f"{convert_hundred(number // 1000)} mil {convert_hundred(number % 1000)}".strip()

        if number == 0:
            return "cero"
        else:
            return convert_thousand(number).replace("  ", " ")


    def wage_to_words_es(self):
        wage = int(self.wage)  # Assuming self.wage is the monetary field
        return self.number_to_words_es(wage).upper()

    def get_current_date_formatted(self):
        # Use datetime.today() to get the current datetime object
        today = datetime.today()  # Correct usage

        day = today.day
        month = today.month
        year = today.year

        # Convert day to word using your method
        day_word = self.day_to_spanish_word(day)

        # Mapping or method for month in words
        months = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        month_word = months[month].upper()

        # Format and return the full date string as specified
        return f"a los {day_word} ({day}) del mes de {month_word} del {year}, en tres (3) originales, uno para cada una de las partes y los otros serán depositados en el Departamento de Trabajo para los fines legales correspondientes."

    def get_today_date_formatted(self):
    # Get today's date; consider using fields.Date.context_today(self) for timezone awareness in Odoo
        today = datetime.today()  # Correct usage

        day = today.day
        month = today.month
        year = today.year
        # Convert day and month to Spanish words; Utilizing existing day_to_spanish_word method
        day_word = self.day_to_spanish_word(day)

        # Define Spanish month names
        months = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        month_word = months[month].upper()
        # Format the year to show only the last digit if necessary
        year_str = f"del {year}"
        # Combine into the required format
        formatted_date = f"hoy día {day_word} ({day}) del mes de {month_word} {year_str}."
        return formatted_date   