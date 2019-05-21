from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time, os
from argparse import ArgumentParser

driver = webdriver.Firefox()
base_url = "https://catalogue.nlb.gov.sg"

def remove_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        print("file_name does not exist")


def search_book(book):
    driver.find_element_by_id('header-search-entry').send_keys(book)
    select = Select(driver.find_element_by_id('optionsDrop'))
    select.select_by_visible_text('Books')
    driver.find_element_by_id('header-search-submit').click()

def view_availability():
    screenshot = "nlb.png"
    time.sleep(3)
    link = driver.find_element_by_css_selector('div.card-text.availability a').get_attribute("href")
    print(link)
    # driver.find_element_by_css_selector('.card-title').click()
    # driver.find_element_by_xpath('//a[contains(text(), "View availability")]').click()
    driver.get(link)   
    remove_file(screenshot)
    driver.save_screenshot(screenshot)
    available_status = driver.find_elements_by_xpath("//span[contains(text(), 'Available')]")
    # available_libs = driver.find_elements_by_xpath("//span[contains(text(), 'Available')]/parent::td/parent::tr/td/span")

    time.sleep(10)
    for elt in available_status:
        print(elt.find_element_by_xpath("./parent::td/parent::tr/td/span").text)
    
    if len(available_status) == 0:
        print("book not available for loan")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-b' , '--book', action='store', dest='BOOK', default = "How Google tests software")
    parser = parser.parse_args()
    try:
        driver.get('https://catalogue.nlb.gov.sg')
        search_book(parser.BOOK)
        view_availability()
        driver.close()
    except Exception as e:
        print(e)
        driver.close()