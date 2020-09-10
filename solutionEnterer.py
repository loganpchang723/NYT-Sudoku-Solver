#code within the driver function was used to figure out how to input solutions into the website baord

#NOTE: this was used for unit-testing...all final code was copy and pasted into 'test.py' and some code later changed for debugging purposes
from selenium import webdriver
import time
driver = webdriver.Chrome()
if __name__ == '__main__':
    boardArray = []
    driver.get("https://www.nytimes.com/puzzles/sudoku/easy")
    oneButton = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div[2]/div/div[3]/div/div[2]/div[8]')
    #board = driver.find_element_by_class_name('su-board')
    #box = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div[2]/div/div[1]/div/div/div/div[4]')
    for i in range (1,82):
        box = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div[2]/div/div[1]/div/div/div/div[' + str(i) + ']')
        fill = box.get_attribute('aria-label')
        if fill == 'empty':
            driver.execute_script("arguments[0].click()", box)
            driver.execute_script("arguments[0].click()", oneButton)

    time.sleep(5)
    driver.quit()
