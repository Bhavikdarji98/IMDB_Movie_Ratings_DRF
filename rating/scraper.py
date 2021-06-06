from . models import MovieRatings
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dateutil.parser import parse

def dumpdata():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    content = driver.page_source
    page_soup = BeautifulSoup(content)
    
    url = 'https://www.imdb.com/chart/top'
    url_text = requests.get(url).text
    soup = BeautifulSoup(url_text, 'html.parser')
    template = 'https://www.imdb.com%s'
    title_links = [template % a.attrs.get('href') for a in soup.select( 'td.titleColumn a' )]
    
    # we have title_links to get 250 movies information
    for movie in title_links:
        driver.get(str(movie))
        content = driver.page_source
        page_soup = BeautifulSoup(content)
        
        name = (page_soup.find("div",{ "class":"title_wrapper" }).get_text( strip=True ).split('|')[0]).split('(')[0]
        
        rating = page_soup.find("span",{"itemprop":"ratingValue"}).text
        subtext= page_soup.find("div",{ "class":"subtext" }).get_text( strip=True ).split('|' )
        
        release_date = subtext[-1]
        # release_date = str_to_date(release_date_)
        
        duration_ = subtext[1]
        duration = minute_duration(duration_)

        description= page_soup.find("div",{ "class":"inline canwrap" }).get_text( strip=True ).split('|')[0]

        print("Successfully scraped data from IMDB.")
        # create dict param
        dict = {
            "name" : name,
            "rating": rating,
            "release_date": release_date,
            "duration": duration,
            "description": description
        }
        # save into database
        MovieRatings.objects.create(**dict)
        print("Entry Created ")
    
def str_to_date(release_date):
    timestr = release_date.split()[:3]
    timestr = ' '.join(timestr)
    release_date = parse(timestr)
    return release_date

def minute_duration(duration):
    hour = 0
    min = 0
    values = duration.split()
    if len(values) > 1:
        hour = values[0][0]
        if len(values[1])<5:
            min = values[1][0]
        else:
            min = values[1][:2]
    else:
        if values[0][-1] != 'h':
            if len(values[0])<5:
                min = values[0][0]
            else:
                min = values[0][:2]
        else:
            hour = values[0][0]
    total_min = int(hour) * 60 + int(min)
    return total_min