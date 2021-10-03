import select
import time

from _pytest.fixtures import fixture
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Test_Parking:

    def setup_class(self):
        self.driver = webdriver.Chrome(executable_path='/Users/zury/PycharmProjects/challenge/drivers/chromedriver')
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.shino.de/parkcalc/')
        self.driver.maximize_window()

    def test_verify_title_app_and_lost_ticket_rule_appear_on_page(self):
        title = self.driver.find_element_by_class_name('PageTitle').text
        note = self.driver.find_element_by_xpath('/html/body/p[8]/i').text
        assert title == 'PARKING COST CALCULATOR'
        assert note == 'A Lost Ticket Fee of $10.00 will be assessed when the original parking stub cannot be produced' \
                       ' when exiting the parking facilities (does not apply to Valet Parking).'


    def test_valet_parking_cost_in_5_hours(self):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value('Valet')
        self.driver.find_element_by_id('StartingDate').clear()
        self.driver.find_element_by_id('StartingDate').send_keys('10/02/2021')
        self.driver.find_element_by_id('StartingTime').clear()
        self.driver.find_element_by_id('StartingTime').send_keys('1:00')
        self.driver.find_element_by_id('LeavingDate').clear()
        self.driver.find_element_by_id('LeavingDate').send_keys('10/02/2021')
        self.driver.find_element_by_id('LeavingTime').clear()
        self.driver.find_element_by_id('LeavingTime').send_keys('6:00')
        time.sleep(5)
        self.driver.find_element_by_name('Submit').click()
        estimated_parking_costs = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td[2]/span[1]').text
        estimated_time = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td[2]/span[2]').text
        assert estimated_parking_costs == '$ 12.00'
        assert estimated_time == '        (0 Days, 5 Hours, 0 Minutes)'

    def test_verify_dropdown(self):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value('Short')
        assert opciones.get_attribute('name') == 'ParkingLot'
        print('Test completed')

    def teardown(self):
        self.driver.close()
        self.driver.quit()

