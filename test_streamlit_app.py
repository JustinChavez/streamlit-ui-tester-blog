
from streamlit_ui_tester import Button, FileUploader, NumberInput, Selectbox

def test_sb_fixture(sb):
    # Open our test website and login with the test user
    sb.open("https://www.saucedemo.com")
    sb.type("#user-name", "standard_user")
    sb.type("#password", "secret_sauce")
    sb.click("input#login-button")

    # Verify that we have logged in by checking for the inventory element
    sb.assert_element("#inventory_container")


def test_button_click(sb):
    sb.open("http://streamlit:8501/button_click")

    # Wait for the Button element to appear
    sb.assert_text("Click Me")

    Button("Click Me", sb.driver).click_button()

    # The following text should appear if the button was clicked
    sb.assert_text("You clicked me!")

def test_file_upload(sb):
    sb.open("http://streamlit:8501/file_upload")

    # Wait for the File Upload element to appear
    sb.assert_text("Upload a file")

    FileUploader("Upload a file", sb.driver).enter_input_file("test.csv")

    # If a file successfully uploads its name should be visible
    sb.assert_text("test.csv")

def test_number_input(sb):
    sb.open("http://streamlit:8501/number_input")

    # Wait for the Number Input element to appear
    sb.assert_text("First Number")

    NumberInput("First Number", sb.driver).enter_text(1)
    NumberInput("Second Number", sb.driver).enter_text(2)

    Button("Add", sb.driver).click_button()

    sb.assert_text("3")

def test_selectbox(sb):
    sb.open("http://streamlit:8501/selectbox")

    # Wait for the SelectBox element to appear
    sb.assert_text("Subpage Navigator")

    # Select the second page
    Selectbox("Subpage Navigator", sb.driver).enter_text("Second Page").enter_return()

    # The following text should appear if the button was clicked
    sb.assert_text("Hello this is the Second Page")
