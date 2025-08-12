# Script used for import "old" users to the new database
import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from Applications.users.models import Acudiente

class Command(BaseCommand):
    help = "Importa acudientes desde un CSV con encabezados: tipo_doc, identificacion, nombre, apellidos, ciudad, direccion, correo, telefono, tipo_regimen."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta al CSV")

    def handle(self, *args, **opts):
        path = Path(opts["csv_path"])
        if not path.exists():
            raise CommandError(f"No existe: {path}")

        creados = actualizados = 0
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj, created = Acudiente.objects.update_or_create(
                    identificacion=str(row["identificacion"]).strip(),
                    defaults={
                        "tipo_doc": str(row["tipo_doc"]).strip(),
                        "nombre": str(row["nombre"]).strip(),
                        "apellidos": str(row["apellidos"]).strip(),
                        "ciudad": str(row["ciudad"]).strip(),
                        "direccion": str(row["direccion"]).strip(),
                        "telefono": str(row["telefono"]).strip(),
                        "correo": str(row["correo"]).strip(),
                        "tipo_regimen": str(row["tipo_regimen"]).strip(),
                    },
                )
                creados += int(created)
                actualizados += int(not created)

        self.stdout.write(self.style.SUCCESS(
            f"Listo ✅  Creados: {creados} | Actualizados: {actualizados}"
        ))
