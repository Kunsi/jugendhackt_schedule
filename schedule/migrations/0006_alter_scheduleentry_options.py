# Generated by Django 4.2.1 on 2023-05-06 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0005_alter_event_acronym_alter_event_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="scheduleentry",
            options={"ordering": ["-start"]},
        ),
    ]
