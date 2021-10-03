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

    def test_short_term_parking_cost_between_the_first_hour(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Short')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '1:59')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 2.00'
        assert_that(estimated_time).contains('(0 Days, 0 Hours, 59 Minutes')

    def test_short_term_parking_cost_in_an_hour_and_a_half(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Short')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '2:30')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 2.00'
        assert_that(estimated_time).contains('(0 Days, 1 Hours, 30 Minutes')

    def test_short_term_parking_cost_in_and_hour_and_thirty_one_minutes(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Short')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '2:31')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 4.00'
        assert_that(estimated_time).contains('(0 Days, 1 Hours, 31 Minutes')

    def test_short_term_parking_cost_for_one_day_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Short')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/03/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 25.00'
        assert_that(estimated_time).contains('(1 Days, 0 Hours, 1 Minutes')

    def test_short_term_parking_for_two_days_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Short')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/04/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 49.00'
        assert_that(estimated_time).contains('(2 Days, 0 Hours, 1 Minutes')

    def test_economy_lot_parking_cost_for_one_hour(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '2:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 2.00'
        assert_that(estimated_time).contains('(0 Days, 1 Hours, 0 Minutes')

    def test_economy_lot_parking_cost_for_one_day(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/03/2021', '1:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 9.00'
        assert_that(estimated_time).contains('(1 Days, 0 Hours, 0 Minutes')

    def test_economy_lot_parking_cost_for_one_day_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/03/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 11.00'
        assert_that(estimated_time).contains('(1 Days, 0 Hours, 1 Minutes')

    def test_economy_lot_parking_cost_for_six_days_and_23_hours(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/08/2021', '12:59')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 54.00'
        assert_that(estimated_time).contains('(5 Days, 23 Hours, 59 Minutes')

    def test_economy_lot_parking_cost_for_eight_days_sixty_one_minutes(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/10/2021', '2:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 67.00'
        assert_that(estimated_time).contains('(8 Days, 1 Hours, 1 Minutes')

    def test_economy_lot_parking_cost_for_fourteen_day(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Economy')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/16/2021', '1:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 108.00'
        assert_that(estimated_time).contains('(14 Days, 0 Hours, 0 Minutes')

    def test_long_term_garage_parking_cost_for_one_day_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Garage')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/03/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 14.00'
        assert_that(estimated_time).contains('(1 Days, 0 Hours, 1 Minutes')

    def test_long_term_garage_parking_cost_for_one_hour(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Garage')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '2:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 2.00'
        assert_that(estimated_time).contains('(0 Days, 1 Hours, 0 Minutes')

    def test_long_term_garage_parking_cost_for_seven_days_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Garage')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/09/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 74.00'
        assert_that(estimated_time).contains('(7 Days, 0 Hours, 1 Minutes')

    def test_long_term_surface_parking_cost_for_one_hour_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Surface')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/02/2021', '2:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 4.00'
        assert_that(estimated_time).contains('(0 Days, 1 Hours, 1 Minutes')

    def test_long_term_surface_parking_cost_for_one_day_and_one_minute(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Surface')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/03/2021', '1:01')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 12.00'
        assert_that(estimated_time).contains('(1 Days, 0 Hours, 1 Minutes')

    def test_long_term_surface_parking_cost_for_fourteen_days(self):
        select_parking_lot_and_dates = ParkingLots(self.driver)
        select_parking_lot_and_dates.select_parking_lot('Long-Surface')
        select_parking_lot_and_dates.input_entry_date_time('10/02/2021', '1:00')
        select_parking_lot_and_dates.input_leaving_date_time('10/16/2021', '1:00')
        time.sleep(5)
        estimated_parking_costs = ParkingLots(self.driver).calculate_parking_costs()
        estimated_time = ParkingLots(self.driver).validate_estimated_time()
        assert estimated_parking_costs == '$ 120.00'
        assert_that(estimated_time).contains('(14 Days, 0 Hours, 0 Minutes')

    def teardown(self):
        self.driver.close()
        self.driver.quit()
