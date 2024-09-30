from datetime import date
from decimal import Decimal
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


import os
from django.utils.timezone import now

from django.db.models import Count
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import pandas as pd
import logging
from django.http import JsonResponse
import contract
from .models import CodePostal, Delegation, Invoice, Localite, Contract
from .forms import ContractForm, InvoiceForm
import requests
from django.contrib import messages
import json
from django.views.decorators.http import require_POST
from .models import Contract
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template.loader import render_to_string

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from django.http import HttpResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from reportlab.lib.enums import TA_RIGHT
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.utils.timezone import now
from .models import Invoice
from django.db.models import Q


logger = logging.getLogger(__name__)

@never_cache
@login_required
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.created_by = request.user
            contract.save()
            return redirect('list_contract')
        else:
            print(form.errors)  # Affiche les erreurs de formulaire dans la console
    else:
        form = ContractForm()
    return render(request, 'contract/add_contract.html', {'form': form})



@never_cache
@login_required
def list_contract(request):
    
    if request.user.is_staff:  
        contracts = Contract.objects.all()  
    else: 
        contracts = Contract.objects.filter(created_by=request.user)  
    
    return render(request, 'contract/list_contract.html', {'contracts': contracts})

    

def load_delegations(request):
    gouvernorat_id = request.GET.get('gouvernorat_id')
    delegations = list(Delegation.objects.filter(gouvernorat_id=gouvernorat_id).values('id', 'nomDelegation'))
    return JsonResponse(delegations, safe=False)

def load_localites(request):
    delegation_id = request.GET.get('delegation_id')
    localites = list(Localite.objects.filter(delegation_id=delegation_id).values('id', 'nomLocalite'))
    return JsonResponse(localites, safe=False)
def edit_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            form.save()
            return redirect('list_contract')
    else:
        form = ContractForm(instance=contract)
    return render(request, 'contract/edit_contract.html', {'form': form, 'contract': contract})

def test_view(request):
    file_path = r'C:\Users\ASUS\Downloads\codes_tunisie.xlsx' 
    df = pd.read_excel(file_path)

    nomGouvernorat = 'ARIANA'
    nomDelegation = 'RAOUED'

    delegations_from_gouvernorat = get_delegations_by_gouvernorat(df, nomGouvernorat)
    localites_from_delegation = get_secteurs_by_delegation(df, nomDelegation)
    all_gouvernorats = get_all_gouvernorats(df)

    return JsonResponse({
        "delegations_from_gouvernorat": delegations_from_gouvernorat,
        "localites_from_delegation": localites_from_delegation,
        "all_gouvernorats": all_gouvernorats
    })

# Utility functions
def get_delegations_by_gouvernorat(df, nomGouvernorat):
    return df[df['nomGouvernorat'] == nomGouvernorat]['nomDelegation'].unique().tolist()

def get_secteurs_by_delegation(df, nomDelegation):
    return df[df['nomDelegation'] == nomDelegation]['nomLocalite'].unique().tolist()

def get_all_gouvernorats(df):
    return df['nomGouvernorat'].unique().tolist()

def load_delegations(request):
    gouvernorat_id = request.GET.get('gouvernorat_id')
    print(f'Gouvernorat ID: {gouvernorat_id}')  # Debug
    delegations = list(Delegation.objects.filter(gouvernorat_id=gouvernorat_id).values('id', 'nomDelegation'))
    print(f'Delegations: {delegations}')  # Debug
    return JsonResponse(delegations, safe=False)

def load_localites(request):
    delegation_id = request.GET.get('delegation_id')
    print(f'Delegation ID: {delegation_id}')  # Debug
    localites = list(Localite.objects.filter(delegation_id=delegation_id).values('id', 'nomLocalite'))
    print(f'Localites: {localites}')  # Debug
    return JsonResponse(localites, safe=False)

def ajax_load_code_postal(request):
    localite_id = request.GET.get('localite_id')
    print(f'Localite ID: {localite_id}')  # Debug
    code_postal = get_object_or_404(CodePostal, localite_id=localite_id)
    print(f'Code Postal: {code_postal.codePostal}')  # Debug
    return JsonResponse({'code_postal': code_postal.codePostal})

def get_coordinates(request):
    localite_id = request.GET.get('localite_id')
    if localite_id:
        try:
            localite = Localite.objects.get(id=localite_id)
            address = f"{localite.nomLocalite}, {localite.delegation.nomDelegation}, {localite.delegation.gouvernorat.nomGouvernorat}, Tunisia"
            url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
            response = requests.get(url)
            data = response.json()
            if data:
                coordinates = {'lat': data[0]['lat'], 'lon': data[0]['lon']}
            else:
                coordinates = {'lat': None, 'lon': None}
        except Localite.DoesNotExist:
            coordinates = {'lat': None, 'lon': None}
        except Exception as e:
            print(f"Error fetching coordinates: {e}")  # Debug
            coordinates = {'lat': None, 'lon': None}
    else:
        coordinates = {'lat': None, 'lon': None}
    return JsonResponse(coordinates)

