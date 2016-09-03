# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 16:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boleta', '0009_auto_20160830_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoletasClinicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relaciones_mismo_sexo', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('dinero_por_relaciones', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('identificacion_genero', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('embarazada_vih', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fecha_ultima_menstruacion', models.DateField(blank=True, null=True)),
                ('semanas_gestiacion', models.IntegerField(blank=True, null=True)),
                ('evaluacion_go', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('programacion_cesaria', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fecha_cesaria', models.DateField(blank=True, null=True)),
                ('afiliacion_seguridad_social', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('clase_afiliacion', models.CharField(max_length=200, verbose_name='Clase de Afiliacion')),
                ('seguro_privado', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('nombre_aseguradora', models.CharField(max_length=200, verbose_name='Nombre de la Aseguradora Social')),
                ('fecha_diagnostico', models.DateField(blank=True, null=True)),
                ('fecha_primera_consulta', models.DateField(blank=True, null=True)),
                ('fecha_proxima_cita', models.DateField(blank=True, null=True)),
                ('cita_medica', models.CharField(blank=True, max_length=200, null=True)),
                ('retiro_medicamento', models.CharField(blank=True, max_length=200, null=True)),
                ('talla', models.CharField(blank=True, max_length=3, null=True)),
                ('peso', models.CharField(blank=True, max_length=3, null=True)),
                ('imc', models.CharField(blank=True, max_length=3, null=True)),
                ('estado_inmunologico', models.IntegerField(blank=True, choices=[(1, 'CD4<200'), (2, 'CD4=200-499'), (3, 'CD4>=500'), (4, 'N/A')], null=True)),
                ('estado_clinico', models.IntegerField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], null=True)),
                ('estadio_infeccion', models.CharField(blank=True, max_length=2, null=True)),
                ('lic4', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('lic4_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('lic4_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('lic4_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('caviral', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('caviral_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('caviral_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('caviral_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('hepb_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('hepb_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('hepb_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('hepc_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('hepc_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('hepc_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('rpr', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('rpr_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('rpr_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('rpr_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('rxtorax', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('rxtorax_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('rxtorax_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('rxtorax_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('sespu', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('sespu_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('sespu_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('sespu_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('ppd', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ppd_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('ppd_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('ppd_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('cultivo', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('cultivo_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('cultivo_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('cultivo_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('usg', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('usg_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('usg_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('usg_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('blopsia', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('blopsia_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('blopsia_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('blopsia_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('otro', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('otro_resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('otro_fecha_realizacion', models.DateField(blank=True, null=True)),
                ('otro_ordenado_consulta', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO'), (3, 'N/A')], null=True)),
                ('tupu', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_diag', models.DateField(blank=True, null=True)),
                ('tupu_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_fecha_initrat', models.DateField(blank=True, null=True)),
                ('tupu_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_entrat_diag', models.DateField(blank=True, null=True)),
                ('tupu_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('tupu_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_intrat_diag', models.DateField(blank=True, null=True)),
                ('tupu_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tupu_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('tupu_trat', models.IntegerField(blank=True, choices=[('Isoniacida', 'Isoniacida'), ('Rifampicina', 'Rifampicina'), ('Pirazinamida', 'Pirazinamida'), ('Etambutol', 'Etambutol'), ('Estreptomicina', 'Estreptomicina')], null=True)),
                ('tudi', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_diag', models.DateField(blank=True, null=True)),
                ('tudi_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_fecha_initrat', models.DateField(blank=True, null=True)),
                ('tudi_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_entrat_diag', models.DateField(blank=True, null=True)),
                ('tudi_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('tudi_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_intrat_diag', models.DateField(blank=True, null=True)),
                ('tudi_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('tudi_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('hepb', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_diag', models.DateField(blank=True, null=True)),
                ('hepb_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_fecha_initrat', models.DateField(blank=True, null=True)),
                ('hepb_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_entrat_diag', models.DateField(blank=True, null=True)),
                ('hepb_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('hepb_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_intrat_diag', models.DateField(blank=True, null=True)),
                ('hepb_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepb_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('hepc', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_diag', models.DateField(blank=True, null=True)),
                ('hepc_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_fecha_initrat', models.DateField(blank=True, null=True)),
                ('hepc_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_entrat_diag', models.DateField(blank=True, null=True)),
                ('hepc_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('hepc_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_intrat_diag', models.DateField(blank=True, null=True)),
                ('hepc_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('hepc_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('ulg', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_diag', models.DateField(blank=True, null=True)),
                ('ulg_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_fecha_initrat', models.DateField(blank=True, null=True)),
                ('ulg_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_entrat_diag', models.DateField(blank=True, null=True)),
                ('ulg_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('ulg_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_intrat_diag', models.DateField(blank=True, null=True)),
                ('ulg_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('ulg_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('secure', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_diag', models.DateField(blank=True, null=True)),
                ('secure_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_fecha_initrat', models.DateField(blank=True, null=True)),
                ('secure_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_entrat_diag', models.DateField(blank=True, null=True)),
                ('secure_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('secure_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_intrat_diag', models.DateField(blank=True, null=True)),
                ('secure_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('secure_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('fluva', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_diag', models.DateField(blank=True, null=True)),
                ('fluva_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_fecha_initrat', models.DateField(blank=True, null=True)),
                ('fluva_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_entrat_diag', models.DateField(blank=True, null=True)),
                ('fluva_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('fluva_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_intrat_diag', models.DateField(blank=True, null=True)),
                ('fluva_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('fluva_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('buin', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_diag', models.DateField(blank=True, null=True)),
                ('buin_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_fecha_initrat', models.DateField(blank=True, null=True)),
                ('buin_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_entrat_diag', models.DateField(blank=True, null=True)),
                ('buin_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('buin_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_intrat_diag', models.DateField(blank=True, null=True)),
                ('buin_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('buin_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('edes', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_diag', models.DateField(blank=True, null=True)),
                ('edes_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_fecha_initrat', models.DateField(blank=True, null=True)),
                ('edes_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_entrat_diag', models.DateField(blank=True, null=True)),
                ('edes_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('edes_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_intrat_diag', models.DateField(blank=True, null=True)),
                ('edes_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('edes_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('verge', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_diag', models.DateField(blank=True, null=True)),
                ('verge_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_fecha_initrat', models.DateField(blank=True, null=True)),
                ('verge_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_entrat_diag', models.DateField(blank=True, null=True)),
                ('verge_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('verge_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_intrat_diag', models.DateField(blank=True, null=True)),
                ('verge_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('verge_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('trasex', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_diag', models.DateField(blank=True, null=True)),
                ('trasex_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_fecha_initrat', models.DateField(blank=True, null=True)),
                ('trasex_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_entrat_diag', models.DateField(blank=True, null=True)),
                ('trasex_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('trasex_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_intrat_diag', models.DateField(blank=True, null=True)),
                ('trasex_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('trasex_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('proc', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_diag', models.DateField(blank=True, null=True)),
                ('proc_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_fecha_initrat', models.DateField(blank=True, null=True)),
                ('proc_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_entrat_diag', models.DateField(blank=True, null=True)),
                ('proc_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('proc_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_intrat_diag', models.DateField(blank=True, null=True)),
                ('proc_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('proc_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('infpel', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_diag', models.DateField(blank=True, null=True)),
                ('infpel_initrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_fecha_initrat', models.DateField(blank=True, null=True)),
                ('infpel_entrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_entrat_diag', models.DateField(blank=True, null=True)),
                ('infpel_entrat_fintrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_entrat_fecha_fintrat', models.DateField(blank=True, null=True)),
                ('infpel_intrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_intrat_diag', models.DateField(blank=True, null=True)),
                ('infpel_intrat_reitrat', models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True)),
                ('infpel_intrat_fecha_reitrat', models.DateField(blank=True, null=True)),
                ('boleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boleta.Boletas')),
            ],
        ),
        migrations.AddField(
            model_name='asistencia',
            name='actualizado_por',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='actualizado_por_asistencia', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='creado_por',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='creado_por_asistencia', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='actividad',
            field=models.CharField(max_length=200, verbose_name='Actividad/Tema'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='coordinador',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del/la Coordinador de Proyecto'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='establecimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Establecimientos', verbose_name='ONG Implementadora'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='intervencion',
            field=models.IntegerField(choices=[(1, 'Proveer o referir a Servicios de Consejeria y Prueba'), (2, 'Promocion y Distribucion de Condones y Lubricantes'), (3, 'Referencia a Tamizaje, Prevencion y Tratamiento de ITS'), (4, 'Difusion/Alcance y Empoderamiento'), (5, 'Abordaje para IEC'), (6, 'Referencia Salud Reproductiva (Planificacion Familiar)')], verbose_name='Tipo de Intervensi\xf3n'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='poblacion',
            field=models.IntegerField(choices=[(1, 'MTS'), (2, 'HSH/TG')], verbose_name='Tipo de Poblaci\xf3n Clave Atendida'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='responsable',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del/la Responsable de la Actividad'),
        ),
    ]
