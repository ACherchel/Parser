import requests
from bs4 import BeautifulSoup
import csv


def get_html(url_cat):
    r= requests.get(url_cat)
    return r.text

def get_html_cat(base_url):
    r= requests.get(base_url)
    return r.text

def get_categorie(html):
    tot_cat=[]
    for i in range(1,116):
        soup = BeautifulSoup(html, 'lxml')
        categorie = soup.find('div', class_ = 'left-box-home').find('nav').find('ul').find_all('a')[i].get('href')
        tot_cat.append(categorie)
    return tot_cat


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='more-pages-l clearfix').find_all('a', class_='more-pages-l-i-link novisited')[-1].get('href')
    total_pages= pages.split('=')[1].split('/')[0]
    return int(total_pages)

def write_csv(data):
    with open('Kancler.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['title'],
                          data['price'],
                          data['quantity'],
                          data['url'],
                         data['picture']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads= soup.find('div', class_='g-l catalog-l clearfix').find_all('div', class_='g-l-i clearfix')


    for ad in ads:
        try:
            title = ad.find('div', class_='g-l-i-details-title').find('a',).text
        except:
            title=''
        try:
            url= ad.find('div', class_='g-l-i-details-title').find('a').get('href')
        except:
            url= ''
        try:
            price=ad.find('div', class_='pp-price-cost uah pp-price-cost-cur').text
        except:
            price=''
        try:
            quantity_s=ad.find('div', class_='warehouse').find('span').text
            quantity_m=ad.find('div', class_='warehouse').next_sibling.next_sibling.find('span').text
            quantity=int(quantity_s)+int(quantity_m)
        except:
            quantity=''
        try:
            picture=ad.find('div', class_='pp-image-wrap g-list-i-img').find('img').get('src')
        except:
            picture=''
        data= {'title':title,
                'url':url,
                'price':price,
                'quantity':quantity,
               'picture':picture}

        write_csv(data)



def main():
    base_url = 'https://kancler.com/'
    page_part= 'page='
    que_part= '/'
    tot_cat=get_categorie(get_html_cat(base_url))
    print(tot_cat)

    while tot_cat!=[]:
        url_cat=tot_cat.pop()
        try:
            total_pages= get_total_pages(get_html(url_cat))

            for i in range(1, total_pages+1):
                url_gen= url_cat+page_part+str(i)+que_part
                # print(url_gen)
                html= get_html(url_gen)
                get_page_data(html)
        except:
            html = get_html(url_cat)
            get_page_data(html)




if __name__ == '__main__':
    main()
