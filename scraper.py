#code within the driver function was used to figure out how to scrape the board from the website

#NOTE: this was used for unit-testing...all final code was copy and pasted into 'test.py' and some code later changed for debugging purposes
from selenium import webdriver
import time
driver = webdriver.Chrome()
if __name__ == '__main__':
    boardArray = []
    driver.get("https://www.nytimes.com/puzzles/sudoku/easy")
    board = driver.find_element_by_class_name('su-board')
    stringRep = ''
    for i in range(1,82):
        elem = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div[2]/div/div[1]/div/div/div/div['+str(i)+']').get_attribute('aria-label')
        digit = '0'
        if elem != 'empty':
            digit = elem
        stringRep += digit
        if i%9 == 0:
            boardArray.append(stringRep)
            stringRep = ''
    for i in range (0,9):
        print(boardArray[i])
    time.sleep(5)
    driver.quit()
