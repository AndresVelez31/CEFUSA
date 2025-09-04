from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Guardian(models.Model):
    id = models.AutoField(primary_key=True, db_column="idAcudiente")

    class DocumentType(models.TextChoices):
        CC = "Cédula de ciudadanía", "Cédula de ciudadanía"
        CE = "Cédula de extranjería", "Cédula de extranjería"
        PA = "Pasaporte", "Pasaporte"
        PEP = "Permiso especial de permanencia", "Permiso especial de permanencia"
        OTHER = "Otro", "Otro"

    class RegimeType(models.TextChoices):
        IVA_RESPONSIBLE = "Responsable de IVA", "Responsable de IVA"
        NOT_IVA_RESPONSIBLE = "No responsable de IVA", "No responsable de IVA"

    document_type = models.CharField(
        max_length=31, 
        db_column="tipoDoc",
        choices=DocumentType.choices)
    
    identification = models.CharField(
        max_length=15,
        unique=True,
        validators=[MinLengthValidator(5)],
        help_text="Número de documento del acudiente.",
        db_column="identificacion",
    )
    first_name = models.CharField(max_length=45, db_column="nombre")
    last_name = models.CharField(max_length=45, db_column="apellidos")
    city = models.CharField(max_length=45, db_column="ciudad")
    address = models.CharField(max_length=100, db_column="direccion")
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^[0-9+()\-\s]+$")],
        help_text="Incluye indicativo si aplica.",
        db_column="telefono",
    )
    email = models.EmailField(max_length=120, db_column="correo")
    regime_type = models.CharField(
        max_length=45,  # en MySQL es 45
        db_column="tipoRegimen",
        choices=RegimeType.choices,
    )

    class Meta:
        db_table = "Acudiente"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.identification})"


class Player(models.Model):
    id = models.AutoField(primary_key=True, db_column="idJugador")

    class DocumentType(models.TextChoices):
        CC = "Cédula de ciudadanía", "Cédula de ciudadanía"
        TI = "Tarjeta de identidad", "Tarjeta de identidad"
        RC = "Registro civil", "Registro civil"
        PA = "Pasaporte", "Pasaporte"
        TEP = "Tarjeta especial de permanencia", "Tarjeta especial de permanencia"
        TE = "Tarjeta de extranjería", "Tarjeta de extranjería"

    class TrainingSession(models.TextChoices):
        MORNING = "Mañana", "Mañana"
        AFTERNOON = "Tarde", "Tarde"

    first_name = models.CharField(max_length=45, db_column="nombre")
    last_name = models.CharField(max_length=45, db_column="apellido")
    document_type = models.CharField(max_length=31, db_column="tipoDoc",
                                choices=DocumentType.choices)
    identification = models.CharField(max_length=15, db_column="identificacion",
                                      validators=[MinLengthValidator(5)])
    birth_date = models.DateField(db_column="fechaNacimiento")
    birth_city = models.CharField(max_length=45, db_column="ciudadNacimiento")
    address = models.CharField(max_length=100, db_column="direccion")
    city = models.CharField(max_length=45, db_column="ciudad")
    educational_institution = models.CharField(max_length=60, db_column="intitucionE")  # así viene en el dump
    training_session = models.CharField(max_length=15, db_column="jornadaEntreno",
                                       choices=TrainingSession.choices)
    # ENUM('Sí','No') -> booleanos Django
    has_disease = models.BooleanField(default=False, db_column="enfermedad")
    disease_type = models.CharField(max_length=45, blank=True, null=True, db_column="tipoEnfermedad")
    has_contraindication = models.BooleanField(default=False, db_column="contraindicacion")
    emergency_contact = models.CharField(max_length=45, db_column="contactoEmergencia")
    contact_number = models.CharField(max_length=20, db_column="numContacto")  # teléfonos mejor como texto
    eps = models.CharField(max_length=15, db_column="eps")
    relationship = models.CharField(max_length=30, db_column="parentesco")
    care_center = models.CharField(max_length=45, db_column="centroAtencion")
    pdf_doc_id = models.CharField(max_length=100, db_column="pdfDocId")
    pdf_eps_certificate = models.CharField(max_length=100, db_column="pdfCertificadoEPS")

    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.PROTECT,
        related_name="players",
        db_column="acudiente",
    )

    class Meta:
        db_table = "Jugador"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"