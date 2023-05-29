from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import csv
import time

def efreshData_csv():
    keys = ["배달", "밥집", "카페", "술집", "고깃집", "횟집", "한식", "중식", "일식", "양식", "아시안", "멕시칸", "이탈리안", "뷔폐", "브런치", "패스트푸드", "분식", "국물요리", "면요리", "해산물"]
    ages = ["20대", "30대", "40대", "50대", "60대%20이상"]
    purposes = ["아침식사", "점심식사", "저녁식사", "혼밥", "혼술", "혼카페", "데이트", "회식", "건강식", "다이어트", "가족외식", "아이동반", "실버푸드", "식사모임", "술모임", "차모임", "접대", "간식"]
    moods = ["가성비좋은", "분위기좋은", "푸짐한", "격식있는", "고급스러운", "서민적인", "시끌벅적한", "조용한", "깔끔한", "이색적인", "뷰가좋은", "예쁜", "지역주민이찾는"]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--virtual-time-budget=10000')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    driver = webdriver.Chrome(options=chrome_options)

    def return_store(factors, num):
        for factor in factors:
            driver.get('https://www.diningcode.com/list.dc?query=%EA%B4%91%EC%A3%BC%20%EC%B6%A9%EC%9E%A5%EB%A1%9C' + f'&keyword={factor}')
            extracted_text = []

            wait = WebDriverWait(driver, 10)
            scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]')))

            last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

            while True:
                actions = ActionChains(driver)
                actions.move_to_element(scroll_element).perform()
                driver.execute_script("arguments[0].scrollBy(0, 5000)", scroll_element)

                time.sleep(0.5)

                new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

                if new_height == last_height:
                    try:
                        for i in range(1, 100):
                            title = driver.find_elements(By.XPATH, f'/html/body/div/div/div[1]/div[3]/a[{i}]/div[1]/div/div[1]/h2')
                            Restaurant_Menu_list_innerHTML = title[0].get_property("innerHTML")
                            match = re.search(r'\d+\.\s+(.*?)\s+<', Restaurant_Menu_list_innerHTML)
                            extracted_text.append(match.group(1))
                    except:
                        pass
                    break

                last_height = new_height

            with open('stores.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

            for row in rows:
                if row[0] in extracted_text:
                    row[num] = eval(row[num])
                    row[num].append(factor)

            with open('stores.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    csv_file = 'stores.csv'

    with open(csv_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['가게이름', '카테고리', '주소', '전화번호', '영업시간', '메뉴', '최소가격', '최대가격', '차액', '평점', '사진', '주소', '나이대', '분위기', '목적'])

        for key in keys:
            driver.get('https://www.diningcode.com/list.dc?query=%EA%B4%91%EC%A3%BC%20%EC%B6%A9%EC%9E%A5%EB%A1%9C' + f'&keyword={key}')
            
            wait = WebDriverWait(driver, 10)
            scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]')))

            last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

            while True:
                actions = ActionChains(driver)
                actions.move_to_element(scroll_element).perform()
                driver.execute_script("arguments[0].scrollBy(0, 5000)", scroll_element)

                time.sleep(1)

                new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

                if new_height == last_height:
                    break

                last_height = new_height

            web = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[3]')))
            innerHTML = web[0].get_property("innerHTML")
            href_list = re.findall(re.compile(r'href="([^"]*)"'), innerHTML)

            for href in href_list:
                driver.get('https://www.diningcode.com' + f'{href}')

                driver.execute_script("""
                    var adElements = document.querySelectorAll('#div_profile > div.grp_ads, #google-ad-area');
                    for (var i = 0; i < adElements.length; i++) {
                        adElements[i].style.display = 'none';
                    }
                """)

                title =  driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[1]/div[1]/p')[0].text
                address_1 = driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[2]/ul/li[1]/a[2]')[0].text
                address_2 = driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[2]/ul/li[1]/a[3]')[0].text
                address_3 = driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[2]/ul/li[1]/span')[0].text
                Phone_number = driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[2]/ul/li[2]')[0].text
                try:
                    open_day = driver.find_elements(By.XPATH, '//*[@id="div_detail"]/div[1]/ul/li/p[1]')[0].text
                    open_time = driver.find_elements(By.XPATH, '//*[@id="div_detail"]/div[1]/ul/li/p[2]')[0].text
                    if "<span" in open_day:
                        open_day = "게시되지 않음"
                        open_time = None
                except:
                    open_day = "게시되지 않음"
                    open_time = None

                try:
                    Restaurant_Menu_list = driver.find_elements(By.XPATH, '//*[@id="div_detail"]/div[2]/ul')
                    Restaurant_Menu_list_innerHTML = Restaurant_Menu_list[0].get_property("innerHTML")
                except:
                    try:
                        Restaurant_Menu_list = driver.find_elements(By.XPATH, '//*[@id="div_detail"]/div[1]/ul')
                        Restaurant_Menu_list_innerHTML = Restaurant_Menu_list[0].get_property("innerHTML")
                    except:
                        Restaurant_Menu_list = None
                        Restaurant_Menu_list_innerHTML = None

                if Restaurant_Menu_list_innerHTML != None:
                    Menu_list = re.findall(re.compile(r'<span class="Restaurant_Menu">(.*?)</span>'), Restaurant_Menu_list_innerHTML)
                    Menu_price_list = re.findall(re.compile(r'<p class="r-txt Restaurant_MenuPrice">(.*?)</p>'), Restaurant_Menu_list_innerHTML)
                    if Menu_list:
                        lst = []
                        for item in Menu_price_list:
                            try:
                                value = int(item.replace(',', '').replace('원', ''))
                                lst.append(value)
                            except ValueError:
                                pass
                            
                        min_value = 0           
                        if lst:
                            min_value = min(lst)
                            max_value = max(lst)
                            difference = max_value - min_value
                    else:
                        Menu_list = None
                        Menu_price_list = None
                        min_value = 0
                        max_value = 0
                        difference = 0

                else:
                    Menu_list = None
                    Menu_price_list = None
                    min_value = 0
                    max_value = 0
                    difference = 0

                try:
                    review = driver.find_elements(By.XPATH, '//*[@id="lbl_review_point"]')[0].text
                except:
                    review = "게시되지 않음"

                try:
                    img = driver.find_elements(By.XPATH, '//*[@id="div_profile"]/div[1]/ul/li[1]/img')
                    img_src = img[0].get_attribute("src")
                except:
                    img_src = "게시되지 않음"

                writer.writerow([title, key, f"광주시 {address_1} {address_2} {address_3}", Phone_number, f"{open_day} {open_time}", Menu_list, Menu_price_list, min_value, max_value, difference, review, img_src, 'https://www.diningcode.com' + f'{href}', [], [], []])

        for factor, number in [(ages, 13), (purposes, 14), (moods, 15)]:
            return_store(factor, number)

    print(f'작업이 완료되었습니다.')