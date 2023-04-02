from flask import Flask, request, jsonify
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import numpy as np
import pandas as pd
import re, nltk, string
from nltk.corpus import stopwords

  
app = Flask(__name__)

app.config["DEBUG"] = True


data = pd.read_excel('carbon-footprint-data.xlsx')
labels = pd.read_excel('labels.xlsx')

names = data["Product name (and functional unit)"]
industries = data["Company's GICS Industry"]
carbons = data["Product's carbon footprint (PCF, kg CO2e)"]
weights = data["Product weight (kg)"]
industry_names = [
        'Food Products',
        'Not used for 2015 reporting',
        'Building Products',
        'Electronic Equipment, Instruments & Components',
        'Chemicals',
        'Construction Materials',
        'Textiles, Apparel & Luxury Goods',
        'Computers & Peripherals',
        'Household Durables',
        'Beverages',
        'Metals & Mining',
        'Semiconductors & Semiconductor Equipment',
        'Software',
        'Paper & Forest Products',
        'Commercial Services & Supplies',
        'Aerospace & Defense',
        'Communications Equipment',
        'Gas Utilities',
        'Wireless Telecommunication Services',
        'Office Electronics',
        'Electrical Equipment',
        'Containers & Packaging',
        'Specialty Retail',
        'Media',
        'Automobiles',
        'Auto Components',
        'Life Sciences Tools & Services',
        'Machinery',
        'Diversified Telecommunication Services',
        'Trading Companies & Distributors',
        'Oil, Gas & Consumable Fuels',
        'Food & Staples Retailing',
        'Tobacco',
        'Personal Products',
        'IT Services',
        ]


unique_industry = {
        'Food Products': [],
        'Not used for 2015 reporting': [],
        'Building Products': [],
        'Electronic Equipment, Instruments & Components': [],
        'Chemicals': [],
        'Construction Materials': [],
        'Textiles, Apparel & Luxury Goods': [],
        'Computers & Peripherals': [],
        'Household Durables': [],
        'Beverages': [],
        'Metals & Mining': [],
        'Semiconductors & Semiconductor Equipment': [],
        'Software': [],
        'Paper & Forest Products': [],
        'Commercial Services & Supplies': [],
        'Aerospace & Defense': [],
        'Communications Equipment': [],
        'Gas Utilities': [],
        'Wireless Telecommunication Services': [],
        'Office Electronics': [],
        'Electrical Equipment': [],
        'Containers & Packaging': [],
        'Specialty Retail': [],
        'Media': [],
        'Automobiles': [],
        'Auto Components': [],
        'Life Sciences Tools & Services': [],
        'Machinery': [],
        'Diversified Telecommunication Services': [],
        'Trading Companies & Distributors': [],
        'Oil, Gas & Consumable Fuels': [],
        'Food & Staples Retailing': [],
        'Tobacco': [],
        'Personal Products': [],
        'IT Services': [],
        }

for i, industry in industries.items():
    unique_industry[industry].append(i)


print(unique_industry)

avgs = []
temp_sum = 0
for industry in industry_names:
    for i in unique_industry[industry]:
        temp_sum += int(carbons[i])
    avgs.append(temp_sum / len(unique_industry[industry]))
    temp_sum = 0

avg_weights = []
for industry in industry_names:
    for i in unique_industry[industry]:
        temp_sum += int(weights[i])
    avg_weights.append(temp_sum / len(unique_industry[industry]))
    temp_sum = 0

print(avgs)
print(avg_weights)

def get_result(image_path):
    #use selenium to open the website
    webdriver_path = r"./chromedriver"
    driver = webdriver.Chrome(webdriver_path)
    driver.get("https://microsoft.github.io/onnxjs-demo/#/squeezenet")
    time.sleep(5)

    #click the button to upload the image
    #the style is "display: none;" and it is the second in the array. It is in the form of an input tag
    file_upload = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div/div[1]/div/div[3]/div[1]/div[1]/label/input"))
    )
    file_upload.send_keys(image_path)

    time.sleep(3)

    xpath = "/html/body/div/div/div[3]/main/div/div/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]"
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    print(result.text)
    return (result.text)
    


#create a route for image except name it imageWeb. Instead of taking a file it should use a file from online, download it, and then run the get_result function
@app.route("/imageWeb", methods=["GET"])
def imageWebTry():
     try:
          url = "https://img1.cgtrader.com/items/633725/ed706f12da/water-drink-plastic-bottle-250ml-3d-model-low-poly-max--obj-mtl-fbx-c4d-blend.jpg"
          url = request.args.get("url")
          urllib.request.urlretrieve(url, "/Users/albrino/Downloads/Old-Items/ChromeExtensionScrapingHelloWorld/images/" + url.split("/")[-1])
          return jsonify(get_result("/Users/albrino/Downloads/Old-Items/ChromeExtensionScrapingHelloWorld/images/" + url.split("/")[-1]))
     except Exception as e:
        print(e)
        return "error"

@app.route("/carbon/<string:category>/<int:weight>")
def carbon(category, weight):
    index = -1
    for i, industry in enumerate(industry_names):
        if category == industry:
            index = i
    footprint = avgs[i] /  avg_weights[i] * weight
    return f"{footprint}"

@app.route("/category/<string:label>")
def category(label):
    i, c = np.where(labels == label)
    return f"{labels.columns[c][0]}"


#start app at port
if __name__ == "__main__":
    app.run(port=5000)

