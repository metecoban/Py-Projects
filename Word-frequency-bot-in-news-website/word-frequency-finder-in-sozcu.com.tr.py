from selenium import webdriver
import matplotlib.pyplot as plt
import pandas as pd


def set_lists_from_sozcu():
    browser.get("https://www.sozcu.com.tr/")
    browser.execute_script("window.scrollTo(0, 300)")
    for i in range(1, 12):
        browser.find_element_by_xpath('//*[@id="sz_manset"]/div[2]/span[' + str(i) + ']').click()
        browser.switch_to.window(browser.window_handles[1])
        if '/yazarlar/' in browser.current_url or not ('sozcu.com.tr' in browser.current_url):
            change_the_page()
            continue
        titles.append(browser.find_element_by_css_selector('.content-head h1').text)
        texts.append(browser.find_element_by_css_selector('.content-head h2').text)
        categorie_temp = browser.find_element_by_css_selector('div[class$="news-cat"] > a:nth-child(2)').text
        while " " in categorie_temp:
            categorie_temp = categorie_temp.replace(" ", "")
        categories.append(categorie_temp)
        dates.append(browser.find_element_by_css_selector('.date-time').text[20:])
        change_the_page()
    browser.close()


def change_the_page():
    window_after = browser.window_handles[0]
    browser.close()
    browser.switch_to.window(window_after)


def split_as_spaces(list1):
    new_list = []
    for i in list1:
        for j in i.split():
            new_list.append(j)
    return new_list


def word_frequency_with_dataframe():
    result_list = []
    for i in range(len(all_data.columns.values)):
        divided = split_as_spaces(all_data[all_data.columns.values[i]].tolist())
        result_list.append(frequency_finder(divided))
    return result_list


def word_frequency_for_category():
    result_list = []
    for i in range(len(category_data)):
        divided = list(category_data[i].values())
        result_list.append(frequency_finder(divided[0]))
    return result_list


def frequency_finder(divided_list):
    my_dict = {}
    while 0 < len(divided_list):
        value_count = divided_list.count(divided_list[0])
        my_dict[divided_list[0]] = value_count
        divided_string = divided_list[0]
        while divided_string in divided_list:
            divided_list.remove(divided_string)
    return my_dict


def category_control(demo_dates, demo_categories):
    general_list = []
    while 0 < len(demo_dates):
        tempo = demo_dates[0]
        date_count = demo_dates.count(tempo)
        mini_list = []
        for i in range(date_count):
            date_index = demo_dates.index(tempo)
            mini_list.append(demo_categories[date_index])
            demo_dates.pop(date_index)
            demo_categories.pop(date_index)
        mini_dict = {tempo: mini_list}
        general_list.append(mini_dict)
    return general_list


def create_plot(temp, label_name):
    if 80 < len(temp):
        plt.figure(figsize=(5, 35))
    elif 40 < len(temp):
        plt.figure(figsize=(5, 10))
    for i, v in enumerate(temp.values()):
        plt.text(v, i, str(v), color='blue', fontweight='bold')
    plt.barh(list(temp.keys()), list(temp.values()))
    if label_name == 'Categories Table':
        label_name = list(category_data[0].keys())[0] + " Category Table"
    plt.title(label_name)
    plt.show()


def send_for_plotting():
    name_of_list = ['Titles Table', 'Texts Table', ' Categories Table']
    for i in range(len(result)):
        if i >= 2:
            create_plot(result[i], list(category_data[i-2].keys())[0] + name_of_list[2])
        else:
            create_plot(result[i], name_of_list[i])
    print('Plot tables created.')


browser = webdriver.Chrome()  # Determine the path of your chromedriver.exe
titles, dates, categories, texts = [], [], [], []
set_lists_from_sozcu()
category_data = category_control(dates, categories)

data = {'Titles': titles,
        'Texts': texts}
all_data = pd.DataFrame(data)

dict_list = word_frequency_with_dataframe()
dict_list2 = word_frequency_for_category()
result = dict_list + dict_list2
send_for_plotting()
