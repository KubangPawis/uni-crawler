from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random
import re

# RETURN VALUES: dept_name(str), clean_peo_list(list)
def extract_program_details(program_details_url, headers):

    # Local method to find deepest tag nesting of <ol> and <ul> (Because of the fragmented/confusing HTML layouting)
    def find_deepest_list_tag(element):
        current = element.find(['ol', 'ul'])
        while current:
            next_level = current.find(['ol', 'ul'])
            if not next_level:
                break
            current = next_level
        return current

    prog_details_response = requests.get(program_details_url, headers=headers)
    prog_details_soup = BeautifulSoup(prog_details_response.text, 'lxml')

    # Department Name
    vision_header = prog_details_soup.find('h4', string=re.compile(r'^VISION', re.IGNORECASE))
    if vision_header:
        dept_match = re.search(r'The ((?:[A-Z][a-z]+|of|and)(?:\s(?:[A-Z][a-z]+|of|and))*)', vision_header.find_next('p').get_text(strip=True))
        dept_name = dept_match.group(1) if dept_match else 'N/A'
    else:
        dept_name = 'N/A'

    # Program Educational Objectives (PEO)
    peo_header = prog_details_soup.find('h4', string=re.compile(r'^Program Educational Objectives', re.IGNORECASE))
    clean_peo_list = []
    if peo_header:
        peo_listing_base = peo_header.find_next(['ol', 'ul'])
        peo_listing = find_deepest_list_tag(peo_listing_base)

        if not peo_listing:
            peo_listing = peo_listing_base

        for peo in peo_listing:
            if peo_txt := peo.get_text(strip=True):
                peo_txt = peo_txt.capitalize()
                clean_peo_list.append(peo_txt)

    # RETURN DTYPES: str, list
    return dept_name, clean_peo_list

def extract_degree_type(program_header, program_name):
    if re.match(r'^TERTIARY PROGRAMS', program_header, re.IGNORECASE):
        if program_name.upper().startswith('BS'):
            return 'Bachelor of Science'
        elif program_name.upper().startswith('AB') or program_name.upper().startswith('BA'):
            return 'Bachelor of Arts'
        elif program_name.startswith('Bachelor'):
            return 'Bachelor'
        else:
            return 'Bachelor'
    elif re.match(r'^SPECIAL PROGRAMS', program_header, re.IGNORECASE):
        return 'Special Program'
    elif re.match(r'^TECHNICAL VOCATIONAL PROGRAMS', program_header, re.IGNORECASE):
        return 'Technical Vocational Program'
    else:
        return program_header.title()
    
def extract_program_name(raw_program_name):
    clean_prog_name = re.match(r'^(?:BS|AB|Bachelor of) (.+)', raw_program_name, re.IGNORECASE)
    if clean_prog_name:
        return clean_prog_name.group(1)
    return raw_program_name

