import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from Applications.users.models import Acudiente, Jugador  # ajusta ruta a tu proyecto

def parse_bool(v):
    if v is None:
        return False
    v = str(v).strip().lower()
    return v in {"si", "sí", "true", "1", "y", "yes"}

def parse_date(v):
    if not v or str(v).strip() == "":
        return None
    from datetime import datetime
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(v).strip(), fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(str(v)).date()
    except Exception:
        raise CommandError(f"Fecha inválida: {v!r} (usa YYYY-MM-DD o DD/MM/YYYY)")

class Command(BaseCommand):
    help = "Importa jugadores desde un CSV normalizado. Usa acudiente_id (FK) y de forma opcional acudiente_identificacion como respaldo."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta al CSV de jugadores")

    def handle(self, *args, **opts):
        path = Path(opts["csv_path"])
        if not path.exists():
            raise CommandError(f"No existe: {path}")

        creados = actualizados = 0
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            # columnas mínimas requeridas (no exigimos acudiente_identificacion)
            required = {
                "nombre","apellido","tipo_doc","identificacion","fecha_nacimiento","ciudad_nacimiento",
                "direccion","ciudad","institucion_educativa","jornada_entreno","tiene_enfermedad",
                "tipo_enfermedad","tiene_contraindicacion","contacto_emergencia","num_contacto",
                "eps","parentesco","centro_atencion","pdf_doc_id","pdf_certificado_eps",
                "acudiente_id"  # ahora esta es la fuente principal para el FK
            }
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"Faltan columnas en el CSV: {sorted(missing)}")

            for row in reader:
                # 1) Resolver el acudiente (preferir acudiente_id; fallback a acudiente_identificacion si existiera)
                line = getattr(reader, "line_num", "desconocida")
                acu_id = None

                acu_id_raw = (row.get("acudiente_id") or "").strip()
                if acu_id_raw:
                    # validar que exista ese PK
                    try:
                        acu_id = int(acu_id_raw)
                    except ValueError:
                        raise CommandError(f"[línea {line}] acudiente_id inválido: {acu_id_raw!r}")

                    try:
                        # verificar existencia
                        Acudiente.objects.only("id").get(pk=acu_id)
                    except Acudiente.DoesNotExist:
                        raise CommandError(f"[línea {line}] acudiente_id no existe en Acudiente: {acu_id}")
                else:
                    # fallback opcional si tu CSV todavía trajera esta columna
                    doc = (row.get("acudiente_identificacion") or "").strip()
                    if not doc:
                        raise CommandError(
                            f"[línea {line}] Falta 'acudiente_id' y tampoco hay 'acudiente_identificacion'."
                        )
                    try:
                        acu_id = Acudiente.objects.values_list("id", flat=True).get(identificacion=doc)
                    except Acudiente.DoesNotExist:
                        raise CommandError(f"[línea {line}] Acudiente no encontrado para identificacion={doc!r}")

                # 2) Construir defaults del Jugador
                defaults = {
                    "nombre": (row["nombre"] or "").strip(),
                    "apellido": (row["apellido"] or "").strip(),
                    "tipo_doc": (row["tipo_doc"] or "").strip(),
                    "fecha_nacimiento": parse_date(row["fecha_nacimiento"]),
                    "ciudad_nacimiento": (row["ciudad_nacimiento"] or "").strip(),
                    "direccion": (row["direccion"] or "").strip(),
                    "ciudad": (row["ciudad"] or "").strip(),
                    "institucion_educativa": (row["institucion_educativa"] or "").strip(),
                    "jornada_entreno": (row["jornada_entreno"] or "").strip(),
                    "tiene_enfermedad": parse_bool(row["tiene_enfermedad"]),
                    "tipo_enfermedad": ((row.get("tipo_enfermedad") or "").strip() or None),
                    "tiene_contraindicacion": parse_bool(row["tiene_contraindicacion"]),
                    "contacto_emergencia": (row["contacto_emergencia"] or "").strip(),
                    "num_contacto": (row["num_contacto"] or "").strip(),
                    "eps": (row["eps"] or "").strip(),
                    "parentesco": (row["parentesco"] or "").strip(),
                    "centro_atencion": (row["centro_atencion"] or "").strip(),
                    "pdf_doc_id": (row["pdf_doc_id"] or "").strip(),
                    "pdf_certificado_eps": (row["pdf_certificado_eps"] or "").strip(),
                    "acudiente_id": acu_id,  # FK resuelto
                }

                obj, created = Jugador.objects.update_or_create(
                    identificacion=str(row["identificacion"]).strip(),
                    defaults=defaults,
                )
                creados += int(created)
                actualizados += int(not created)

        self.stdout.write(self.style.SUCCESS(
            f"Jugadores importados ✅  Creados: {creados} | Actualizados: {actualizados}"
        ))
