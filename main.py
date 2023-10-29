import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://vodiy.ua/pdr/test/?complect=6&theme=12&part=3'

s = Service(r"C:\Users\bekke\chomeDriver\chromedriver.exe")

driver = webdriver.Chrome(service=s)
driver.get(url)
indexes = {}
failed = {}
formatted = {}
is_end = False
while True:
    search = driver.find_element(By.CLASS_NAME, "ticketpage_ul")
    li = search.find_elements(By.TAG_NAME, "li")
    bar = driver.find_element(By.CLASS_NAME, "to_finish")
    to_finish = bar.find_element(By.TAG_NAME, "b").text
    count = 0
    current_q = 0
    is_refreshed = False
    for i in li:
        if is_refreshed:
            break
        tickets = i.find_elements(By.CLASS_NAME, "ticket_right")
        text = i.find_element(By.CLASS_NAME,"title_ticket")
        for t in tickets:
            driver.execute_script("arguments[0].scrollIntoView();", t)
            labels = i.find_elements(By.TAG_NAME, "label")
            label_index = 0
            if current_q in indexes:
                continue
            for l in labels:
                if l.is_displayed() and l.is_enabled() and count < int(to_finish) - 1:
                    if current_q in failed and label_index in failed[current_q]:
                        label_index += 1
                        continue
                    l.click()

                class_name = l.get_attribute("class")
                arr = class_name.split()
                if len(arr) == 2:
                    if arr[1] == "error_ticket":
                        if current_q in failed:
                            failed[current_q].append(label_index)
                        else:
                            failed[current_q] = [label_index]
                        driver.refresh()
                        is_refreshed = True
                        break
                    if arr[1] == "right_ticket":
                        indexes[current_q] = label_index
                        formatted[text.text] = label_index+1
                        break
                label_index += 1
            count += 1
        current_q += 1
        if len(indexes.keys()) == int(to_finish) - 1:
            is_end = True
            break
    if is_end:
        break

f = open("results.txt", "w")
s = ""
for d, k in formatted.items():
    s += F"{d} ans {k}\n"

f.write(s)
f.close()

driver.quit()
