import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://vedas.sac.gov.in/en/"

def get_soup():
    resp = requests.get(url=BASE_URL, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")



def scrape_site_heading(soup):
    data = {}
    img = soup.select_one("#body > div.header > div > div:nth-child(4) > img:nth-child(3)")
    if img:
        data['alt'] = img.get("alt", "").strip()
        data['title'] = img.get("title", "").strip()

    return data




# ---- extract announcement section ---- #
def scrape_announcements(soup):
    data = {}
    section = soup.select_one("#contents > div.home-content > div.announce-carousel > div.announcement")
    if section:
        heading = section.select_one("h4.pdf-detail")
        if heading:
            data['heading'] = heading.get_text(strip=True)

        items = []
        for link in section.select("a"):
            text = link.get_text(" ", strip=True)
            href = link.get("href")
            if text and href:
                items.append({"text": text, "href": href})

        
        for span in section.select("span"):
            text = span.get_text(" ", strip=True)
            if text:
                items.append({"text": text})
        
        for p in section.select("p"):
            text = p.get_text(" ", strip=True)
            if text:
                items.append({"text": text})
        
        data['items'] = items

    return data

def scrape_awards(soup):
    data = {}
    heading = soup.select_one("#maincontent > div:nth-child(1) > div > h4.text-bold")
    if heading:
        data['heading'] = heading.get_text(strip=True)

    # extract the description paragraph
    desc = soup.select_one("#maincontent > div:nth-child(1) > table > tbody > tr > td:nth-child(1) > p.content-c")
    if desc:
        data['description'] = desc.get_text(" ", strip=True)

    
    # -- Optional -- #
    table_desc = soup.select("#maincontent > div:nth-child(1) > table p.content-c")
    if table_desc:
        extra_texts = [td.get_text(" ", strip=True) for td in table_desc if td]
        extra = " ".join(extra_texts)
        if "description" in data:
            data['description'] += " " + extra
        else:
            data['description'] = extra
    
    return data

def scrape_builtup(soup):
    data = {}
    heading = soup.select_one("#maincontent > div:nth-child(3) > div > h4")
    if heading:
        data['heading'] = heading.get_text(strip=True)

    desc = soup.select_one("#maincontent > div:nth-child(3) p.content-c")
    if desc:
        data['description'] = desc.get_text(" ", strip=True)

    return data


def scrape_webinar(soup):
    data = {}
    heading = soup.select_one("#maincontent > div:nth-child(5) > div > h4")
    if heading:
        data['heading'] = heading.get_text(strip=True)
    desc = soup.select_one("#maincontent > div:nth-child(5) p.content-c")
    if desc:
        data['description'] = desc.get_text(" ", strip=True)
    return data


def scrape_interferometric(soup):
    data = {}
    heading = soup.select_one("#maincontent > div:nth-child(7) > div > h4")
    if heading:
        data['heading'] = heading.get_text(strip=True)
    desc = soup.select_one("#maincontent > div:nth-child(7) p.content-c")
    if desc:
        data['description'] = desc.get_text(" ", strip=True)
    return data

def scrape_solar_power_plants(soup):
    data = {}
    heading = soup.select_one("#maincontent > div:nth-child(9) > div > h4")
    if heading:
        data['heading'] = heading.get_text(strip=True)
    desc = soup.select_one("#maincontent > div:nth-child(9) p.content-c")
    if desc:
        data['description'] = desc.get_text(" ", strip=True)
    return data


def scrape_contact(soup):
    data = {}
    block = soup.select_one("#body > div.footer > section > div > div > div:nth-child(1) > div")
    if block:
        lines = [(p.get_text(" ", strip=True)) for p in block.select("p")]
        phone_node = block.select_one("li span.color-text-a")
        phone_text = block.get_text(" ", strip=True) if phone_node else None
        data['contact'] = lines
        data['phone'] = phone_text

    return data





# ---- extract website heading ---- #
def scrape_all():
    soup = get_soup()
    result = {
        "site_heading": scrape_site_heading(soup=soup),
        "announcements": scrape_announcements(soup=soup),
        "awards": scrape_awards(soup=soup),
        "builtup_area": scrape_builtup(soup=soup),
        "webinar": scrape_webinar(soup=soup),
        "interferometric": scrape_interferometric(soup=soup),
        "solar_power_plants": scrape_solar_power_plants(soup=soup),
        "contact": scrape_contact(soup=soup)
        

    }
    out_dir = os.path.join("app", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "vedas.json")
    with open(out_path, "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data = scrape_all()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    






