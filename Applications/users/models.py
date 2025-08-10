from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

# Create your models here.

class Acudiente(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        CE = "CE", "Cédula de extranjería"
        PA = "PA", "Pasaporte"
        PEP = "PEP", "Permiso especial de permanencia"
        OTRO = "OTRO", "Otro"

    class TipoRegimen(models.TextChoices):
        RESP_IVA = "RESP_IVA", "Responsable de IVA"
        NO_RESP_IVA = "NO_RESP_IVA", "No responsable de IVA"

    # id automático (AutoField/BigAutoField según settings)
    tipo_doc = models.CharField(max_length=10, choices=TipoDocumento.choices)
    identificacion = models.CharField(
        max_length=15,
        unique=True,
        validators=[MinLengthValidator(5)],
        help_text="Número de documento del acudiente."
    )
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    ciudad = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^[0-9+()\-\s]+$")],
        help_text="Incluye indicativo si aplica."
    )
    correo = models.EmailField(max_length=120)
    tipo_regimen = models.CharField(max_length=12, choices=TipoRegimen.choices)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.identificacion})"


class Jugador(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        TI = "TI", "Tarjeta de identidad"
        RC = "RC", "Registro civil"
        PA = "PA", "Pasaporte"
        TEP = "TEP", "Tarjeta especial de permanencia"
        TE = "TE", "Tarjeta de extranjería"

    class Jornada(models.TextChoices):
        MANANA = "MANANA", "Mañana"
        TARDE = "TARDE", "Tarde"

    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    tipo_doc = models.CharField(max_length=10, choices=TipoDocumento.choices)
    identificacion = models.CharField(max_length=15, validators=[MinLengthValidator(5)])
    fecha_nacimiento = models.DateField()
    ciudad_nacimiento = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=45)
    institucion_educativa = models.CharField(max_length=60)
    jornada_entreno = models.CharField(max_length=10, choices=Jornada.choices)
    # Mejor como booleanos en Django:
    tiene_enfermedad = models.BooleanField(default=False)
    tipo_enfermedad = models.CharField(max_length=45, blank=True, null=True)
    tiene_contraindicacion = models.BooleanField(default=False)
    contacto_emergencia = models.CharField(max_length=45)
    num_contacto = models.CharField(max_length=20)  # teléfonos como texto
    eps = models.CharField(max_length=30)
    parentesco = models.CharField(max_length=30)
    centro_atencion = models.CharField(max_length=45)
    pdf_doc_id = models.CharField(max_length=150)          # podrías migrar a FileField más adelante
    pdf_certificado_eps = models.CharField(max_length=150) # idem
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.PROTECT,
        related_name="jugadores"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"