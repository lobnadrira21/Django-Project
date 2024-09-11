import requests
from bs4 import BeautifulSoup
from contract.models import Gouvernorat, Delegation, Localite

def fetch_data():
    url = 'https://fr.wikipedia.org/wiki/Gouvernorat_(Tunisie)'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver le tableau des gouvernorats
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) > 1:
                    gouvernorat_name = cols[0].text.strip()
                    gouvernorat, created = Gouvernorat.objects.get_or_create(name=gouvernorat_name)

                    # Trouver la page des délégations et municipalités du gouvernorat
                    link = row.find('a')['href']
                    gov_url = 'https://fr.wikipedia.org' + link
                    gov_response = requests.get(gov_url)
                    
                    if gov_response.status_code == 200:
                        gov_soup = BeautifulSoup(gov_response.text, 'html.parser')
                        tables_gov = gov_soup.find_all('table', {'class': 'wikitable'})
                        
                        for table_gov in tables_gov:
                            rows_gov = table_gov.find_all('tr')
                            for row_gov in rows_gov[1:]:
                                cols_gov = row_gov.find_all('td')
                                if len(cols_gov) > 1:
                                    delegation_name = cols_gov[0].text.strip()
                                    delegation, created = Delegation.objects.get_or_create(name=delegation_name, gouvernorat=gouvernorat)
                                    
                                    localite_name = cols_gov[1].text.strip()
                                    Localite.objects.get_or_create(
                                        name=localite_name,
                                        delegation=delegation,
                                        code_postal=cols_gov[2].text.strip() if len(cols_gov) > 2 else None,
                                        latitude=None,  # Vous devrez peut-être ajuster cela
                                        longitude=None  # Vous devrez peut-être ajuster cela
                                    )
    else:
        print('Failed to fetch data from Wikipedia')
