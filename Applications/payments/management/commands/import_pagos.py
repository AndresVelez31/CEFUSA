import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from Applications.payments.models import Pago
from Applications.users.models import Acudiente  # Asegúrate de que esta importación sea correcta

class Command(BaseCommand):
    help = 'Importa datos de pagos desde un archivo CSV a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta del archivo CSV a importar')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'El archivo "{csv_file_path}" no existe'))
            return

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            total_rows = 0
            imported_rows = 0
            skipped_rows = 0

            for row in reader:
                total_rows += 1
                try:
                    # Procesar campos numéricos
                    valor = float(row['valor'])
                    
                    # Procesar campos de fecha
                    fecha = datetime.strptime(row['fecha'], '%Y-%m-%d').date()
                    
                    # Procesar responsable (si existe)
                    responsable_id = row['responsable'].strip() if row['responsable'] else None
                    responsable = None
                    if responsable_id:
                        try:
                            responsable = Acudiente.objects.get(id=responsable_id)
                        except Acudiente.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f'Responsable con ID {responsable_id} no encontrado en fila {total_rows}'
                            ))
                    
                    # Crear el pago
                    pago = Pago(
                        cuenta=row['cuenta'],
                        fecha=fecha,
                        descripcion=row['descripcion'][:45],  # Asegurar que no exceda el límite
                        sucursal=row['sucursal'][:45],
                        referencia1=row['referencia1'][:45] if row['referencia1'] else None,
                        referencia2=row['referencia2'][:45] if row['referencia2'] else None,
                        valor=valor,
                        nombre=row['nombre'][:45],
                        motivo=row['motivo'][:50],
                        factura_venta=row['factura_venta'][:30] if row['factura_venta'] else None,
                        recibo_caja=row['recibo_caja'][:20] if row['recibo_caja'] else None,
                        comentario=row['comentario'][:150] if row['comentario'] else None,
                        responsable=responsable
                    )
                    
                    pago.save()
                    imported_rows += 1
                    
                except Exception as e:
                    skipped_rows += 1
                    self.stdout.write(self.style.ERROR(
                        f'Error en fila {total_rows}: {str(e)}. Datos: {row}'
                    ))

            self.stdout.write(self.style.SUCCESS(
                f'Proceso completado. Total filas: {total_rows}, '
                f'Importadas: {imported_rows}, '
                f'Omitidas: {skipped_rows}'
            ))