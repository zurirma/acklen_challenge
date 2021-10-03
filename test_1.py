import select

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Test_Parking:

    def test_1(self):
        driver = webdriver.Chrome(executable_path='/Users/zury/PycharmProjects/challenge/drivers/chromedriver')

        driver.implicitly_wait(10)
        driver.maximize_window()

        driver.get('http://www.shino.de/parkcalc/')
        opciones = driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value('Short')
        assert opciones.get_attribute('name') == 'ParkingLot'

        driver.close()
        driver.quit()
        print('Test completed')








