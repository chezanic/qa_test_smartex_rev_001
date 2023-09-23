
from selenium import webdriver

username = "standard_user"
wrong_username = "test"
password = "secret_sauce"

url = "https://www.saucedemo.com/"


def open_main_page():
    driver.get(url)


def test_login_success():
    open_main_page()

    driver.find_element("id", "user-name").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("id", "login-button").click()

    if driver.current_url.endswith("inventory.html"):
        return True
    else:
        return False


def test_invalid_login():
    open_main_page()

    driver.find_element("id", "user-name").send_keys(wrong_username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("id", "login-button").click()

    error_message = driver.find_element("xpath", "//div[contains(@class, 'error-message-container error')]/h3").text

    if error_message == "Epic sadface: Username and password do not match any user in this service":
        return True
    else:
        return False


def test_blank_login():
    open_main_page()

    driver.find_element("id", "user-name").send_keys()
    driver.find_element("id", "password").send_keys()
    driver.find_element("id", "login-button").click()

    error_message = driver.find_element("xpath", "//div[contains(@class, 'error-message-container error')]/h3").text

    if error_message == "Epic sadface: Username is required":
        return True
    else:
        return False


class TestContainer:

    def __init__(self, resport_file_name):
        self.report_file_name = resport_file_name
        self.tests = []

    def add_test(self, test_name, test_function):
        self.tests.append({"test_name": test_name, "test_function": test_function, "test_passed": False})

    def run_test(self):
        for test in self.tests:
            test["test_passed"] = test["test_function"]()

    def export(self):
        with open(self.report_file_name, "w") as file:
            for test in self.tests:
                file.write(test["test_name"] + ": ")
                if test["test_passed"]:
                    file.write("test passed\n")
                else:
                    file.write("test failed\n")


if __name__ == "__main__":
    driver = webdriver.Firefox()

    test_container = TestContainer("qa_report")
    test_container.add_test("Verify Correct Login", test_login_success)
    test_container.add_test("Verify Invalid Login", test_invalid_login)
    test_container.add_test("Verify Blank Login", test_blank_login)
    test_container.run_test()
    test_container.export()

    driver.quit()
