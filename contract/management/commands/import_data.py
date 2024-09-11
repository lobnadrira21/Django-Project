import pandas as pd
import os
from django.core.management.base import BaseCommand
from contract.models import CodePostal, Gouvernorat, Delegation, Localite

class Command(BaseCommand):
    
  help = 'Load administrative data from Excel file'

  def handle(self, *args, **kwargs):
        file_path = r'C:\Users\ASUS\Downloads\codes_tunisie.xlsx'  # Use raw string
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            gouvernorat, _ = Gouvernorat.objects.get_or_create(nomGouvernorat=row['nomGouvernorat'])
            delegation, _ = Delegation.objects.get_or_create(nomDelegation=row['nomDelegation'], gouvernorat=gouvernorat)
            localite, _ = Localite.objects.get_or_create(nomLocalite=row['nomLocalite'], delegation=delegation)
            CodePostal.objects.get_or_create(localite=localite, codePostal=row['codePostal'])

        self.stdout.write(self.style.SUCCESS('Les données de codes postaux ont été importées avec succès.'))