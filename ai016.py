import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By


def crawl_data(page):
    # 初始化浏览器驱动
    driver = webdriver.Chrome()  # 这里使用Chrome浏览器，如果您使用其他浏览器，请相应地修改
    url = f"https://www.ai016.com/api/index/home/opusIndex?order=1&page={page}&size=18"
    driver.get(url)

    # 等待页面加载完成
    time.sleep(3)  # 根据需要调整等待时间

    # 提取数据
    data_element = driver.find_element(By.XPATH,"//pre")
    data_text = data_element.text

    # 关闭浏览器驱动
    driver.quit()

    return data_text


def extract_data(data_text):
    # 解析数据
    data = eval(data_text)['msg']['data']

    # 提取所需字段
    extracted_data = []
    for item in data:
        color = item.get('color', 'NULL')
        ai_model = item.get('ai_model', 'NULL')
        model_name = item.get('model_name', 'NULL')
        opus_keywords = item.get('opus_keywords', 'NULL')
        opus_order = item.get('opus_order', 'NULL')
        opus_pic = item.get('opus_pic', 'NULL')
        opus_title = item.get('opus_title', 'NULL')
        pic_height = item.get('pic_height', 'NULL')
        pic_width = item.get('pic_width', 'NULL')
        same_prompt = item.get('same_prompt', 'NULL')

        # 修改opus_pic字段的值
        opus_pic = f"https://www.ai016.com/prompt/{opus_order}"

        extracted_data.append([color, ai_model, model_name, opus_keywords, opus_order,
                               opus_pic, opus_title, pic_height, pic_width, same_prompt])

    return extracted_data


def write_to_excel(data, filename):
    try:
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Color', 'AI Model', 'Model Name', 'Opus Keywords', 'Opus Order',
                   'Opus Pic', 'Opus Title', 'Pic Height', 'Pic Width', 'Same Prompt'])

    for row in data:
        ws.append(row)

    wb.save(filename)


def main():
    page = 1
    filename = "ai016.xlsx"
    while True:
        try:
            data_text = crawl_data(page)
            extracted_data = extract_data(data_text)
            write_to_excel(extracted_data, filename)
            page += 1
        except:
            break


if __name__ == "__main__":
    main()
