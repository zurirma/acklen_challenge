from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class ParkingLots:
    def __init__(self, driver):
        self.driver = driver

    def select_parking_lot(self, value):
        opciones = self.driver.find_element_by_id('ParkingLot')
        seleccionar = Select(opciones)
        seleccionar.select_by_value(value)

    def input_entry_date_time(self, start_date, start_time):
        self.driver.find_element_by_id('StartingDate').clear()
        self.driver.find_element_by_id('StartingDate').send_keys(start_date)
        self.driver.find_element_by_id('StartingTime').clear()
        self.driver.find_element_by_id('StartingTime').send_keys(start_time)

    def input_leaving_date_time(self, leaving_date, leaving_time):
        self.driver.find_element_by_id('LeavingDate').clear()
        self.driver.find_element_by_id('LeavingDate').send_keys(leaving_date)
        self.driver.find_element_by_id('LeavingTime').clear()
        self.driver.find_element_by_id('LeavingTime').send_keys(leaving_time)

    def calculate_parking_costs(self):
        self.driver.find_element_by_name('Submit').click()
        estimated_parking_costs = self.driver.find_element_by_xpath(
            '/html/body/form/table/tbody/tr[4]/td[2]/span[1]').text
        return estimated_parking_costs

    def validate_estimated_time(self):
        estimated_time = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td[2]/span[2]').text
        return estimated_time






