import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

# live_url="https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
url="https://appbrewery.github.io/instant_pot/"

#add headers in requests.get for the web page to give information according to you

# header= {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Encoding": "gzip, deflate, br, zstd",
#         "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
#         "Host": "httpbin.org",
#         "Priority": "u=0, i",
#         "Sec-Ch-Ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
#         "Sec-Ch-Ua-Mobile": "?0",
#         "Sec-Ch-Ua-Platform": "\"Windows\"",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "cross-site",
#         "Sec-Fetch-User": "?1",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
#         "X-Amzn-Trace-Id": "Root=1-66e6fc61-219b45a13a7eec44253412cb"
#     }


response=requests.get(url=url)
html_page=response.text

soup=BeautifulSoup(html_page,"html.parser")

#getting product title
title = soup.find(id="productTitle").get_text().strip()

#getting whole price
whole_price=soup.find(class_="a-offscreen")
price=whole_price.getText() #price with dollar symbol

#getting price as float
price_as_float=float(price.split("$")[1]) #price without dollar symbol

#--------------------------------------------SENDING AN EMAIL-----------------------------------------------------#
BUY_PRICE=100
import smtplib
my_email=os.environ["MY_EMAIL"]
password=os.environ["EMAIL_PASSWORD"]
if price_as_float<BUY_PRICE:
    message = f"{title} is on sale for {price}!"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs="juwairiatabasoom@gmail.com",msg=f"Subject:Amazon Low price Alert!!!\n\n{message}\n{url}".encode("utf-8"))

