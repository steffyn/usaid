# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boleta', '0012_auto_20160901_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boletasclinicas',
            name='biopsia_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='biopsia_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='buin_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='caviral_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='caviral_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='cultivo_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='cultivo_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='edes_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='estado_clinico',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='fluva_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepb_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='hepc_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='infpel_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='lic4_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='lic4_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='otro_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='otro_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ppd_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ppd_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='proc_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='rpr_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='rpr_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='rxtorax_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='rxtorax_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='secure_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='sespu_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='sespu_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='trasex_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tudi_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='tupu_trat',
            field=models.CharField(blank=True, choices=[('Isoniacida', 'Isoniacida'), ('Rifampicina', 'Rifampicina'), ('Pirazinamida', 'Pirazinamida'), ('Etambutol', 'Etambutol'), ('Estreptomicina', 'Estreptomicina')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='ulg_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='usg_fecha_realizacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Realizacion'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='usg_resultado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnostico'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_entrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Actualmente en Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_entrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_entrat_fecha_fintrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_entrat_fintrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Finalizo Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_fecha_initrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_intrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Interrumpio Tratamiento'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_intrat_diag',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_intrat_fecha_reitrat',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='boletasclinicas',
            name='verge_intrat_reitrat',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], null=True, verbose_name='Reinicio Tratamiento'),
        ),
    ]