def list_contract_admin(request):
    contracts = Contract.objects.all()
    return render(request, 'contract/valid_contract.html', {'contracts': contracts})


def approve_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    contract.status = 'approved'
    contract.save()

    # Ajouter un message de succès pour l'utilisateur
    messages.success(request, f'Le contrat {contract.id} a été approuvé avec succès.')

    # Rediriger vers la page appropriée
    return redirect(request.META.get('HTTP_REFERER', 'card_valid_contract'))


def reject_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    contract.status = 'rejected'
    contract.save()

    # Ajouter un message d'alerte pour l'utilisateur
    messages.warning(request, f'Le contrat {contract.id} a été rejeté.')

    # Rediriger vers la page appropriée
    return redirect(request.META.get('HTTP_REFERER', 'card_valid_contract'))



def view_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contract/valid_contract.html', {'contract': contract})
def view_contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contract/detail_contract.html', {'contract': contract})

def card_contract(request):
    contracts = Contract.objects.all()
    return render(request, 'contract/card_valid_contract.html', {'contracts': contracts})








def list_invoices(request):
    # Vérifier si l'utilisateur est administrateur ou non
    if request.user.is_staff:  
        # Si l'utilisateur est administrateur, afficher toutes les factures
        invoices = Invoice.objects.all()
    else: 
        # Sinon, afficher seulement les factures créées par l'utilisateur
        invoices = Invoice.objects.filter(created_by=request.user)

    # Récupérer les critères de recherche
    numero_facture = request.GET.get('numero_facture', '')
    contract = request.GET.get('contract', '')
    date_echeance = request.GET.get('date_echeance', '')
    status_paiement = request.GET.get('status_paiement', '')

    # Appliquer les filtres seulement si les champs sont remplis
    if numero_facture:
        invoices = invoices.filter(numero_facture__icontains=numero_facture)
    
    if contract:
        invoices = invoices.filter(contract__icontains=contract)
    
    if date_echeance:
        invoices = invoices.filter(date_echeance=date_echeance)
    
    if status_paiement:
        invoices = invoices.filter(status_paiement=status_paiement)

    return render(request, 'facturation/list_invoice.html', {'invoices': invoices})



