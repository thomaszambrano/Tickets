# Generated manually: revert M2M a relación 1:N Evento → TipoTicket

from django.db import migrations, models
import django.db.models.deletion


def _copiar_evento_desde_tabla_intermedia(apps, schema_editor):
    EventoTipoTicket = apps.get_model('eventos', 'EventoTipoTicket')
    TipoTicket = apps.get_model('eventos', 'TipoTicket')
    Evento = apps.get_model('eventos', 'Evento')

    primer_evento = Evento.objects.order_by('pk').first()
    for tt in TipoTicket.objects.filter(evento__isnull=True):
        par = (
            EventoTipoTicket.objects.filter(tipo_ticket_id=tt.pk)
            .order_by('pk')
            .first()
        )
        if par:
            tt.evento_id = par.evento_id
            tt.save(update_fields=['evento_id'])
        elif primer_evento:
            tt.evento_id = primer_evento.pk
            tt.save(update_fields=['evento_id'])


def _noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_lugar_latitud_lugar_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoticket',
            name='evento',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tipos_ticket',
                to='eventos.evento',
            ),
        ),
        migrations.RunPython(_copiar_evento_desde_tabla_intermedia, _noop),
        migrations.RemoveField(
            model_name='evento',
            name='tipos_ticket',
        ),
        migrations.DeleteModel(
            name='EventoTipoTicket',
        ),
        migrations.AlterField(
            model_name='tipoticket',
            name='evento',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tipos_ticket',
                to='eventos.evento',
            ),
        ),
    ]
