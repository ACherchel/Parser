import requests
from bs4 import BeautifulSoup
import csv


def get_html_cat(base_url):
    r = requests.get(base_url)
    return r.text


def get_html_sub_cat(cat_url):
    r = requests.get(cat_url)
    return r.text

def full_html(url):
    r= requests.get(url)
    return r.text

def write_csv(data):
    with open('AK.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['title'],
                         data['article'],
                         data['price'],
                         data['quantity'],
                         data['image']))



def get_cat(html):
    total_cat = []
    for i in range(0, 16):
        try:
            soup = BeautifulSoup(html, 'lxml')
            categorie = soup.find('ul', class_='mob cat attachments1').find_all('a')[i].get('href')
            total_cat.append(categorie)
        except:
            break
    return total_cat


def get_sub_cat(html):
    soup = BeautifulSoup(html, 'lxml')
    total_sub_cat = []
    for i in range(0, 50):
        try:
            sub_categorie = soup.find('ul', class_='cat attachments2').find_all('a')[i].get('href')
            total_sub_cat.append(sub_categorie)
        except:
            break
    return total_sub_cat


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination').find_all('a')[-2].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


def get_page_product(html):
    soup = BeautifulSoup(html, 'lxml')
    total_prod_url = []
    for i in range(0, 25):
        try:
            product = soup.find('div', class_='products catalog asd').find('ul').find_all('li')[0].find('a').get('href')
            total_prod_url.append(product)
        except:
            break
    return total_prod_url


def get_product_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        title=soup.find('div', class_='product').find('div', class_='page-title').text
    except:
        title=''
    try:
        article = soup.find('div', class_='product').find('div', class_='center').find('div', class_='article').find('span').next_sibling
    except:
        article = ''
    try:
         price = soup.find('div', class_='product').find('div', class_='center').find('table', class_='prices').find('p', class_='price').text
    except:
         price = ''
    try:
         quantity = soup.find('div', class_='product').find('div', class_='center').find('div', class_='stock_new')
         total_quantity = quantity.split(':')[1]
    except:
         total_quantity = ''
    try:
         image = soup.find('div', class_='product').find('div', class_='image').find('a').get('href')
    except:
         image = ''

    data = {'title': title,
             'article':article,
             'price': price,
             'quantity': total_quantity,
             'image': image}

    write_csv(data)


def main():
    base_url = 'https://ak.ua/'
    page_part = '?page='
    tot_cat = get_cat(get_html_cat(base_url))

    while tot_cat != []:
        cat_url =base_url+ tot_cat.pop()
        tot_sub_cat = get_sub_cat(get_html_sub_cat(cat_url))
        while tot_sub_cat != []:
            url_sub_cat =base_url+ tot_sub_cat.pop()
            full_sub_url=full_html(url_sub_cat)
            try:
                total_pages = get_page_product(get_html_sub_cat(full_sub_url))

                for i in range(1, total_pages + 1):
                    url_gen = base_url + page_part + str(i)
                    html = get_html_cat(url_gen)
                    prod_url = get_page_product(html)
                    while prod_url != []:
                        page =base_url+ prod_url.pop()
                        full_page= full_html(page)
                        get_product_data(full_page)

            except:
                prod_url = get_page_product(full_sub_url)
                while prod_url != []:
                    prod_page =base_url+ prod_url.pop()
                    full_prod_page=full_html(prod_page)
                    get_product_data(full_prod_page)



if __name__ == '__main__':
    main()