def download_invoice(request, invoice_id):
    # Récupérez l'objet Invoice ici
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    # Créer une réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'
    
    # Créer un document SimpleDocTemplate avec ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Red', textColor=colors.red, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Black', textColor=colors.black, alignment=TA_LEFT))

    # Elements du PDF
    elements = []
    
    # Titre de la facture
    elements.append(Paragraph("Facture", styles['Title']))
    elements.append(Spacer(1, 12))

    # Ajouter le logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logotopnet.png')  # Chemin du logo
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.5*inch, height=1.5*inch)  # Ajustez les dimensions si nécessaire
        elements.append(logo)
    elements.append(Spacer(1, 12))
    
    # Informations de l'expéditeur
    elements.append(Paragraph("Tunis", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Informations du client
    elements.append(Paragraph(f"FACTURÉ À", styles['Heading4']))
    elements.append(Paragraph(f"Nom du client: {invoice.contract}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Informations de la facture
    elements.append(Paragraph(f"N° de facture: {invoice.numero_facture}", styles['RightAlign']))
    elements.append(Paragraph(f"Date: {date.today().strftime('%b. %d, %Y')}", styles['RightAlign']))  # Date du système
    elements.append(Paragraph(f"Date d'échéance: {invoice.date_echeance.strftime('%b. %d, %Y')}", styles['RightAlign']))
    elements.append(Spacer(1, 12))
    
    # Table des éléments de la facture
    data = [
        [ "Service Description", "Montant", "TVA Montant", "Total Montant"],
        [ invoice.service_description, f"{invoice.montant} DT", f"{invoice.tva_montant} DT", f"{invoice.total_montant} DT"]
    ]
    
    table = Table(data, colWidths=[1.5*inch]*5)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Total de la facture et gestion du statut de paiement
    solde_a_payer = 0 if invoice.status_paiement == 'paid' else invoice.total_montant
    elements.append(Paragraph(f"Sous-total HT: {invoice.montant} DT", styles['RightAlign']))
    elements.append(Paragraph(f"TVA: {invoice.tva_montant} DT", styles['RightAlign']))
    elements.append(Paragraph(f"<strong>Total TTC: {invoice.total_montant} DT</strong>", styles['RightAlign']))
    elements.append(Paragraph(f"Paiement(s): {invoice.total_montant if invoice.status_paiement == 'paid' else '0.00'} DT", styles['RightAlign']))
    elements.append(Paragraph(f"<strong>Solde à payer: {solde_a_payer} DT</strong>", styles['RightAlign']))
    elements.append(Spacer(1, 24))  # Ajouter de l'espace avant les notes
    elements.append(Paragraph("<strong>Remarques :</strong>", styles['Normal']))

    # Créer un cadre autour des notes
    data_notes = [[f"{invoice.notes}"]]
    table_notes = Table(data_notes, colWidths=[6 * inch])  # Largeur du rectangle pour les notes
    table_notes.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Ajouter une bordure
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(table_notes)
    # Ajout du texte "Payé" en rouge si le statut de paiement est "paid"
    if invoice.status_paiement == 'paid':
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Payé", styles['Red']))
        elements.append(Paragraph(f"Mode de paiement: {invoice.methode_paiement}", styles['Black']))
    # Vérifier si la date d'échéance est dépassée
     
   
    if (invoice.status_paiement in [None, 'unpaid']) and date.today() > invoice.date_echeance:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("<strong>Le paiement de la facture est en retard.</strong>", styles['Red']))
    # Générer le PDF
    doc.build(elements)
    
    return response





def add_invoice(request):
    contrats = Contract.objects.filter(created_by=request.user, status='approved')

    form = InvoiceForm()
    form.fields['contract'].queryset = contrats

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user  # Associer l'utilisateur
            invoice.save()
            return redirect('list_invoice')

    return render(request, 'facturation/add_invoice.html', {'form': form})


def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Filtrer les contrats créés par l'utilisateur et qui ont un statut approuvé
    contrats = Contract.objects.filter(created_by=request.user, status='approved')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('list_invoice')  # Redirige vers la liste des factures après la mise à jour
    else:
        form = InvoiceForm(instance=invoice)
        # Limiter les choix du champ "contract" aux contrats de l'utilisateur connecté
        form.fields['contract'].queryset = contrats
    
    return render(request, 'facturation/update_invoice.html', {'form': form, 'invoice': invoice})


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('list_invoice') 

def view_invoice(request, invoice_id):
    # Récupérer la facture selon son ID ou renvoyer une 404 si elle n'existe pas
    invoice = get_object_or_404(Invoice, id=invoice_id)
    today_date = date.today()

    return render(request, 'facturation/invoice_template.html', {
        'invoice': invoice,
        'today_date': today_date,
    })
    
    
    
def card_invoices_admin(request):
    invoices = Invoice.objects.all()  # Vous pouvez filtrer selon les besoins
    return render(request, 'facturation/card_invoices.html', {'invoices': invoices})



@login_required
def admin_dashboard(request):
    current_year = now().year

    # Labels pour les mois
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Liste initialisée pour le nombre de factures créées et payées par mois
    invoice_totals = [0] * 12
    paid_invoice_counts = [0] * 12

    # Récupérer toutes les factures créées et payées par mois
    invoices_by_month = Invoice.objects.filter(created_at__year=current_year).annotate(month=ExtractMonth('created_at')).values('month').annotate(invoice_count=Count('id')).order_by('month')
    paid_invoices_by_month = Invoice.objects.filter(status_paiement='paid', created_at__year=current_year).annotate(month=ExtractMonth('created_at')).values('month').annotate(invoice_count=Count('id')).order_by('month')

    # Remplir les tableaux des factures créées et payées
    for invoice in invoices_by_month:
        month_index = invoice['month'] - 1  # Index des mois (0 pour janvier)
        invoice_totals[month_index] = invoice['invoice_count']

    for paid_invoice in paid_invoices_by_month:
        month_index = paid_invoice['month'] - 1
        paid_invoice_counts[month_index] = paid_invoice['invoice_count']

      # Nouvelle partie : Répartition des factures par statut de paiement
    payment_status_labels = ['Payées', 'En attente', 'Impayées']
    paid_invoices_count = Invoice.objects.filter(status_paiement='paid').count()
    pending_invoices_count = Invoice.objects.filter(status_paiement='pending').count()
    unpaid_invoices_count = Invoice.objects.filter(status_paiement='unpaid').count()
    payment_status_counts = [paid_invoices_count, pending_invoices_count, unpaid_invoices_count]

    # Passer toutes les données dans le contexte
    context = {
        'labels': labels,
        'invoice_totals': invoice_totals,
        'paid_invoice_counts': paid_invoice_counts,
        'payment_status_labels': payment_status_labels,
        'payment_status_counts': payment_status_counts,
    }

    return render(request, 'contract/valid_contract.html', context)

    

    

def search_contract(request):
    # Get search query from the request
    search_query = request.GET.get('search', '')

    # Start with all contracts
    contracts = Contract.objects.all()

    if search_query:
        # Dynamically search across all relevant fields of the Contract model
        contracts = contracts.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(gouvernorat__icontains=search_query) |
            Q(type_abonnement__icontains=search_query) |
            Q(type_smart_rapido__icontains=search_query) |
            Q(localite__icontains=search_query) |
            Q(telephone_contact__icontains=search_query) |
            Q(gsm_contact__icontains=search_query) |
            Q(adresse_installation__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    return render(request, 'contract/list_contract.html', {'contracts': contracts})