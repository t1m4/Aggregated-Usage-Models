import os
from itertools import chain

from django.core.management import BaseCommand
from django.db import connection

from wingtel.usage.utils import read_file_to_string

SQL_TRIGGERS = {}
SQL_PROCEDURES_NAMES = {"create_aggregated_object", "update_aggregated_object"}
SQL_PROCEDURES_FILENAMES = {"usage_triggers.sql"}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sql_functions_dir = "wingtel/usage/sql_functions/"
        procedures = []
        for procedure_filename in SQL_PROCEDURES_FILENAMES:
            procedures.append(read_file_to_string(os.path.join(sql_functions_dir, procedure_filename)))
        sql_script = "\n".join(chain(procedures))

        with connection.cursor() as cursor:
            cursor.execute(sql_script)
