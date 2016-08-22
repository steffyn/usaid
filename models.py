# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Actividadeseconomicas(models.Model):
    idactividadeconomica = models.AutoField(db_column='IdActividadEconomica', primary_key=True)  # Field name made lowercase.
    descripcionactividadeconomica = models.CharField(db_column='DescripcionActividadEconomica', max_length=255)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ActividadesEconomicas'


class Barrios(models.Model):
    idbarrio = models.AutoField(db_column='IdBarrio', primary_key=True)  # Field name made lowercase.
    iddepartamento = models.IntegerField(db_column='IdDepartamento')  # Field name made lowercase.
    idmunicipio = models.IntegerField(db_column='IdMunicipio')  # Field name made lowercase.
    idciudad = models.IntegerField(db_column='IdCiudad')  # Field name made lowercase.
    descripcionbarrio = models.CharField(db_column='DescripcionBarrio', max_length=250)  # Field name made lowercase.
    codigobarrio = models.CharField(db_column='CodigoBarrio', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Barrios'


class Boletas(models.Model):
    idboleta = models.AutoField(db_column='IdBoleta')  # Field name made lowercase.
    idestablecimiento = models.IntegerField(db_column='IdEstablecimiento')  # Field name made lowercase.
    numeroidentidad = models.CharField(db_column='NumeroIdentidad', max_length=13)  # Field name made lowercase.
    numeroexpediente = models.CharField(db_column='NumeroExpediente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idsexo = models.IntegerField(db_column='IdSexo')  # Field name made lowercase.
    edadanos = models.IntegerField(db_column='EdadAnos')  # Field name made lowercase.
    edadmeses = models.IntegerField(db_column='EdadMeses')  # Field name made lowercase.
    pseudonimo = models.CharField(db_column='Pseudonimo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idestadocivil = models.IntegerField(db_column='IdEstadoCivil')  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idocupacion = models.IntegerField(db_column='IdOcupacion')  # Field name made lowercase.
    iddepartamento = models.IntegerField(db_column='IdDepartamento')  # Field name made lowercase.
    idmunicipio = models.IntegerField(db_column='IdMunicipio')  # Field name made lowercase.
    calle = models.CharField(db_column='Calle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bloque = models.CharField(db_column='Bloque', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numerocasa = models.CharField(db_column='NumeroCasa', max_length=10, blank=True, null=True)  # Field name made lowercase.
    referencias = models.CharField(db_column='Referencias', max_length=500, blank=True, null=True)  # Field name made lowercase.
    idgrupoetnico = models.IntegerField(db_column='IdGrupoEtnico')  # Field name made lowercase.
    otrogrupoetnico = models.CharField(db_column='OtroGrupoEtnico', max_length=50, blank=True, null=True)  # Field name made lowercase.
    otropoblacion = models.CharField(db_column='OtroPoblacion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numeroidentidadmadre = models.CharField(db_column='NumeroIdentidadMadre', max_length=13, blank=True, null=True)  # Field name made lowercase.
    nombremadre = models.CharField(db_column='NombreMadre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefonomadre = models.CharField(db_column='TelefonoMadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numeroidentidadpadre = models.CharField(db_column='NumeroIdentidadPadre', max_length=13, blank=True, null=True)  # Field name made lowercase.
    nombrepadre = models.CharField(db_column='NombrePadre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefonopadre = models.CharField(db_column='TelefonoPadre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombretutor = models.CharField(db_column='NombreTutor', max_length=150, blank=True, null=True)  # Field name made lowercase.
    numeroidentidadtutor = models.CharField(db_column='NumeroIdentidadTutor', max_length=13, blank=True, null=True)  # Field name made lowercase.
    direcciontutor = models.CharField(db_column='DireccionTutor', max_length=500, blank=True, null=True)  # Field name made lowercase.
    telefonotutor = models.CharField(db_column='TelefonoTutor', max_length=13, blank=True, null=True)  # Field name made lowercase.
    idpoblacion = models.IntegerField(db_column='IdPoblacion', blank=True, null=True)  # Field name made lowercase.
    idactividadeconomica = models.IntegerField(db_column='IdActividadEconomica', blank=True, null=True)  # Field name made lowercase.
    fechaultimamenstruacion = models.CharField(db_column='FechaUltimaMenstruacion', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idciudad = models.IntegerField(db_column='IdCiudad', blank=True, null=True)  # Field name made lowercase.
    idbarrio = models.IntegerField(db_column='IdBarrio', blank=True, null=True)  # Field name made lowercase.
    creadopor = models.CharField(db_column='CreadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='ActualizadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion', blank=True, null=True)  # Field name made lowercase.
    rnp = models.NullBooleanField(db_column='RNP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Boletas'


class Boletasconsejeria(models.Model):
    idboletaconsejeria = models.AutoField(db_column='IdBoletaConsejeria')  # Field name made lowercase.
    idboleta = models.IntegerField(db_column='IdBoleta')  # Field name made lowercase.
    fechaconsejeria = models.CharField(db_column='FechaConsejeria', max_length=10, blank=True, null=True)  # Field name made lowercase.
    periodicidad = models.IntegerField(db_column='Periodicidad', blank=True, null=True)  # Field name made lowercase.
    nombrepersonasolicitante = models.CharField(db_column='NombrePersonaSolicitante', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nombredelconsejero = models.CharField(db_column='NombreDelConsejero', max_length=150, blank=True, null=True)  # Field name made lowercase.
    creadopor = models.CharField(db_column='CreadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='ActualizadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BoletasConsejeria'


class Boletasconsejeriapostprueba(models.Model):
    idboletaconsejeriapostprueba = models.AutoField(db_column='IdBoletaConsejeriaPostPrueba')  # Field name made lowercase.
    idboleta = models.IntegerField(db_column='IdBoleta')  # Field name made lowercase.
    fechaconsejeria = models.CharField(db_column='FechaConsejeria', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombredelconsejero = models.CharField(db_column='NombreDelConsejero', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creadopor = models.CharField(db_column='CreadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='ActualizadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion', blank=True, null=True)  # Field name made lowercase.
    referido = models.CharField(db_column='Referido', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BoletasConsejeriaPostPrueba'


class Boletasobservaciones(models.Model):
    idboletaobservacion = models.AutoField(db_column='IdBoletaObservacion', primary_key=True)  # Field name made lowercase.
    idboleta = models.IntegerField(db_column='IdBoleta')  # Field name made lowercase.
    idestablecimiento = models.IntegerField(db_column='IdEstablecimiento')  # Field name made lowercase.
    nombredelconsejero = models.CharField(db_column='NombreDelConsejero', max_length=150)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=255)  # Field name made lowercase.
    creadopor = models.CharField(db_column='CreadoPor', max_length=255)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion')  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='ActualizadoPor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion', blank=True, null=True)  # Field name made lowercase.
    tipoobservacion = models.IntegerField(db_column='TipoObservacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BoletasObservaciones'


class Boletaspruebas(models.Model):
    idboletaprueba = models.AutoField(db_column='IdBoletaPrueba', primary_key=True)  # Field name made lowercase.
    idboleta = models.IntegerField(db_column='IdBoleta')  # Field name made lowercase.
    fechasolicitud = models.CharField(db_column='FechaSolicitud', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numeroprueba = models.IntegerField(db_column='NumeroPrueba', blank=True, null=True)  # Field name made lowercase.
    fechaextraccion = models.CharField(db_column='FechaExtraccion', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechamuestra = models.CharField(db_column='FechaMuestra', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaprueba = models.CharField(db_column='FechaPrueba', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idkitpruebatamizaje = models.IntegerField(db_column='IdKitPruebaTamizaje', blank=True, null=True)  # Field name made lowercase.
    resultadopruebatamizaje = models.IntegerField(db_column='ResultadoPruebaTamizaje', blank=True, null=True)  # Field name made lowercase.
    nombrepersonaprueba = models.CharField(db_column='NombrePersonaPrueba', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fechapruebaconfirmatoria = models.CharField(db_column='FechaPruebaConfirmatoria', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idkitpruebaconfirmatoria = models.IntegerField(db_column='IdKitPruebaConfirmatoria', blank=True, null=True)  # Field name made lowercase.
    idinstitucionpruebaconfirmatoria = models.IntegerField(db_column='IdInstitucionPruebaConfirmatoria', blank=True, null=True)  # Field name made lowercase.
    resultadopruebaconfirmatoria = models.IntegerField(db_column='ResultadoPruebaConfirmatoria', blank=True, null=True)  # Field name made lowercase.
    nombrelaboratorio = models.CharField(db_column='NombreLaboratorio', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecharefiriopruebaconfirmatoria = models.CharField(db_column='FechaRefirioPruebaConfirmatoria', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creadopor = models.CharField(db_column='CreadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='ActualizadoPor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BoletasPruebas'


class Ciudades(models.Model):
    idciudad = models.AutoField(db_column='IdCiudad', primary_key=True)  # Field name made lowercase.
    iddepartamento = models.IntegerField(db_column='IdDepartamento')  # Field name made lowercase.
    idmunicipio = models.IntegerField(db_column='IdMunicipio')  # Field name made lowercase.
    descripcionciudad = models.CharField(db_column='DescripcionCiudad', max_length=250)  # Field name made lowercase.
    codigociudad = models.CharField(db_column='CodigoCiudad', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ciudades'


class Condiciones(models.Model):
    idcondicion = models.AutoField(db_column='IdCondicion', primary_key=True)  # Field name made lowercase.
    descripcioncondicion = models.CharField(db_column='DescripcionCondicion', max_length=255)  # Field name made lowercase.
    orden = models.IntegerField(db_column='Orden')  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Condiciones'


class Condicionesporboleta(models.Model):
    idcondicionporboleta = models.AutoField(db_column='IdCondicionPorBoleta')  # Field name made lowercase.
    idboleta = models.IntegerField(db_column='IdBoleta')  # Field name made lowercase.
    idcondicion = models.IntegerField(db_column='IdCondicion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CondicionesPorBoleta'


class Datos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    redsanitaria = models.CharField(db_column='RedSanitaria', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='Departamento', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    codigodepartamento = models.CharField(db_column='CodigoDepartamento', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    mapadepartamento = models.IntegerField(db_column='MapaDepartamento', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    codigomunicipio = models.CharField(db_column='CodigoMunicipio', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    mapamunicipio = models.IntegerField(db_column='MapaMunicipio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Datos'


class Departamentos(models.Model):
    iddepartamento = models.AutoField(db_column='IdDepartamento', primary_key=True)  # Field name made lowercase.
    descripciondepartamento = models.CharField(db_column='DescripcionDepartamento', max_length=50)  # Field name made lowercase.
    codigodepartamento = models.CharField(db_column='CodigoDepartamento', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamentos'


class Establecimientos(models.Model):
    idestablecimiento = models.AutoField(db_column='IdEstablecimiento', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    iddepartamento = models.IntegerField(db_column='IdDepartamento', blank=True, null=True)  # Field name made lowercase.
    idmunicipio = models.IntegerField(db_column='IdMunicipio', blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=500, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idtipodeestablecimiento = models.IntegerField(db_column='IdTipoDeEstablecimiento', blank=True, null=True)  # Field name made lowercase.
    idproveedor = models.IntegerField(db_column='IdProveedor', blank=True, null=True)  # Field name made lowercase.
    regionsanitaria = models.CharField(db_column='RegionSanitaria', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    publico = models.NullBooleanField(db_column='Publico')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Establecimientos'


class Estadosciviles(models.Model):
    idestadocivil = models.AutoField(db_column='IdEstadoCivil', primary_key=True)  # Field name made lowercase.
    descripcionestadocivil = models.CharField(db_column='DescripcionEstadoCivil', max_length=30)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EstadosCiviles'


class Gruposetnicos(models.Model):
    idgrupoetnico = models.AutoField(db_column='IdGrupoEtnico', primary_key=True)  # Field name made lowercase.
    descripciongrupoetnico = models.CharField(db_column='DescripcionGrupoEtnico', max_length=50)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GruposEtnicos'


class Municipios(models.Model):
    idmunicipio = models.AutoField(db_column='IdMunicipio', primary_key=True)  # Field name made lowercase.
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='IdDepartamento')  # Field name made lowercase.
    descripcionmunicipio = models.CharField(db_column='DescripcionMunicipio', max_length=50)  # Field name made lowercase.
    codigomunicipio = models.CharField(db_column='CodigoMunicipio', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Municipios'


class Ocupaciones(models.Model):
    idocupacion = models.AutoField(db_column='IdOcupacion', primary_key=True)  # Field name made lowercase.
    descripcionocupacion = models.CharField(db_column='DescripcionOcupacion', max_length=50)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ocupaciones'


class Opcionesmenu(models.Model):
    idopcion = models.AutoField(db_column='IdOpcion')  # Field name made lowercase.
    roleid = models.CharField(db_column='RoleId', max_length=100)  # Field name made lowercase.
    descripcionopcion = models.CharField(db_column='DescripcionOpcion', max_length=100)  # Field name made lowercase.
    numeroopcion = models.CharField(db_column='NumeroOpcion', max_length=10)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255, blank=True, null=True)  # Field name made lowercase.
    submenu = models.NullBooleanField(db_column='SubMenu')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OpcionesMenu'


class Periodicidades(models.Model):
    idperiodicidad = models.AutoField(db_column='IdPeriodicidad', primary_key=True)  # Field name made lowercase.
    descripcionperiodicidad = models.CharField(db_column='DescripcionPeriodicidad', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Periodicidades'


class Poblaciones(models.Model):
    idpoblacion = models.AutoField(db_column='IdPoblacion', primary_key=True)  # Field name made lowercase.
    descripcionpoblacion = models.CharField(db_column='DescripcionPoblacion', max_length=50)  # Field name made lowercase.
    orden = models.IntegerField(db_column='Orden')  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Poblaciones'


class Proveedores(models.Model):
    idproveedor = models.AutoField(db_column='IdProveedor')  # Field name made lowercase.
    descripcionproveedor = models.CharField(db_column='DescripcionProveedor', max_length=50)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Proveedores'


class Pruebas(models.Model):
    idprueba = models.AutoField(db_column='IdPrueba', primary_key=True)  # Field name made lowercase.
    descripcionprueba = models.CharField(db_column='DescripcionPrueba', max_length=255)  # Field name made lowercase.
    tipo = models.IntegerField(db_column='Tipo')  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pruebas'


class Rnp(models.Model):
    numeroidentidad = models.CharField(db_column='NumeroIdentidad', primary_key=True, max_length=13)  # Field name made lowercase.
    primernombre = models.CharField(db_column='PrimerNombre', max_length=50)  # Field name made lowercase.
    segundonombre = models.CharField(db_column='SegundoNombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=50)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechadenacimiento = models.CharField(db_column='FechaDeNacimiento', max_length=10)  # Field name made lowercase.
    idsexo = models.IntegerField(db_column='IdSexo')  # Field name made lowercase.
    idestadocivil = models.IntegerField(db_column='IdEstadoCivil')  # Field name made lowercase.
    fotografia = models.BinaryField(db_column='Fotografia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RNP'


class Responsables(models.Model):
    idresponsable = models.AutoField(db_column='IdResponsable', primary_key=True)  # Field name made lowercase.
    numeroidentidad = models.CharField(db_column='NumeroIdentidad', max_length=13)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=50)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechadenacimiento = models.CharField(db_column='FechaDeNacimiento', max_length=10)  # Field name made lowercase.
    idsexo = models.IntegerField(db_column='IdSexo')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usuariodesistema = models.CharField(db_column='UsuarioDeSistema', max_length=50)  # Field name made lowercase.
    idestablecimiento = models.IntegerField(db_column='IdEstablecimiento', blank=True, null=True)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Responsables'


class Sexos(models.Model):
    idsexo = models.AutoField(db_column='IdSexo', primary_key=True)  # Field name made lowercase.
    descripcionsexo = models.CharField(db_column='DescripcionSexo', max_length=20)  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sexos'


class Tiposdeestablecimientos(models.Model):
    idtipodeestablecimiento = models.AutoField(db_column='IdTipoDeEstablecimiento', primary_key=True)  # Field name made lowercase.
    descripciontipodeestablecimiento = models.CharField(db_column='DescripcionTipoDeEstablecimiento', max_length=50)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposDeEstablecimientos'


class AspnetApplications(models.Model):
    applicationname = models.CharField(db_column='ApplicationName', unique=True, max_length=256)  # Field name made lowercase.
    loweredapplicationname = models.CharField(db_column='LoweredApplicationName', unique=True, max_length=256)  # Field name made lowercase.
    applicationid = models.CharField(db_column='ApplicationId', primary_key=True, max_length=36)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Applications'


class AspnetMembership(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    userid = models.ForeignKey('AspnetUsers', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128)  # Field name made lowercase.
    passwordformat = models.IntegerField(db_column='PasswordFormat')  # Field name made lowercase.
    passwordsalt = models.CharField(db_column='PasswordSalt', max_length=128)  # Field name made lowercase.
    mobilepin = models.CharField(db_column='MobilePIN', max_length=16, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=256, blank=True, null=True)  # Field name made lowercase.
    loweredemail = models.CharField(db_column='LoweredEmail', max_length=256, blank=True, null=True)  # Field name made lowercase.
    passwordquestion = models.CharField(db_column='PasswordQuestion', max_length=256, blank=True, null=True)  # Field name made lowercase.
    passwordanswer = models.CharField(db_column='PasswordAnswer', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isapproved = models.BooleanField(db_column='IsApproved')  # Field name made lowercase.
    islockedout = models.BooleanField(db_column='IsLockedOut')  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    lastlogindate = models.DateTimeField(db_column='LastLoginDate')  # Field name made lowercase.
    lastpasswordchangeddate = models.DateTimeField(db_column='LastPasswordChangedDate')  # Field name made lowercase.
    lastlockoutdate = models.DateTimeField(db_column='LastLockoutDate')  # Field name made lowercase.
    failedpasswordattemptcount = models.IntegerField(db_column='FailedPasswordAttemptCount')  # Field name made lowercase.
    failedpasswordattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAttemptWindowStart')  # Field name made lowercase.
    failedpasswordanswerattemptcount = models.IntegerField(db_column='FailedPasswordAnswerAttemptCount')  # Field name made lowercase.
    failedpasswordanswerattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAnswerAttemptWindowStart')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Membership'


class AspnetPaths(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    pathid = models.CharField(db_column='PathId', primary_key=True, max_length=36)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=256)  # Field name made lowercase.
    loweredpath = models.CharField(db_column='LoweredPath', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Paths'
        unique_together = (('applicationid', 'loweredpath'),)


class AspnetPersonalizationallusers(models.Model):
    pathid = models.ForeignKey(AspnetPaths, models.DO_NOTHING, db_column='PathId', primary_key=True)  # Field name made lowercase.
    pagesettings = models.BinaryField(db_column='PageSettings')  # Field name made lowercase.
    lastupdateddate = models.DateTimeField(db_column='LastUpdatedDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_PersonalizationAllUsers'


class AspnetPersonalizationperuser(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    pathid = models.ForeignKey(AspnetPaths, models.DO_NOTHING, db_column='PathId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('AspnetUsers', models.DO_NOTHING, db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    pagesettings = models.BinaryField(db_column='PageSettings')  # Field name made lowercase.
    lastupdateddate = models.DateTimeField(db_column='LastUpdatedDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_PersonalizationPerUser'
        unique_together = (('pathid', 'userid'), ('userid', 'pathid'),)


class AspnetProfile(models.Model):
    userid = models.ForeignKey('AspnetUsers', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase.
    propertynames = models.TextField(db_column='PropertyNames')  # Field name made lowercase.
    propertyvaluesstring = models.TextField(db_column='PropertyValuesString')  # Field name made lowercase.
    propertyvaluesbinary = models.BinaryField(db_column='PropertyValuesBinary')  # Field name made lowercase.
    lastupdateddate = models.DateTimeField(db_column='LastUpdatedDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Profile'


class AspnetRoles(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    roleid = models.CharField(db_column='RoleId', primary_key=True, max_length=36)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', max_length=256)  # Field name made lowercase.
    loweredrolename = models.CharField(db_column='LoweredRoleName', max_length=256)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Roles'
        unique_together = (('applicationid', 'loweredrolename'),)


class AspnetSchemaversions(models.Model):
    feature = models.CharField(db_column='Feature', max_length=128)  # Field name made lowercase.
    compatibleschemaversion = models.CharField(db_column='CompatibleSchemaVersion', max_length=128)  # Field name made lowercase.
    iscurrentversion = models.BooleanField(db_column='IsCurrentVersion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_SchemaVersions'
        unique_together = (('feature', 'compatibleschemaversion'),)


class AspnetUsers(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    userid = models.CharField(db_column='UserId', primary_key=True, max_length=36)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=256)  # Field name made lowercase.
    loweredusername = models.CharField(db_column='LoweredUserName', max_length=256)  # Field name made lowercase.
    mobilealias = models.CharField(db_column='MobileAlias', max_length=16, blank=True, null=True)  # Field name made lowercase.
    isanonymous = models.BooleanField(db_column='IsAnonymous')  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Users'
        unique_together = (('applicationid', 'loweredusername'),)


class AspnetUsersinroles(models.Model):
    userid = models.ForeignKey(AspnetUsers, models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    roleid = models.ForeignKey(AspnetRoles, models.DO_NOTHING, db_column='RoleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_UsersInRoles'
        unique_together = (('userid', 'roleid'),)


class AspnetWebeventEvents(models.Model):
    eventid = models.CharField(db_column='EventId', primary_key=True, max_length=32)  # Field name made lowercase.
    eventtimeutc = models.DateTimeField(db_column='EventTimeUtc')  # Field name made lowercase.
    eventtime = models.DateTimeField(db_column='EventTime')  # Field name made lowercase.
    eventtype = models.CharField(db_column='EventType', max_length=256)  # Field name made lowercase.
    eventsequence = models.DecimalField(db_column='EventSequence', max_digits=19, decimal_places=0)  # Field name made lowercase.
    eventoccurrence = models.DecimalField(db_column='EventOccurrence', max_digits=19, decimal_places=0)  # Field name made lowercase.
    eventcode = models.IntegerField(db_column='EventCode')  # Field name made lowercase.
    eventdetailcode = models.IntegerField(db_column='EventDetailCode')  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    applicationpath = models.CharField(db_column='ApplicationPath', max_length=256, blank=True, null=True)  # Field name made lowercase.
    applicationvirtualpath = models.CharField(db_column='ApplicationVirtualPath', max_length=256, blank=True, null=True)  # Field name made lowercase.
    machinename = models.CharField(db_column='MachineName', max_length=256)  # Field name made lowercase.
    requesturl = models.CharField(db_column='RequestUrl', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    exceptiontype = models.CharField(db_column='ExceptionType', max_length=256, blank=True, null=True)  # Field name made lowercase.
    details = models.TextField(db_column='Details', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_WebEvent_Events'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
