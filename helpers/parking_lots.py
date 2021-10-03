from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class ParkingLots:
    def __init__(self, driver):
        self.driver = driver
        self.parking_lot = (By.ID, 'ParkingLot')
        self.starting_date = (By.ID, 'StartingDate')
        self.starting_time = (By.ID, 'StartingTime')
        self.leaving_date = (By.ID, 'LeavingDate')
        self.leaving_time = (By.ID, 'LeavingTime')
        self.calculate_button = (By.NAME, 'Submit')
        self.estimated_parking_costs = (By.XPATH, '/html/body/form/table/tbody/tr[4]/td[2]/span[1]')
        self.estimated_time = (By.XPATH, '/html/body/form/table/tbody/tr[4]/td[2]/span[2]')


    def select_parking_lot(self, value):
        opciones = self.driver.find_element_by_id(self.parking_lot)
        seleccionar = Select(opciones)
        seleccionar.select_by_value(value)

    def input_entry_date_time(self, start_date, start_time):
        self.driver.find_element_by_id(self.starting_date).clear()
        self.driver.find_element_by_id(self.starting_date).send_keys(start_date)
        self.driver.find_element_by_id(self.starting_time).clear()
        self.driver.find_element_by_id(self.starting_time).send_keys(start_time)

    def input_leaving_date_time(self, leaving_date, leaving_time):
        self.driver.find_element_by_id(self.leaving_date).clear()
        self.driver.find_element_by_id(self.leaving_date).send_keys(leaving_date)
        self.driver.find_element_by_id(self.leaving_time).clear()
        self.driver.find_element_by_id(self.leaving_time).send_keys(leaving_time)

    def calculate_parking_costs(self):
        self.driver.find_element_by_name(self.calculate_button).click()
        estimated_parking_costs = self.driver.find_element_by_xpath(
            self.estimated_parking_costs).text
        return estimated_parking_costs

    def validate_estimated_time(self):
        estimated_time = self.driver.find_element_by_xpath(self.estimated_time).text
        return estimated_time