def main():
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                  "AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/122.0.0.0 Safari/537.36"
    }

    # headers: to bypass WAF firewall in sending HTTP request (not unethical; still conforming to robots.txt)
    url_response = requests.get('https://cefi.edu.ph/programs/', headers=headers)
    soup = BeautifulSoup(url_response.text, 'lxml')


    # Field data extraction    
    main_content = soup.find('div', class_='elementor-widget-text-editor')
    program_headers = main_content.find_all('h4')
    for header in program_headers:
        header_next = header.find_next_sibling()
        if header_next:
            if header_next.name == 'ol':
                program_listing = header_next.find_all('li', recursive=False) # Get only direct children
                for program in program_listing:
                    # Standard course/strand program
                    if program.find('ul') is None:
                        program_tag = program.find('a')
                        program_details_url = program_tag['href']
                        program_name = program_tag.get_text(strip=True)
                        degree_type = extract_degree_type(header.get_text(strip=True), program_name)
                        program_name = extract_program_name(program_name)
                        major = 'N/A'
                        campus = 'Lucena'
                        print()
                        print('----------------')
                        print(f'{program_name}')
                        print(f'Degree Type: {degree_type}')
                        print(f'Major: {major}')
                        print(f'Campus: {campus}')

                        # PROGRAM DETAILS: data extraction
                        dept_name, clean_peo_list = extract_program_details(program_details_url, headers)
                        print(f'Department: {dept_name}')
                        for peo in clean_peo_list:
                            print(f' > {peo}')

                    # Course w/ major listing
                    else:
                        program_name = program.find('a').get_text(strip=True)
                        program_name = re.search(r'^(.+) majors? in', program_name, re.IGNORECASE).group(1)
                        degree_type = extract_degree_type(header.get_text(strip=True), program_name)
                        program_name = extract_program_name(program_name)
                        major_listing = program.find('ul').find_all('a')
                        for mj in major_listing:
                            major_details_url = mj['href']
                            major = mj.get_text(strip=True)
                            campus = 'Lucena'
                            print()
                            print('----------------')
                            print(f'{program_name}')
                            print(f'Degree Type: {degree_type}')
                            print(f'Major: {major}')
                            print(f'Campus: {campus}')

                            # PROGRAM DETAILS: data extraction
                            dept_name, clean_peo_list = extract_program_details(major_details_url, headers)
                            print(f'Department: {dept_name}')
                            for peo in clean_peo_list:
                                print(f' > {peo}')
        
            elif header_next.name == 'ul':
                inner_ol = header_next.find('ol')
                if inner_ol:
                    # Academic Tracks
                    program_listing = inner_ol.find_all('li')
                    for program in program_listing:
                        program_tag = program.find('a')
                        program_details_url = program_tag['href']
                        program_name = program_tag.get_text(strip=True)
                        degree_type = extract_degree_type(header.get_text(strip=True), program_name)
                        program_name = extract_program_name(program_name)
                        major = 'N/A'
                        campus = 'Lucena'
                        print()
                        print('----------------')
                        print(f'{program_name}')
                        print(f'Degree Type: {degree_type}')
                        print(f'Major: {major}')
                        print(f'Campus: {campus}')

                        # PROGRAM DETAILS: data extraction
                        dept_name, clean_peo_list = extract_program_details(program_details_url, headers)
                        print(f'Department: {dept_name}')
                        for peo in clean_peo_list:
                            print(f' > {peo}')

                    # Technical-Vocational Track
                    tech_voc_listing = header_next.find_all(recursive=False)[1]
                    tech_voc_track = tech_voc_listing.find_all('a')
                    for strand in tech_voc_track:
                        program_details_url = strand['href']
                        program_name = strand.get_text(strip=True)
                        program_name = re.match(r'.*(?:\d+\.|\*)(.+)', program_name).group(1).strip() # Extract clean data
                        program_name = program_name.replace('&nbsp;', '') # Remove '&nbsp;' instances
                        degree_type = extract_degree_type(header.get_text(strip=True), program_name)
                        program_name = extract_program_name(program_name)
                        major = 'N/A'
                        campus = 'Lucena'
                        print()
                        print('----------------')
                        print(f'{program_name}')
                        print(f'Degree Type: {degree_type}')
                        print(f'Major: {major}')
                        print(f'Campus: {campus}')

                        # PROGRAM DETAILS: data extraction
                        dept_name, clean_peo_list = extract_program_details(program_details_url, headers)
                        print(f'Department: {dept_name}')
                        for peo in clean_peo_list:
                            print(f' > {peo}')

                # Standard one-level unordered listing
                else:
                    ul_listing = header_next.find_all('a')
                    for strand in ul_listing:
                        program_details_url = strand['href']
                        program_name = strand.get_text(strip=True)
                        degree_type = extract_degree_type(header.get_text(strip=True), program_name)
                        program_name = extract_program_name(program_name)
                        major = 'N/A'
                        campus = 'Lucena'
                        print()
                        print('----------------')
                        print(f'{program_name}')
                        print(f'Degree Type: {degree_type}')
                        print(f'Major: {major}')
                        print(f'Campus: {campus}')

                        # PROGRAM DETAILS: data extraction
                        dept_name, clean_peo_list = extract_program_details(program_details_url, headers)
                        print(f'Department: {dept_name}')
                        for peo in clean_peo_list:
                            print(f' > {peo}')
                    
        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    main()