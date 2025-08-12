from django.db import models

class Pago(models.Model):
    id = models.AutoField(primary_key=True, db_column="idPago")

    class CuentaChoices(models.TextChoices):
        CUENTA_5031 = "5031", "5031"
        CUENTA_5032 = "5032", "5032"

    cuenta = models.CharField(
        max_length=4,
        db_column="cuenta",
        choices=[("5031", "5031"), ("5032", "5032")],
        default="5031",
    )


    fecha = models.DateField(db_column="fecha")
    descripcion = models.CharField(max_length=45, db_column="descripcion")
    sucursal = models.CharField(max_length=45, db_column="sucursal")
    referencia1 = models.CharField(max_length=45, blank=True, null=True, db_column="referencia1")
    referencia2 = models.CharField(max_length=45, blank=True, null=True, db_column="referencia2")

    valor = models.DecimalField(
        max_digits=12,  # hasta billones con 2 decimales
        decimal_places=2,
        default=0.00,
        db_column="valor"
    )

    nombre = models.CharField(max_length=45, db_column="nombre")
    motivo = models.CharField(max_length=50, db_column="motivo")
    factura_venta = models.CharField(max_length=30, blank=True, null=True, db_column="facturaVenta")
    recibo_caja = models.CharField(max_length=20, blank=True, null=True, db_column="reciboCaja")
    comentario = models.CharField(max_length=150, blank=True, null=True, db_column="comentario")

    responsable = models.ForeignKey(
        "users.Acudiente",
        on_delete=models.PROTECT,
        related_name="pagos",
        db_column="responsable",
        blank=True,
        null=True
    )

    class Meta:
        db_table = "Pago"

    def __str__(self):
        return f"Pago {self.id} - {self.fecha}"
