from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Acudiente(models.Model):
    id = models.AutoField(primary_key=True, db_column="idAcudiente")

    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        CE = "CE", "Cédula de extranjería"
        PA = "PA", "Pasaporte"
        PEP = "PEP", "Permiso especial de permanencia"
        OTRO = "OTRO", "Otro"

    class TipoRegimen(models.TextChoices):
        RESP_IVA = "RESP_IVA", "Responsable de IVA"
        NO_RESP_IVA = "NO_RESP_IVA", "No responsable de IVA"

    tipo_doc = models.CharField(max_length=20, db_column="tipoDoc",
                                choices=TipoDocumento.choices)
    identificacion = models.CharField(
        max_length=15,
        unique=True,
        validators=[MinLengthValidator(5)],
        help_text="Número de documento del acudiente.",
        db_column="identificacion",
    )
    nombre = models.CharField(max_length=45, db_column="nombre")
    apellidos = models.CharField(max_length=45, db_column="apellidos")
    ciudad = models.CharField(max_length=45, db_column="ciudad")
    direccion = models.CharField(max_length=100, db_column="direccion")
    telefono = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^[0-9+()\-\s]+$")],
        help_text="Incluye indicativo si aplica.",
        db_column="telefono",
    )
    correo = models.EmailField(max_length=120, db_column="correo")
    tipo_regimen = models.CharField(
        max_length=45,  # en MySQL es 45
        db_column="tipoRegimen",
        choices=TipoRegimen.choices,
    )

    class Meta:
        db_table = "Acudiente"

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.identificacion})"


class Jugador(models.Model):
    id = models.AutoField(primary_key=True, db_column="idJugador")

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

    nombre = models.CharField(max_length=45, db_column="nombre")
    apellido = models.CharField(max_length=45, db_column="apellido")
    tipo_doc = models.CharField(max_length=20, db_column="tipoDoc",
                                choices=TipoDocumento.choices)
    identificacion = models.CharField(max_length=15, db_column="identificacion",
                                      validators=[MinLengthValidator(5)])
    fecha_nacimiento = models.DateField(db_column="fechaNacimiento")
    ciudad_nacimiento = models.CharField(max_length=45, db_column="ciudadNacimiento")
    direccion = models.CharField(max_length=100, db_column="direccion")
    ciudad = models.CharField(max_length=45, db_column="ciudad")
    institucion_educativa = models.CharField(max_length=60, db_column="intitucionE")  # así viene en el dump
    jornada_entreno = models.CharField(max_length=15, db_column="jornadaEntreno",
                                       choices=Jornada.choices)
    # ENUM('Sí','No') -> booleanos Django
    tiene_enfermedad = models.BooleanField(default=False, db_column="enfermedad")
    tipo_enfermedad = models.CharField(max_length=45, blank=True, null=True, db_column="tipoEnfermedad")
    tiene_contraindicacion = models.BooleanField(default=False, db_column="contraindicacion")
    contacto_emergencia = models.CharField(max_length=45, db_column="contactoEmergencia")
    num_contacto = models.CharField(max_length=20, db_column="numContacto")  # teléfonos mejor como texto
    eps = models.CharField(max_length=15, db_column="eps")
    parentesco = models.CharField(max_length=30, db_column="parentesco")
    centro_atencion = models.CharField(max_length=45, db_column="centroAtencion")
    pdf_doc_id = models.CharField(max_length=100, db_column="pdfDocId")
    pdf_certificado_eps = models.CharField(max_length=100, db_column="pdfCertificadoEPS")

    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.PROTECT,
        related_name="jugadores",
        db_column="acudiente",
    )

    class Meta:
        db_table = "Jugador"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"