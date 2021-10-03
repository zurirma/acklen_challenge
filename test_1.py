import select

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Test_Parking:

    def setup_class(self):
        self.driver = webdriver.Chrome(executable_path='/Users/zury/PycharmProjects/challenge/drivers/chromedriver')
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.shino.de/parkcalc/')
        self.driver.maximize_window()

    def test_verify_dropdown(self):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value('Short')
        assert opciones.get_attribute('name') == 'ParkingLot'
        self.driver.close()
        self.driver.quit()
        print('Test completed')
