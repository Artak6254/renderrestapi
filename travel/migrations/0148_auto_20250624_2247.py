from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0147_alter_tickets_ticket_type'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE travel_passengers
                ALTER COLUMN date_of_birth TYPE varchar(100)
                USING date_of_birth::text;
            """,
            reverse_sql="""
                ALTER TABLE travel_passengers
                ALTER COLUMN date_of_birth TYPE interval;
            """
        )
    ]

