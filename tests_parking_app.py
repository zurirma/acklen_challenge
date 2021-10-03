import select
import time

import pytest
from selenium import webdriver
from assertpy import assert_that
from selenium.webdriver.support.ui import Select
from helpers.parking_lots import ParkingLots


class TestParking:

    def setup_class(self):
        self.driver = webdriver.Chrome(executable_path='/Users/zury/PycharmProjects/challenge/drivers/chromedriver')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.shino.de/parkcalc/')

    @pytest.fixture
    def select_parking_lot(self, value):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value(value)

    def test_verify_title_app_and_lost_ticket_rule_appear_on_page(self):
        title = self.driver.find_element_by_class_name('PageTitle').text
        note = self.driver.find_element_by_xpath('/html/body/p[8]/i').text
        assert title == 'PARKING COST CALCULATOR'
        assert note == 'A Lost Ticket Fee of $10.00 will be assessed when the original parking stub cannot be produced' \
                       ' when exiting the parking facilities (does not apply to Valet Parking).'

    def test_valet_parking_cost_in_5_hours(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Valet')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '6:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 12.00'
        assert_that(estimated_time).contains('(0 Days, 5 Hours, 0 Minutes')

    def test_valet_parking_cost_in_more_than_5_hours(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Valet')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '6:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 18.00'
        assert_that(estimated_time).contains('(0 Days, 5 Hours, 1 Minutes')



    def test_verify_dropdown(self):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value('Short')
        assert opciones.get_attribute('name') == 'ParkingLot'
        print('Test completed')

    def teardown(self):
        self.driver.close()
        self.driver.quit()
