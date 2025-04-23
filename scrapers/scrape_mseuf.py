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

        # Mid item delay
        time.sleep(random.uniform(1, 3))

        prog_details_url = card.find('a', attrs={'class': 'action', 'title': 'View Program'})['href']
        prog_details_response = requests.get(f'https://mseuf.edu.ph{prog_details_url}')
        prog_details_soup = BeautifulSoup(prog_details_response.text, 'lxml')

        # --------- PROGRAM DETAILS: text extraction (error handled) ---------

        # Program Educational Objectives (PEO)
        obj_div = prog_details_soup.find('div', class_='objectives')
        obj_tbody = obj_div.find('tbody')
        if obj_tbody:
            obj_tr_list = obj_tbody.find_all('tr')
            cnt = 1
            for tr in obj_tr_list:
                obj_objective = tr.find('td') # Get first 'td' instance for objectives
                obj_objective_txt = obj_objective.get_text(strip=True)
                obj_objective_txt = re.sub(r'^\d', '', obj_objective_txt) # Remove annoying objective count prefix
                print(f'Objective #{cnt}: {obj_objective_txt}')
                print()

                cnt += 1
        
        # Delay
        time.sleep(random.uniform(1, 3))



if __name__ == '__main__':
    main()