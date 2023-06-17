
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

# 检查Excel文件是否存在，如果不存在则创建一个新的工作簿
excel_file = 'image_urls.xlsx'
if not os.path.exists(excel_file):
    workbook = openpyxl.Workbook()
else:
    workbook = openpyxl.load_workbook(excel_file)

# 创建或选择工作表
sheet = workbook.active

# 设置浏览器选项
options = webdriver.ChromeOptions()

# 创建WebDriver对象
driver = webdriver.Chrome(options=options)

pos = 1
while True:
    T=True
    options = webdriver.ChromeOptions()

    # 创建WebDriver对象
    driver = webdriver.Chrome(options=options)
    url = f"https://www.fiverr.com/categories/graphics-design/ai-art-prompt?source=pagination&pos=3&page={pos}&offset=-1"
    driver.get(url)
    while True:
        # 滚动到页面底部

        driver.execute_script("window.scrollBy(0, 500)")
        # 等待页面加载完成
        time.sleep(1)

        # 判断是否已滑动到页面底部
        if driver.execute_script("return window.scrollY >= 7000"):
            break
            #
            # T=False



    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/div/div/div/div/a[1]/div/div/div/img")))

    # 提取图片URL
    image_elements = driver.find_elements(By.XPATH, "//div/div/div/div/div/div/a[1]/div/div/div/img")
    image_urls = [element.get_attribute("src") for element in image_elements]

    # 存储图片URL到Excel
    for image_url in image_urls:
        sheet.append([image_url])

    # 保存数据到Excel
    workbook.save(excel_file)
    pos += 1
    # time.sleep(5000)

    # 关闭WebDriver
    driver.quit()

