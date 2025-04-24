from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random
import re

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
                        print(f'{program_name}')
                        print()

                    # Course w/ major listing
                    else:
                        program_name = program.find('a').get_text(strip=True)
                        program_name = re.search(r'^(.+) majors? in', program_name, re.IGNORECASE).group(1)
                        print(f'{program_name}')
                        major_listing = program.find('ul').find_all('a')
                        for mj in major_listing:
                            major_details_url = mj['href']
                            major = mj.get_text(strip=True)
                            print(f'Major: {major}')
                        print()

            elif header_next.name == 'ul':
                inner_ol = header_next.find('ol')
                if inner_ol:
                    # Academic Tracks
                    program_listing = inner_ol.find_all('li')
                    for program in program_listing:
                        program_tag = program.find('a')
                        program_details_url = program_tag['href']
                        program_name = program_tag.get_text(strip=True)
                        print(f'{program_name}')
                        print()

                    # Technical-Vocational Track
                    tech_voc_listing = header_next.find_all(recursive=False)[1]
                    tech_voc_track = tech_voc_listing.find_all('a')
                    for strand in tech_voc_track:
                        program_details_url = strand['href']
                        program_name = strand.get_text(strip=True)
                        program_name = re.match(r'.*(?:\d+\.|\*)(.+)', program_name).group(1).strip() # Extract clean data
                        program_name = program_name.replace('&nbsp;', '') # Remove '&nbsp;' instances
                        print(f'{program_name}')
                        print()

                # Standard one-level unordered listing
                else:
                    ul_listing = header_next.find_all('a')
                    for strand in ul_listing:
                        program_details_url = strand['href']
                        program_name = strand.get_text()
                        print(f'{program_name}')
                        print()
                    
        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    main()