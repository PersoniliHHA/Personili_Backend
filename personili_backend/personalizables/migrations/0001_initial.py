# Generated by Django 5.0 on 2024-07-15 20:24

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("designs", "0001_initial"),
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image_path_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "departments",
            },
        ),
        migrations.CreateModel(
            name="DesignedPersonalizableVariant",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
            ],
            options={
                "db_table": "designed_personalizable_variants",
            },
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
            ],
            options={
                "db_table": "options",
            },
        ),
        migrations.CreateModel(
            name="PersonalizationType",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image_path_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "personalization_types",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "availability_status",
                    models.CharField(
                        choices=[
                            ("Available", "Available"),
                            ("Unavailable", "Unavailable"),
                            ("Hidden", "Hidden"),
                            ("ComingSoon", "ComingSoon"),
                        ],
                        default="Available",
                        max_length=255,
                    ),
                ),
                (
                    "image_path_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="personalizables.category",
                    ),
                ),
            ],
            options={
                "db_table": "categories",
            },
        ),
        migrations.CreateModel(
            name="DesignedPersonalizableZone",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("components", models.JSONField(blank=True, null=True)),
                (
                    "designed_personalizable_variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="designed_personalizable_variant_zone",
                        to="personalizables.designedpersonalizablevariant",
                    ),
                ),
            ],
            options={
                "db_table": "designed_personalizable_zones",
            },
        ),
        migrations.CreateModel(
            name="DesignedZoneRelatedDesign",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("dx1", models.FloatField(null=True)),
                ("dy1", models.FloatField(null=True)),
                ("dx2", models.FloatField(null=True)),
                ("dy2", models.FloatField(null=True)),
                (
                    "design",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bbbb",
                        to="designs.design",
                    ),
                ),
                (
                    "designed_personalizable_zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rrrr",
                        to="personalizables.designedpersonalizablezone",
                    ),
                ),
            ],
            options={
                "db_table": "designed_zone_related_designs",
            },
        ),
        migrations.CreateModel(
            name="OptionValue",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.CharField(max_length=255, null=True)),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="option_values",
                        to="personalizables.option",
                    ),
                ),
            ],
            options={
                "db_table": "option_values",
            },
        ),
        migrations.CreateModel(
            name="Personalizable",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "brand",
                    models.CharField(
                        default="Generic Brand", max_length=255, null=True
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        default="Generic Model", max_length=255, null=True
                    ),
                ),
                ("is_sponsored", models.BooleanField(default=False)),
                ("is_open_for_personalization", models.BooleanField(default=False)),
                ("can_be_template", models.BooleanField(default=False)),
                ("used_with_store_designs", models.BooleanField(default=False)),
                ("used_with_user_uploaded_designs", models.BooleanField(default=False)),
                ("used_with_same_workshop_designs", models.BooleanField(default=False)),
                (
                    "used_with_other_workshop_designs",
                    models.BooleanField(default=False),
                ),
                ("used_with_platform_designs", models.BooleanField(default=False)),
                (
                    "allowed_designs",
                    models.ManyToManyField(
                        related_name="personalizables", to="designs.design"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category",
                        to="personalizables.category",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="department",
                        to="personalizables.department",
                    ),
                ),
                (
                    "workshop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personalizables",
                        to="organizations.workshop",
                    ),
                ),
            ],
            options={
                "db_table": "personalizables",
            },
        ),
        migrations.CreateModel(
            name="PersonalizableOption",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personalizables",
                        to="personalizables.option",
                    ),
                ),
                (
                    "personalizable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="personalizables.personalizable",
                    ),
                ),
            ],
            options={
                "db_table": "personalizable_options",
            },
        ),
        migrations.CreateModel(
            name="PersonalizableVariant",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("quantity", models.IntegerField(default=1, null=True)),
                ("base_price", models.FloatField(default=0.0, null=True)),
                (
                    "personalizable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="personalizables.personalizable",
                    ),
                ),
            ],
            options={
                "db_table": "personalizable_variants",
            },
        ),
        migrations.AddField(
            model_name="designedpersonalizablevariant",
            name="personalizable_variant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="designed_personalizable_variant",
                to="personalizables.personalizablevariant",
            ),
        ),
        migrations.CreateModel(
            name="PersonalizableVariantValue",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "option_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variant_values",
                        to="personalizables.optionvalue",
                    ),
                ),
                (
                    "personalizable_option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variant_values",
                        to="personalizables.personalizableoption",
                    ),
                ),
                (
                    "personalizable_variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variant_values",
                        to="personalizables.personalizablevariant",
                    ),
                ),
            ],
            options={
                "db_table": "personalizable_variant_values",
            },
        ),
        migrations.CreateModel(
            name="PersonalizableZone",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                ("max_nb_designs", models.IntegerField(default=1, null=True)),
                ("x1", models.FloatField(null=True)),
                ("y1", models.FloatField(null=True)),
                ("x2", models.FloatField(null=True)),
                ("y2", models.FloatField(null=True)),
                (
                    "personalizable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zones",
                        to="personalizables.personalizable",
                    ),
                ),
            ],
            options={
                "db_table": "personalizable_zones",
            },
        ),
        migrations.AddField(
            model_name="designedpersonalizablezone",
            name="personalizable_zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="designed_personalizable_zone",
                to="personalizables.personalizablezone",
            ),
        ),
        migrations.CreateModel(
            name="PersonalizationMethod",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image_path_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_path_3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "personalization_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personalization_method",
                        to="personalizables.personalizationtype",
                    ),
                ),
            ],
            options={
                "db_table": "personalization_methods",
            },
        ),
    ]
