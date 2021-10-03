from selenium import webdriver
from selenium.webdriver.support.ui import Select


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





