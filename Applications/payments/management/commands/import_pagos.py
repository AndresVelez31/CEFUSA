import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from Applications.payments.models import Pago

CUENTAS_VALIDAS = {"5031", "5032"}

def _s(v):
    return "" if v is None else str(v).strip()

def _opt(v):
    v = _s(v)
    return v if v else None

def parse_date(v):
    """Acepta YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY o ISO."""
    from datetime import datetime
    v = _s(v)
    if not v:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(v).date()
    except Exception:
        return None

def parse_decimal(v, default=Decimal("0.00")):
    """
    Convierte a Decimal tolerando '1.234,56', '1,234.56', '5000', '-250000', etc.
    """
    v = _s(v)
    if not v:
        return default
    if "," in v and "." not in v:
        v = v.replace(".", "")
        v = v.replace(",", ".")
    else:
        v = v.replace(",", "")
    try:
        return Decimal(v)
    except InvalidOperation:
        return default

class Command(BaseCommand):
    help = "Importa pagos desde un CSV y crea SIEMPRE nuevos registros en Pago."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta al archivo CSV de pagos")
        parser.add_argument(
            "--default-sucursal",
            default="GENERAL",
            help="Valor por defecto para 'sucursal' cuando venga vacío (por defecto: GENERAL)",
        )

    def handle(self, *args, **opts):
        path = Path(opts["csv_path"])
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"No existe el archivo: {path}"))
            return

        sucursal_default = _s(opts.get("default_sucursal") or "GENERAL")[:45]

        creados = saltadas = errores = 0
        objs = []

        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            cols = set(reader.fieldnames or [])

            # Ahora solo exigimos estas columnas mínimas
            requeridas = {"fecha", "descripcion", "nombre"}
            faltantes = requeridas - cols
            if faltantes:
                self.stderr.write(self.style.ERROR(
                    f"Faltan columnas requeridas en el CSV: {sorted(faltantes)}"
                ))
                return

            for line_num, row in enumerate(reader, start=2):
                try:
                    fecha = parse_date(row.get("fecha"))
                    descripcion = _s(row.get("descripcion"))
                    nombre = _s(row.get("nombre"))

                    if not (fecha and descripcion and nombre):
                        self.stderr.write(self.style.WARNING(
                            f"[línea {line_num}] Saltada: faltan 'fecha', 'descripcion' o 'nombre'."
                        ))
                        saltadas += 1
                        continue

                    # Completar sucursal y motivo con defaults si vienen vacíos
                    sucursal = _s(row.get("sucursal")) or sucursal_default
                    sucursal = sucursal[:45]
                    motivo = _s(row.get("motivo")) or descripcion[:50]

                    # cuenta
                    cuenta = _s(row.get("cuenta"))
                    if not cuenta or cuenta not in CUENTAS_VALIDAS:
                        cuenta = Pago._meta.get_field("cuenta").get_default()

                    # valor
                    valor = parse_decimal(row.get("valor"), default=Decimal("0.00"))

                    # FK responsable (opcional)
                    responsable_id = _s(row.get("responsable_id"))
                    responsable_id = int(responsable_id) if responsable_id.isdigit() else None

                    objs.append(Pago(
                        cuenta=cuenta,
                        fecha=fecha,
                        descripcion=descripcion[:45],
                        sucursal=sucursal,
                        referencia1=_opt(row.get("referencia1")),
                        referencia2=_opt(row.get("referencia2")),
                        valor=valor,
                        nombre=nombre[:45],
                        motivo=motivo,
                        factura_venta=_opt(row.get("factura_venta")),
                        recibo_caja=_opt(row.get("recibo_caja")),
                        comentario=_opt(row.get("comentario")),
                        responsable_id=responsable_id,
                    ))

                except Exception as e:
                    errores += 1
                    self.stderr.write(self.style.ERROR(
                        f"[línea {line_num}] Error al procesar la fila: {e}"
                    ))

        if not objs:
            self.stderr.write(self.style.WARNING("No hay filas válidas para insertar."))
            return

        try:
            with transaction.atomic():
                Pago.objects.bulk_create(objs, batch_size=500)
                creados = len(objs)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error en bulk_create: {e}"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"Importación finalizada ✅  Creados: {creados} | Saltadas: {saltadas} | Errores: {errores}"
        ))
