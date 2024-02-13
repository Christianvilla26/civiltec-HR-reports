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
        month_word = months[month].capitalize()

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
        month_word = months[month].capitalize()
        # Format the year to show only the last digit if necessary
        year_str = f"del {year}"
        # Combine into the required format
        formatted_date = f"hoy día {day_word} ({day}) del mes de {month_word} {year_str}."
        return formatted_date
    
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    

    desempeno = fields.Selection([
        ('excelente', 'Excelente'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
    ], string='Desempeño')

    funciones = fields.Text(string='Funciones')

    def get_elapsed_time_in_spanish(self):
        if not self.first_contract_date:
            return "Fecha no definida"
        
        first_contract_date = fields.Date.from_string(self.first_contract_date) if isinstance(self.first_contract_date, str) else self.first_contract_date
        today = fields.Date.context_today(self)
        
        # Calculate differences
        delta = today - first_contract_date
        total_days = delta.days
        years = total_days // 365
        months = (total_days % 365) // 30  # Approximation
        days = (total_days % 365) % 30  # Remaining days

        # Translate to Spanish
        years_str = f"{years} {'año' if years == 1 else 'años'}" if years else ""
        months_str = f"{months} {'mes' if months == 1 else 'meses'}" if months else ""
        days_str = f"{days} {'día' if days == 1 else 'días'}" if days else ""

        # Combine parts
        parts = [p for p in [years_str, months_str, days_str] if p]
        elapsed_time_spanish = ", ".join(parts)
        
        return elapsed_time_spanish or "Hoy"
    
    def get_formatted_current_date(self):
        today = datetime.today()  # Correct usage

        day = today.day
        month = today.month
        year = today.year

        # Define Spanish month names
        months = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        month_word = months[month].capitalize()
        # Format the year to show only the last digit if necessary
        year_str = f"del {year}"
        # Combine into the required format
        formatted_date = f"{day} de {month_word} {year_str}."
        return formatted_date
    
    def get_gender_title(self):
        if self.gender == 'female':
            return "Señora"
        else:
            return "Señor"