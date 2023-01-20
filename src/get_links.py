from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

banned_ones = [
        'https://www.alibaba.com/',
        'https://www.alibaba.com/#',
        'https://www.alibaba.com/help?tracelog=footer_hp_buyer',
        'https://www.alibaba.com/Products?tracelog=footer_products',
        'https://www.alibaba.com/sitemap.html?tracelog=footer_sitemap',
        'https://www.alibaba.com/trade/servlet/page/static/copyright_policy',
        'https://www.alibaba.com/countrysearch/continent.html',
        'https://www.alibaba.com/suppliers/supplier.html',
        'https://www.alibaba.com/bulk?tracelog=fromhomepagefooter',
        'https://www.alibaba.com/showroom/showroom.html',
        'https://www.alibaba.com/sitemap.html'
        ]


url = 'https://www.alibaba.com'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options = options)
driver.get(url)

sleep(20)

links = driver.find_elements(By.TAG_NAME, 'a')
real_links = []

for link in links:

    link_url = str(link.get_attribute('href'))

    if link_url.startswith('https://www.alibaba.com') and link_url not in banned_ones:

        if 'tracelog' in link_url:

            pass

        elif 'toprankedseller' in link_url:

            pass

        else:

            real_links.append(link_url)


real_links = real_links[10:]

all_products = []

for link in real_links:
    
    try:

        driver.get(link)

        sleep(3)

        products = driver.find_elements(By.TAG_NAME, 'a')

        real_products = []


        for product in products:

            product_url = str(product.get_attribute('href'))

            if product_url.startswith('https://www.alibaba.com/p-detail/'):

                if product_url not in real_products:
                
                    print(product_url)
                    real_products.append(product_url)


            elif 'product-detail' in product_url:

                if product_url not in real_products:
                
                    print(product_url)
                    real_products.append(product_url)

            else:

                pass

    except:

        pass


    for product in real_products:

        if product not in all_products:

            all_products.append(product)
    
    if len(all_products) >= 10000:

        break



file_path = '/home/bilalcelebi/Workspace/alibaba-dataset/src/products.txt'

for product in all_products:

    with open(file_path, 'a') as f:

        f.write(f'{product}\n')

print(len(all_products))
