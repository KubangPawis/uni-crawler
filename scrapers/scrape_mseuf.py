from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random
import re

def main():
    # Data storage
    program_df = pd.DataFrame(columns=['id', 'program_name', 'major', 'degree_type', 'department'])
    program_campus_df = pd.DataFrame(columns=['id', 'program_id', 'campus'])
    program_peo_df = pd.DataFrame(columns=['id', 'program_id', 'peo'])
    program_outcomes_df = pd.DataFrame(columns=['id', 'program_id', 'outcome'])

    url_response = requests.get('https://mseuf.edu.ph/programs')
    soup = BeautifulSoup(url_response.text, 'lxml')

    # Field data extraction
    cards = soup.find_all('div', class_='card-panel outlined program-card waves-effect')
    for card in cards:
        program_name = card.find('p', class_='program')
        degree_type = card.find('p', class_='degree')
        major = card.find('p', class_='majors')
        campus = card.find('p', class_='campus')

        # --------- Text extraction (error handled) ---------
        # Program Name
        program_name_txt = program_name.get_text(strip=True) if program_name else 'N/A'

        # Degree Type
        degree_type_txt = degree_type.get_text(strip=True) if degree_type else 'N/A'
        degree_type_txt = degree_type_txt.removesuffix(' in').removesuffix(' of') # Remove unnecessary suffixes
        degree_type_txt = degree_type_txt.replace('(', '').replace(')', '') # Remove unnecessary parentheses

        # Major
        major_txt = major.get_text(strip=True) if major else 'N/A'
        major_txt = major_txt.replace('major in', '').strip()

        # Campus Location
        campus_txt = campus.get_text(strip=True) if campus else 'N/A'
        campus_txt = campus_txt.replace('Offered in', '').strip()

        print(f'Program Name: {program_name_txt}')
        print(f'Degree Type: {degree_type_txt}')
        print(f'Majors: {major_txt}')
        print(f'Campus: {campus_txt}')
        print()

        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    main()