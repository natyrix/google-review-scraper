from selenium import webdriver
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'

driver = webdriver.Chrome(ChromeDriverManager().install())
url='https://www.google.com/maps/place/Aspria+Berlin+Ku%E2%80%99damm/@52.5003887,13.2941771,15z/data=!4m10!3m9!1s0x0:0x2faf0f02eacd864e!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771!9m1!1b1'

driver.get(url)
time.sleep(10)

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

number = 0

while True:
    number = number+1

    # Scroll down to bottom
    
    ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
    driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

    # Wait to load page

    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    print(f'last height: {last_height}')

    ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

    new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

    print(f'new height: {new_height}')

    if number == 5:
        break

    if new_height == last_height:
        break

    print('cont')
    last_height = new_height

# //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[11]
# //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[11]/div[1]

item = driver.find_elements(By.XPATH ,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[11]')

time.sleep(5)
print(len(item))

name_list = []
stars_list = []
review_list = []
review_link = []
time_list = []
response_list = []
has_response_list = []

for i in item:

    button = i.find_elements(By.TAG_NAME, 'button')
    for m in button:
        if m.text == "More":
            m.click()
    time.sleep(5)

    name = i.find_elements(By.CLASS_NAME, "d4r55")
    review = i.find_elements(By.CLASS_NAME, "wiI7pd")
    stars = i.find_elements(By.CLASS_NAME, "fzvQIb") #fzvQIb
    duration = i.find_elements(By.CLASS_NAME, "xRkPPb") #xRkPPb
    resonse = i.find_elements(By.CLASS_NAME, "CDe7pd")

    for j,k,l,p, res in zip(name,stars,review,duration, resonse):
        name_list.append(j.text)
        review_list.append(l.text)
        review_link.append(url)
        stars_list.append(int(str(k.text).split('/')[0]))
        time_list.append(p.text)
        shop_response = res.find_element(By.CLASS_NAME, 'wiI7pd').text
        # Check if there is a response from shop owner 
        if shop_response:
            has_response_list.append(True)
        else:
            has_response_list.append(False)
        response_list.append(shop_response)

# Save to CSV
review = pd.DataFrame(
    {'name': name_list,
     'review_content': review_list,
     'review_link': review_link,
     'rating': stars_list,
     'review_time_information': time_list,
     'has_response': has_response_list,
     'reply_from_owner': response_list
    })

review.to_csv('./google_review.csv',index=False)
