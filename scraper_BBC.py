import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# ---- Config
URL = 'https://www.tv-program.sk/bbc-earth/cely-den/'
SEP_LINE = "-" * 40
DETAIL_DELAY_SEC = 0.5  # be nice to the site

# Base date (today)
base_date = datetime.today()

# Slovak day names -> weekday index (0=Mon)
day_map = {
    'Pondelok': 0, 'Utorok': 1, 'Streda': 2, 'Štvrtok': 3,
    'Piatok': 4, 'Sobota': 5, 'Nedeľa': 6
}

# Build "day name" -> dd.mm.YYYY for the current week
date_lookup = {}
for name, weekday_idx in day_map.items():
    delta = weekday_idx - base_date.weekday()
    if delta < 0:
        delta += 7
    date_lookup[name] = (base_date + timedelta(days=delta)).strftime('%d.%m.%Y')


# ------------------ scraping helpers ------------------
def scrape_program_details(relative_url):
    """Fetch extra info from the program page; returns empty fields on error."""
    if not relative_url:
        return {
            'Original Name': '', 'Year': '', 'Description': '',
            'Score': '', 'Genre': ''
        }
    full_url = f'https://www.tv-program.sk{relative_url}'
    try:
        resp = requests.get(full_url, timeout=10)
        time.sleep(DETAIL_DELAY_SEC)
        soup = BeautifulSoup(resp.content.decode('utf-8', errors='replace'), 'html.parser')
    except requests.exceptions.RequestException:
        return {
            'Original Name': '', 'Year': '', 'Description': '',
            'Score': '', 'Genre': ''
        }

    def get_text(sel, default=''):
        tag = soup.select_one(sel)
        return tag.text.strip() if tag else default

    # labeled fields
    def labeled_value(label):
        tag = soup.find('strong', string=label)
        return tag.find_next('span').text.strip() if tag else ''

    return {
        'Original Name': labeled_value('Pôvodný názov:'),
        'Year':          labeled_value('Rok výroby:'),
        'Description':   get_text('.post__body p', ''),
        'Score':         get_text('.bg-warning .h3', ''),
        'Genre':         get_text('.tagy', ''),
    }


def parse_dt(date_str: str, time_str: str):
    """Return datetime for 'dd.mm.YYYY' + 'HH:MM'; None on failure."""
    if not date_str or not time_str:
        return None
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    except ValueError:
        return None


# ------------------ scrape main page ------------------
resp = requests.get(URL)
soup = BeautifulSoup(resp.content.decode('utf-8', errors='replace'), 'html.parser')

channel_tag = soup.select_one('.page__title-name')
channel_name = channel_tag.text.strip() if channel_tag else 'Unknown'

# Collect raw rows grouped by day so we compute durations within each day
days = []  # list of dicts {day_name, date_str, items:[...]}
for day_block in soup.select('.programme-list'):
    day_tag = day_block.select_one('.programme-list__header .col-auto.h4')
    day_name = day_tag.text.strip() if day_tag else 'Unknown'
    date_str = date_lookup.get(day_name, '')

    items = []
    for item in day_block.select('.programme-list__item'):
        time_tag = item.select_one('time.programme-list__time')
        title_tag = item.select_one('a.programme-list__title')
        start_time_str = time_tag.text.strip() if time_tag else None
        title = title_tag.text.strip() if title_tag else None
        link = title_tag.get('href') if title_tag else None

        start_dt = parse_dt(date_str, start_time_str)
        items.append({
            'Title': title,
            'Day': day_name,
            'Date': date_str,
            'Start Time': start_time_str,
            'Start DT': start_dt,
            'Channel': channel_name,
            'Link': link
        })
    days.append({'day_name': day_name, 'date_str': date_str, 'items': items})

# ------------------ compute durations safely ------------------
final_programs = []
detail_cache = {}

for day in days:
    items = day['items']
    n = len(items)
    for i, program in enumerate(items):
        start_dt = program['Start DT']
        duration_min = None
        end_dt = None

        if start_dt:
            # Next start: the next item within this day, or (if missing)
            # we conservatively assume 50 minutes.
            if i + 1 < n and items[i + 1]['Start DT']:
                next_dt = items[i + 1]['Start DT']
                # If page lists times past midnight as "00:xx" under the same day,
                # next_dt could be <= start_dt → treat it as next day.
                if next_dt <= start_dt:
                    next_dt += timedelta(days=1)
                duration_min = int((next_dt - start_dt).total_seconds() // 60)
            else:
                duration_min = 50

            # Guard against weird negatives/zeros
            if duration_min <= 0:
                duration_min = 50
            end_dt = start_dt + timedelta(minutes=duration_min)

        # Fetch details (with simple per-URL cache)
        link = program['Link']
        if link not in detail_cache:
            detail_cache[link] = scrape_program_details(link)
        details = detail_cache[link]

        final_programs.append({
            'Title': program['Title'],
            'Day': program['Day'],
            'Date': program['Date'],
            'Start Time': program['Start Time'] or '',
            'End Time': end_dt.strftime('%H:%M') if end_dt else '',
            'Duration': f'{duration_min} min' if duration_min else '',
            'Channel': program['Channel'],
            'Link': link or '',
            'Original Name': details['Original Name'],
            'Year': details['Year'],
            'Description': details['Description'],
            'Score': details['Score'],
            'Genre': details['Genre']
        })

# ------------------ write output ------------------
with open('tv_programs_BBC.txt', 'w', encoding='utf-8') as f:
    for prog in final_programs:
        for key in [
            'Title', 'Day', 'Date', 'Start Time', 'End Time', 'Duration',
            'Channel', 'Link', 'Original Name', 'Year', 'Description', 'Score', 'Genre'
        ]:
            f.write(f"{key}: {prog.get(key, '')}\n")
        f.write(SEP_LINE + "\n")
