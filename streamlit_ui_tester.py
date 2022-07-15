"""
Streamlit Element: HTML tag that contains the Streamlit Widget.
Contains the label(s) and the interaction tag.

Label: Unique string identifier of each Streamlit widget. Displayed to the user within the
label tag. In the case of the radio button (and maybe checklist), there are multiple labels 
and the first one corresponds to the unique identifying Label.

Interaction Element: Selenium element that points to the HTML tag that records the user 
interaction. Usually the input tag (text input, file upload) or a button tag (clickable button)
"""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Element:
    def __init__(self, st_label, selenium_driver):
        self.st_label = st_label
        self.selenium_driver = selenium_driver

        # Will be initialized by the find_* functions
        self.interact_element = None

    def __select_element(self, search_elements: List, interact_element_type, text_in_label=True):
        """
        Searches for the Streamlit element text that matches the instance variable
        st_label. When found it sets the instance variable interact_element to be the containing
        core interaction tag.

        Args:
            search_elements: List of selenium elements to search through
            interact_element_type: The type of interaction tag contained in the streamlit element
            text_in_label: If true, the st_label text will be within the first label tag
              If false, the st_label text is within a different sub tag.

        Returns:
            None

        Raises:
            ValueError: An element matching the class variable st_label
              could not be found
        """
        for element in search_elements:
            if text_in_label:
                text = element.find_element(By.TAG_NAME, "label").text
            else:
                text = element.text
            if text == self.st_label:
                self.interact_element = element.find_element(By.TAG_NAME, interact_element_type)
                return
        raise ValueError(f"Could not find input with label: {self.st_label}")

    def _find_class_by_single_label(self, class_name):
        """Streamlit Element contains a single label with an input interaction tag"""
        self.__select_element(
            search_elements=self.selenium_driver.find_elements(By.CLASS_NAME, class_name),
            interact_element_type="input",
        )

    def _find_button_element(self, class_name):
        """Streamlit Element contains a single label with a button interaction tag"""
        self.__select_element(
            search_elements=self.selenium_driver.find_elements(By.CLASS_NAME, class_name),
            interact_element_type="button",
            text_in_label=False,
        )

    def _find_file_input_element(self, css_selector):
        """Streamlit Element classname is contained within a custom attribute with a input interaction tag"""
        self.__select_element(
            search_elements=self.selenium_driver.find_elements(By.CSS_SELECTOR, css_selector),
            interact_element_type="input",
        )

    def _find_checkbox_element(self, class_name):
        self.__select_element(
            search_elements=self.selenium_driver.find_elements(By.CLASS_NAME, class_name),
            interact_element_type="span",
        )

    def _find_class_by_multi_label(self, class_name):
        """
        Streamlit Element contains multiple labels. The first label contains the identifier.
        The other labels are the options."""
        for element in self.selenium_driver.find_elements(By.CLASS_NAME, class_name):
            if element.find_element(By.TAG_NAME, "label").text == self.st_label:
                self.interact_element = element
                return
        raise ValueError(f"Could not find a Radio Button selection with label: {self.st_label}")

    def enter_text(self, input):
        """Any pre-existing text, such as placeholders, is deleted before we enter the input"""
        self.interact_element.send_keys(Keys.CONTROL + "a")
        self.interact_element.send_keys(Keys.DELETE)
        self.interact_element.send_keys(input)
        # Return Self to chain action commands
        return self

    def enter_return(self):
        self.interact_element.send_keys(Keys.RETURN)
        return self


class NumberInput(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_class_by_single_label("stNumberInput")


class TextInput(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_class_by_single_label("stTextInput")


class Selectbox(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_class_by_single_label("stSelectbox")


class Checkbox(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_checkbox_element("stCheckbox")

    def check_box(self):
        self.interact_element.click()


class Radio(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_class_by_multi_label("stRadio")

    def select_radio_option(self, option_text):
        all_labels = self.interact_element.find_elements(By.TAG_NAME, "label")
        # Skip the first label tag since it is the label for the group and not an option
        for label in all_labels[1:]:
            if label.text == option_text:
                label.click()
                return
        raise ValueError(f"Could not find a Radio Button option with label: {option_text}")

    def get_radio_options(self):
        options = []
        all_labels = self.interact_element.find_elements(By.TAG_NAME, "label")
        for label in all_labels[1:]:
            options.append(label.text)
        return options


class FileUploader(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_file_input_element('[data-testid="stFileUploader"]')

    def enter_input_file(self, input):
        self.interact_element.send_keys(input)


class Button(Element):
    def __init__(self, st_label, selenium_driver):
        super().__init__(st_label, selenium_driver)
        self._find_button_element("stButton")

    def click_button(self):
        self.interact_element.click()