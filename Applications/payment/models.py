from django.db import models

class Payment(models.Model):
    id = models.AutoField(primary_key=True, db_column="idPago")

    class AccountChoices(models.TextChoices):
        ACCOUNT_5031 = "5031", "5031"
        ACCOUNT_5032 = "5032", "5032"

    account = models.CharField(
        max_length=4,
        db_column="cuenta",
        choices=[("5031", "5031"), ("5032", "5032")],
        default="5031",
    )


    date = models.DateField(db_column="fecha")
    description = models.CharField(max_length=45, db_column="descripcion")
    branch = models.CharField(max_length=45, db_column="sucursal")
    reference_1 = models.CharField(max_length=45, blank=True, null=True, db_column="referencia1")
    reference_2 = models.CharField(max_length=45, blank=True, null=True, db_column="referencia2")

    amount = models.DecimalField(
        max_digits=12,  # up to billions with 2 decimals
        decimal_places=2,
        default=0.00,
        db_column="valor"
    )

    player_name = models.CharField(max_length=45, db_column="nombre")
    reason = models.CharField(max_length=50, db_column="motivo")
    sales_invoice = models.CharField(max_length=30, blank=True, null=True, db_column="facturaVenta")
    receipt = models.CharField(max_length=20, blank=True, null=True, db_column="reciboCaja")
    comment = models.CharField(max_length=150, blank=True, null=True, db_column="comentario")

<<<<<<< HEAD:Applications/payment/models.py
    responsible = models.ForeignKey(
        "user.Guardian",
=======
    fk_responsible = models.ForeignKey(
        "user.Guardian",  # Updated to match the renamed model
        on_delete=models.PROTECT,
        related_name="payment",
        db_column="responsable",
        blank=True,
        null=True
    )

    class Meta:
        db_table = "Pago"

    def __str__(self):
        return f"Payment {self.id} - {self.date}"