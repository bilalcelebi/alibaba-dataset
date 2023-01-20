import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from tqdm import tqdm

def get_data():

    file_path = os.path.join(os.getcwd(), 'products.txt')
    data = open(file_path)

    return data.readlines()


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sanbox')

driver = webdriver.Chrome(options = options)

products = []

data = get_data()

for link in tqdm(data[2500:3500]):

    try:

        driver.get(link)
        sleep(11)

        title = "None"

        try:
            title = driver.find_element('xpath', '//div[@class="product-title"]')
            title = title.text
        except:
            pass

        prices = []

        try:
            price_list = driver.find_elements(By.CLASS_NAME, 'price')
            for price in price_list:

                price = str(price.text)

                if price in prices:

                    pass

                elif '-' in price:

                    pass

                else:
                
                    prices.append(price)
        except:
            pass

        if prices == []:
            prices = "None"

        benefits = []

        try:
            benefit_list = driver.find_elements(By.CLASS_NAME, 'golden-buyer-first-benefit')

            for benefit in benefit_list:

                benefit = str(benefit.text)

                if benefit not in benefits:

                    benefits.append(benefit)
        except:
            pass

        if benefits == []:
            benefits = "None"

        customizations = []

        try:
            customization_list = driver.find_elements(By.CLASS_NAME, 'custom-item')

            for custom in customization_list:

                custom = str(custom.text)
            
                if custom not in customizations and custom != '':

                    customizations.append(custom)
        except:
            pass

        if customizations == []:
            customizations = "None"


        shippings = []

        try:
            shipping_list = driver.find_elements('xpath', '//div[@class="ship-list"]')
            for shipping in shipping_list:
                shipping = str(shipping.text)
                if shipping not in shippings:
                    shippings.append(shipping)
        except:
            pass

        if shippings == []:
            shippings = "None"


        skus = []

        try:
            sku_list = driver.find_elements('xpath', '//a[@class="sku-option sku-actived"]')
            for sku in sku_list:
                sku = str(sku.text)
                if sku not in skus:
                    skus.append(sku)
        except:
            pass

        if skus == []:
            skus = "None"

        overviews = dict()
        
        try:
            overview_names = driver.find_elements('xpath', '//dt[@class="do-entry-item"]')
            overview_values = driver.find_elements('xpath', '//dd[@class="do-entry-item-val"]')


            for item,value in zip(overview_names, overview_values):

                item = str(item.text)
                value = str(value.text)
                overviews[item] = value
        except:
            pass

        if overviews == {}:    
            overviews = "None"

        detail = "None"

        try:
            detail = driver.find_element(By.CLASS_NAME, 'detail-decorate-json-renderer-container').text
        except:
            pass


        company_name = "None"

        try:
            company_name = driver.find_element(By.CLASS_NAME, 'company-name-container').text
        except:
            company_name = driver.find_element(By.CLASS_NAME, 'company-item').text


        attributes = {}

        try:

            attirbutes_titles = driver.find_elements('xpath', '//div[@class="attr-title"]')
            attirbutes_contents = driver.find_elements('xpath', '//div[@class="attr-content"]')

            for title,content in zip(attirbutes_titles, attirbutes_contents):

                title = str(title.text)
                content = str(content.text)

                attributes[title] = content        
        except:

            info_titles = driver.find_elements('xpath', '//div[@class="info-title"]')
            info_intros = driver.find_elements('xpath', '//div[@class="info-intro"]')

            for title,content in zip(info_titles, info_intros):
                    
                    title = str(title.text)
                    content = str(content.text)
        
                    attributes[title] = content


        if attributes == {}:

            attributes = "None"

        sold_count = "None"

        try:
            driver.find_element(By.CLASS_NAME, 'quantity-sold')
            sold_count = driver.find_element(By.CLASS_NAME, 'quantity-sold')
            sold_count = str(sold_count.text)
        except:
            pass

        product_rating = "None"

        try:
            product_rating = driver.find_element('xpath', '//span[@class="next-form-text-align review-value"]')
            product_rating = float(str(product_rating.text))
        except:
            pass

        category_list = driver.find_elements(By.CLASS_NAME, 'detail-next-breadcrumb-text')
        categories = []

        for category in category_list:

            category = str(category.text)

            if category not in categories:

                categories.append(category)
        
        if category == []:

            category = 'None'
        

        company_website = "None"

        try:
            company_website = driver.find_element('xpath', '//a[@class="detail-next-btn detail-next-medium detail-next-btn-normal"]')
            company_website = str(company_website.get_attribute('href'))
        except:
            pass


        product = {
            "Title": title,
            "Price": prices,
            "Benefits": benefits,
            "Customizations": customizations,
            "Overviews": overviews,
            "Detail": detail,
            "Category":category,
            "Product Rating": product_rating,
            "Company Name": company_name,
            "Company Informations": attributes,
            "Link": link,
            "Store Link":company_website,
            "Quantity Sold": sold_count,
            "Shippings": shippings,
            "Skus": skus
        }

        products.append(product)
            

    except:
        pass


driver.quit()

df = pd.DataFrame(products)
df.to_csv('products.csv', index = False)
