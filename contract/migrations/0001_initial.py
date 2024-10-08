# Generated by Django 5.0.6 on 2024-09-18 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gouvernorat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomGouvernorat', models.CharField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomDelegation', models.CharField(max_length=100, null=True)),
                ('gouvernorat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.gouvernorat')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_facture', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('date_echeance', models.DateField()),
                ('service_description', models.TextField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taux_tva', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tva_montant', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status_paiement', models.CharField(blank=True, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], max_length=50, null=True)),
                ('methode_paiement', models.CharField(blank=True, choices=[('cash', 'Cash'), ('card', 'Card')], max_length=50, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Localite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomLocalite', models.CharField(max_length=100, null=True)),
                ('delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.delegation')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_abonnement', models.CharField(choices=[('SMART ADSL', 'SMART ADSL'), ('VDSL', 'VDSL'), ('SMART FIBRE', 'SMART FIBRE'), ('SMART RAPIDO', 'SMART RAPIDO')], max_length=100)),
                ('type_smart_rapido', models.CharField(blank=True, choices=[('SMART Rapido 20M GU TOPNET', 'SMART Rapido 20M GU TOPNET'), ('SMART Rapido 30M GU TOPNET', 'SMART Rapido 30M GU TOPNET'), ('SMART Rapido 50M GU TOPNET', 'SMART Rapido 50M GU TOPNET'), ('SMART Rapido 100M GU TOPNET', 'SMART Rapido 100M GU TOPNET'), ('SMART RAPIDO 20M (sans voix)', 'SMART RAPIDO 20M (sans voix)'), ('SMART RAPIDO 30M (sans voix)', 'SMART RAPIDO 30M (sans voix)'), ('SMART RAPIDO 50M (sans voix)', 'SMART RAPIDO 50M (sans voix)'), ('SMART RAPIDO 100M (sans voix)', 'SMART RAPIDO 100M (sans voix)'), ('PROMO SMART RAPIDO 20M (Sans Voix)', 'PROMO SMART RAPIDO 20M (Sans Voix)'), ('PROMO SMART RAPIDO 30M (Sans Voix)', 'PROMO SMART RAPIDO 30M (Sans Voix)'), ('PROMO SMART RAPIDO 50M (Sans Voix)', 'PROMO SMART RAPIDO 50M (Sans Voix)'), ('PROMO SMART RAPIDO 100M (Sans Voix)', 'PROMO SMART RAPIDO 100M (Sans Voix)'), ('Fidélité SMART RAPIDO 50M (sans voix)', 'Fidélité SMART RAPIDO 50M (sans voix)')], max_length=100, null=True)),
                ('type_smart_fibre', models.CharField(blank=True, choices=[('20M', '20M'), ('50M', '50M'), ('100M', '100M')], max_length=100, null=True)),
                ('type_smart_adsl', models.CharField(blank=True, choices=[('SMART ADSL 10M', 'SMART ADSL 10M'), ('SMART ADSL 12M', 'SMART ADSL 12M'), ('SMART ADSL 20M', 'SMART ADSL 20M')], max_length=100, null=True)),
                ('ville', models.CharField(max_length=100)),
                ('code_postal', models.CharField(max_length=20)),
                ('civilite', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Mlle', 'Mlle')], max_length=4)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('lieu_naissance', models.CharField(max_length=100)),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=10, null=True)),
                ('type_piece_identite', models.CharField(choices=[('CIN', 'CIN'), ('Passport', 'Passport')], max_length=20)),
                ('numero_piece_identite', models.CharField(max_length=50)),
                ('telephone_contact', models.CharField(max_length=20)),
                ('gsm_contact', models.CharField(max_length=20)),
                ('gsm_contact_2', models.CharField(blank=True, max_length=20, null=True)),
                ('adresse_installation', models.TextField()),
                ('coordonnees', models.CharField(blank=True, max_length=255, null=True)),
                ('cin_recto', models.ImageField(blank=True, null=True, upload_to='cin_recto/')),
                ('cin_verso', models.ImageField(blank=True, null=True, upload_to='cin_recto/verso/')),
                ('contrat_tt', models.ImageField(blank=True, null=True, upload_to='cin_recto/tt/')),
                ('contrat_topnet', models.ImageField(blank=True, null=True, upload_to='cin_recto/topnet/')),
                ('contrat_general_vente', models.ImageField(blank=True, null=True, upload_to='cin_recto/v/')),
                ('frequence_paiement', models.CharField(choices=[('1', '1 mois'), ('3', '3 mois'), ('6', '6 mois'), ('12', '12 mois')], max_length=2)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to=settings.AUTH_USER_MODEL)),
                ('delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.delegation')),
                ('gouvernorat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.gouvernorat')),
                ('localite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.localite')),
            ],
        ),
        migrations.CreateModel(
            name='CodePostal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codePostal', models.CharField(max_length=10, null=True)),
                ('localite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.localite')),
            ],
        ),
    ]
