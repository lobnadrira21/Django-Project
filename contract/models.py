from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class Gouvernorat(models.Model):
    nomGouvernorat = models.CharField(max_length=100, unique=True,null=True)

    def __str__(self):
        return self.nomGouvernorat

class Delegation(models.Model):
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE)
    nomDelegation = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.nomDelegation

class Localite(models.Model):
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    nomLocalite = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.nomLocalite

class CodePostal(models.Model):
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    codePostal = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.codePostal
class Contract(models.Model):
    
    TYPE_ABONNEMENT_CHOICES = [
        ('SMART ADSL', 'SMART ADSL'),
        ('VDSL', 'VDSL'),
        ('SMART FIBRE', 'SMART FIBRE'),
        ('SMART RAPIDO', 'SMART RAPIDO')
    ]
    SMART_ADSL= [
        ('SMART ADSL 10M','SMART ADSL 10M'),
        ('SMART ADSL 12M','SMART ADSL 12M'),
        ('SMART ADSL 20M','SMART ADSL 20M'),
    ]
    SMART_RAPIDO_CHOICES = [
        ('SMART Rapido 20M GU TOPNET', 'SMART Rapido 20M GU TOPNET'),
        ('SMART Rapido 30M GU TOPNET', 'SMART Rapido 30M GU TOPNET'),
        ('SMART Rapido 50M GU TOPNET', 'SMART Rapido 50M GU TOPNET'),
        ('SMART Rapido 100M GU TOPNET', 'SMART Rapido 100M GU TOPNET'),
        ('SMART RAPIDO 20M (sans voix)', 'SMART RAPIDO 20M (sans voix)'),
        ('SMART RAPIDO 30M (sans voix)', 'SMART RAPIDO 30M (sans voix)'),
        ('SMART RAPIDO 50M (sans voix)', 'SMART RAPIDO 50M (sans voix)'),
        ('SMART RAPIDO 100M (sans voix)', 'SMART RAPIDO 100M (sans voix)'),
        ('PROMO SMART RAPIDO 20M (Sans Voix)', 'PROMO SMART RAPIDO 20M (Sans Voix)'),
        ('PROMO SMART RAPIDO 30M (Sans Voix)', 'PROMO SMART RAPIDO 30M (Sans Voix)'),
        ('PROMO SMART RAPIDO 50M (Sans Voix)', 'PROMO SMART RAPIDO 50M (Sans Voix)'),
        ('PROMO SMART RAPIDO 100M (Sans Voix)', 'PROMO SMART RAPIDO 100M (Sans Voix)'),
        ('Fidélité SMART RAPIDO 50M (sans voix)', 'Fidélité SMART RAPIDO 50M (sans voix)')
    ]
    SMART_FIBRE = [
        ('20M', '20M'),
        ('50M', '50M'),
        ('100M', '100M'),
    ]

    FREQUENCE_PAIEMENT_CHOICES = [
        ('1', '1 mois'),
        ('3', '3 mois'),
        ('6', '6 mois'),
        ('12', '12 mois'),
    ]
    CIVILITE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Mlle', 'Mlle'),
    ]


    type_abonnement = models.CharField(max_length=100, choices=TYPE_ABONNEMENT_CHOICES)
    type_smart_rapido = models.CharField(max_length=100, choices=SMART_RAPIDO_CHOICES, blank=True, null=True)
    type_smart_fibre = models.CharField(max_length=100, choices=SMART_FIBRE, blank=True, null=True)
    type_smart_adsl = models.CharField(max_length=100, choices=SMART_ADSL,blank=True, null=True)
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    civilite = models.CharField(max_length=4, choices=CIVILITE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    TYPE_PIECE_CHOICES = [
        ('CIN', 'CIN'),
        ('Passport', 'Passport'),
    ]
  
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)


    type_piece_identite = models.CharField(max_length=20, choices=TYPE_PIECE_CHOICES)
    numero_piece_identite = models.CharField(max_length=50)
    telephone_contact = models.CharField(max_length=20)
    gsm_contact = models.CharField(max_length=20)
    gsm_contact_2 = models.CharField(max_length=20, blank=True, null=True)
    adresse_installation = models.TextField()
    coordonnees = models.CharField(max_length=255, blank=True, null=True)
    cin_recto = models.ImageField(upload_to='cin_recto/', blank=True, null=True)
    cin_verso = models.ImageField(upload_to='cin_recto/verso/', blank=True, null=True)
    contrat_tt = models.ImageField(upload_to='cin_recto/tt/', blank=True, null=True)
    contrat_topnet = models.ImageField(upload_to='cin_recto/topnet/', blank=True, null=True)
    contrat_general_vente = models.ImageField(upload_to='cin_recto/v/', blank=True, null=True)
    frequence_paiement = models.CharField(max_length=2, choices=FREQUENCE_PAIEMENT_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts', blank=True, null=True)


    def __str__(self):
        return f'{self.nom} {self.prenom} - {self.numero_piece_identite}'
    
    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"

    def __str__(self):
        return self.full_name





class Invoice(models.Model):
    contract = models.CharField(max_length=255, blank=True, null=True)
    numero_facture = models.CharField(max_length=20, unique=True)
    date_echeance = models.DateField() 
    service_description = models.TextField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tva_montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    total_montant = models.DecimalField(max_digits=10, decimal_places=2)
    status_paiement = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], blank=True, null=True)
   
       
    methode_paiement = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card')], blank=True, null=True)

    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.numero_facture} for contract {self.contract.id}"

    def save(self, *args, **kwargs):
        # Assurez-vous que `montant` et `taux_tva` ne sont pas None
        montant = self.montant if self.montant is not None else Decimal('0.00')
        taux_tva = self.taux_tva if self.taux_tva is not None else Decimal('0.19')  # ou la valeur par défaut souhaitée

        # Calcul du montant de la TVA et du montant total
        self.tva_montant = montant * taux_tva
        self.total_montant = montant + self.tva_montant

        super(Invoice, self).save(*args, **kwargs)


    
    
     

