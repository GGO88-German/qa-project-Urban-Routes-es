import data

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException

    code = None

    for i in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log("performance")
                if log.get("message")
                and "api/v1/number?number" in log.get("message")
            ]

            for log in reversed(logs):
                message_data = json.loads(log)["message"]

                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {
                        "requestId":
                            message_data["params"]["requestId"]
                    }
                )

                code = "".join(
                    [
                        character
                        for character in body["body"]
                        if character.isdigit()
                    ]
                )

        except WebDriverException:
            time.sleep(1)
            continue

        if not code:
            raise Exception(
                "No se encontró el código de confirmación del teléfono.\n"
                "Utiliza 'retrieve_phone_code' solo después de haber "
                "solicitado el código en tu aplicación."
            )

        return code


class UrbanRoutesPage:
    # Ruta
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")

    order_taxi_button = (
        By.XPATH,
        "//button[contains(., 'Pedir un taxi')]"
    )

    # Tarifa Comfort
    comfort_tariff = (
        By.XPATH,
        "//div[normalize-space()='Comfort']"
    )

    selected_tariff = (
        By.CSS_SELECTOR,
        ".tcard.active"
    )

    # Teléfono
    phone_button = (
        By.CSS_SELECTOR,
        ".np-button"
    )

    phone_input = (
        By.ID,
        "phone"
    )

    phone_next_button = (
        By.CSS_SELECTOR,
        ".number-picker .section.active button[type='submit']"
    )

    phone_code_input = (
        By.ID,
        "code"
    )

    phone_confirm_button = (
        By.CSS_SELECTOR,
        ".number-picker .section.active button[type='submit']"
    )

    # Método de pago
    payment_method_button = (
        By.CSS_SELECTOR,
        ".pp-button"
    )

    add_card_button = (
        By.CSS_SELECTOR,
        ".pp-plus"
    )

    card_number_input = (
        By.CSS_SELECTOR,
        ".payment-picker .section.active input#number"
    )

    card_code_input = (
        By.CSS_SELECTOR,
        ".payment-picker .section.active input#code"
    )

    add_card_submit_button = (
        By.CSS_SELECTOR,
        ".payment-picker .section.active button[type='submit']"
    )

    payment_close_button = (
        By.CSS_SELECTOR,
        ".payment-picker .section.active .section-close"
    )

    payment_overlay = (
        By.CSS_SELECTOR,
        ".payment-picker.open .overlay"
    )

    selected_payment_method = (
        By.CSS_SELECTOR,
        ".pp-value-text"
    )

    # Mensaje para el conductor
    driver_message_input = (
        By.ID,
        "comment"
    )

    # Manta y pañuelos
    blanket_switch = (
        By.XPATH,
        "//div[contains(@class, 'r-type-switch')]"
        "[.//div[normalize-space()='Manta y pañuelos']]"
        "//span[contains(@class, 'slider')]"
    )

    blanket_checkbox = (
        By.XPATH,
        "//div[contains(@class, 'r-type-switch')]"
        "[.//div[normalize-space()='Manta y pañuelos']]"
        "//input[@type='checkbox']"
    )

    # Cubetas de helado
    ice_cream_plus_button = (
        By.CSS_SELECTOR,
        ".counter-plus"
    )

    ice_cream_counter_value = (
        By.CSS_SELECTOR,
        ".counter-value"
    )

    # Botón final y ventana del pedido
    final_order_button = (
        By.CSS_SELECTOR,
        "button.smart-button"
    )

    order_header_title = (
        By.CSS_SELECTOR,
        ".order-header-title"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Métodos de la ruta
    def wait_for_load(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.from_field
            )
        )

        self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.to_field
            )
        )

    def set_from(self, from_address):
        from_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.from_field
            )
        )
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        to_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.to_field
            )
        )
        to_element.send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.wait_for_load()
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(
            *self.from_field
        ).get_property("value")

    def get_to(self):
        return self.driver.find_element(
            *self.to_field
        ).get_property("value")

    # Métodos de la tarifa
    def click_order_taxi(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.order_taxi_button
            )
        )
        button.click()

    def select_comfort(self):
        comfort = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.comfort_tariff
            )
        )
        comfort.click()

    def get_selected_tariff(self):
        selected = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.selected_tariff
            )
        )
        return selected.text

    # Métodos del teléfono
    def click_phone_button(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.phone_button
            )
        )
        button.click()

    def set_phone(self, phone_number):
        phone_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.phone_input
            )
        )
        phone_element.clear()
        phone_element.send_keys(phone_number)

    def click_phone_next(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.phone_next_button
            )
        )
        button.click()

        self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.phone_code_input
            )
        )

    def set_phone_code(self, code):
        code_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.phone_code_input
            )
        )
        code_element.send_keys(code)

    def click_phone_confirm(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.phone_confirm_button
            )
        )
        button.click()

    # Métodos de la tarjeta
    def click_payment_method(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.payment_method_button
            )
        )
        button.click()

    def click_add_card(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.add_card_button
            )
        )
        button.click()

    def set_card_number(self, card_number):
        number_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.card_number_input
            )
        )
        number_element.send_keys(card_number)

    def set_card_code(self, card_code):
        code_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.card_code_input
            )
        )
        code_element.send_keys(card_code)
        code_element.send_keys(Keys.TAB)

    def click_add_card_submit(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.add_card_submit_button
            )
        )
        button.click()

    def close_payment_method(self):
        close_button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.payment_close_button
            )
        )
        close_button.click()

        self.wait.until(
            expected_conditions.invisibility_of_element_located(
                self.payment_overlay
            )
        )

    def get_selected_payment_method(self):
        payment = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.selected_payment_method
            )
        )
        return payment.text

    # Métodos del mensaje
    def set_message_for_driver(self, message):
        message_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.driver_message_input
            )
        )
        message_element.clear()
        message_element.send_keys(message)

    def get_message_for_driver(self):
        message_element = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.driver_message_input
            )
        )
        return message_element.get_property("value")

    # Métodos de Manta y pañuelos
    def select_blanket_and_handkerchiefs(self):
        switch = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.blanket_switch
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            switch
        )

        switch.click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(
            expected_conditions.presence_of_element_located(
                self.blanket_checkbox
            )
        )
        return checkbox.is_selected()

    # Métodos de Cubeta de helado
    def add_ice_cream(self):
        plus_button = self.wait.until(
            expected_conditions.presence_of_element_located(
                self.ice_cream_plus_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            plus_button
        )

        plus_button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.ice_cream_plus_button
            )
        )

        plus_button.click()

    def get_ice_cream_count(self):
        counter = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.ice_cream_counter_value
            )
        )
        return int(counter.text)

    # Métodos para pedir el taxi
    def click_final_order_button(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                self.final_order_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        button.click()

    def get_order_header_title(self):
        title = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.order_header_title
            )
        )
        return title.text

    def wait_for_driver_information(self):
        driver_wait = WebDriverWait(
            self.driver,
            60
        )

        driver_wait.until(
            lambda driver: (
                driver.find_element(
                    *self.order_header_title
                ).text.strip()
                not in ("", "Buscar automóvil")
            )
        )

        return self.driver.find_element(
            *self.order_header_title
        ).text


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = webdriver.ChromeOptions()

        options.set_capability(
            "goog:loggingPrefs",
            {
                "performance": "ALL"
            }
        )

        cls.driver = webdriver.Chrome(
            options=options
        )

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_order_taxi()
        routes_page.select_comfort()

        assert (
            "Comfort"
            in routes_page.get_selected_tariff()
        )

    def test_set_phone(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_phone_next()

        confirmation_code = retrieve_phone_code(
            self.driver
        )

        routes_page.set_phone_code(
            confirmation_code
        )
        routes_page.click_phone_confirm()

    def test_add_card(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_add_card_submit()
        routes_page.close_payment_method()

        assert (
            "Tarjeta"
            in routes_page.get_selected_payment_method()
        )

    def test_set_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_message_for_driver(
            data.message_for_driver
        )

        assert (
            routes_page.get_message_for_driver()
            == data.message_for_driver
        )

    def test_select_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.select_blanket_and_handkerchiefs()

        assert (
            routes_page.is_blanket_and_handkerchiefs_selected()
        )

    def test_add_two_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.add_ice_cream()
        routes_page.add_ice_cream()

        assert routes_page.get_ice_cream_count() == 2

    def test_order_taxi_and_wait_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_final_order_button()

        assert (
            routes_page.get_order_header_title()
            == "Buscar automóvil"
        )

        driver_information = (
            routes_page.wait_for_driver_information()
        )

        assert driver_information != "Buscar automóvil"
        assert driver_information != ""

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()