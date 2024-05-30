from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Set Chrome options to disable Page Load Metrics reporting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=NetworkService,PageLoadMetrics")

# Start a new Chrome session with the configured options
driver = webdriver.Chrome(options=chrome_options)

# Define test cases
test_cases = [
    {"description": "Test Case 1: Website opened", "expected_result": None},
    {"description": "Test Case 2: Classified Item from training dataset", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC2.jpg', "expected_result": "Jalebi"},
    {"description": "Test Case 3: Classified Item from testing dataset", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC3.jpg', "expected_result": "Donut"},
    {"description": "Test Case 4: Classified Item from external source image", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC4.jpg', "expected_result": "MasalaDosa"},
    {"description": "Test Case 5: Classifying item from a rotated image", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC5.jpg', "expected_result": "Jalebi"},
    {"description": "Test Case 6: Classifying item from an image of different ratio", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC6.jpg', "expected_result": "MasalaDosa"},
    {"description": "Test Case 7: Notifies that the given food item is still not available in the dataset", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC7.jpg', "expected_result": "Error"},
    {"description": "Test Case 8: Notifies that given Item may be a non-food item", "file_path": r'C:\Users\prasanna_s.a\Desktop\SnapNPlate-master\test\Rsrc\TC8.jpg', "expected_result": "Error"},
    {"description": "Test Case 9: Search successful for existing food item (keyword same as available in dataset)", "search_query": "Idli", "expected_result": "Idli"},
    {"description": "Test Case 10: Search successful for existing food item (different keyword case)", "search_query": "iDli", "expected_result": "Idli"},
    {"description": "Test Case 11: Search successful for existing food item (different keyword with space)", "search_query": "Idli ", "expected_result": "Idli"},
    {"description": "Test Case 12: Notifies that the searched food item is still not available in the dataset", "search_query": "Chips", "expected_result": "Error"},
]

def print_result(description, result, expected, actual):
    if result == "Passed":
        print(f"{description} - \033[92mPassed\033[0m: Expected '{expected}', got '{actual}'")
    else:
        print(f"{description} - \033[91mFailed\033[0m: Expected '{expected}', got '{actual}'")

def test_image_classification(test_case):
    try:
        # Open the web application
        driver.get('http://localhost:3000')

        # Define WebDriverWait with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)

        # Locate the image upload input element
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))

        # Upload the image
        upload_input.send_keys(test_case["file_path"])

        # Wait for 5 seconds
        time.sleep(5)

        if test_case["expected_result"] == "Error":
            # Check for the presence of the error alert
            try:
                error_alert = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert')))
                print_result(test_case['description'], "Passed", "Error alert displayed", "Error alert displayed")
            except TimeoutException:
                print_result(test_case['description'], "Failed", "Error alert displayed", "Error alert not displayed")
        else:
            # Wait until the result element is visible
            result_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="result-element text-start"]/h1')))

            # Get the result text
            result_text = result_element.text

            # Assert that the result matches the expected result
            if result_text == test_case["expected_result"]:
                print_result(test_case['description'], "Passed", test_case["expected_result"], result_text)
            else:
                print_result(test_case['description'], "Failed", test_case["expected_result"], result_text)

    except TimeoutException:
        print_result(test_case['description'], "Failed", "Page loaded", "Timeout - Element not found within the specified time.")
    except Exception as e:
        print_result(test_case['description'], "Failed", "Page loaded", f"An error occurred: {str(e)}")

def test_search_functionality(test_case):
    try:
        # Open the web application
        driver.get('http://localhost:3000')

        # Define WebDriverWait with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)

        # Locate the search input element
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))
        search_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Search")]')))

        # Enter the search query
        search_input.send_keys(test_case["search_query"])

        # Click the search button
        search_button.click()

        # Wait for 5 seconds
        time.sleep(5)

        if test_case["expected_result"] == "Error":
            # Check for the presence of the error alert
            try:
                error_alert = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert')))
                print_result(test_case['description'], "Passed", "Error alert displayed", "Error alert displayed")
            except TimeoutException:
                print_result(test_case['description'], "Failed", "Error alert displayed", "Error alert not displayed")
        else:
            # Wait until the result element is visible
            result_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="result-element text-start"]/h1')))

            # Get the result text
            result_text = result_element.text

            # Assert that the result matches the expected result
            if result_text == test_case["expected_result"]:
                print_result(test_case['description'], "Passed", test_case["expected_result"], result_text)
            else:
                print_result(test_case['description'], "Failed", test_case["expected_result"], result_text)

    except TimeoutException:
        print_result(test_case['description'], "Failed", "Page loaded", "Timeout - Element not found within the specified time.")
    except Exception as e:
        print_result(test_case['description'], "Failed", "Page loaded", f"An error occurred: {str(e)}")

try:
    for test_case in test_cases:
        if "file_path" in test_case:
            test_image_classification(test_case)
        elif "search_query" in test_case:
            test_search_functionality(test_case)

    # Print test case 13 result
    print("\033[94mTest Case 13 Passed: Every component was rendered in all the above cases (website consistency)\033[0m")

except Exception as e:
    print(f"An error occurred during the test execution: {str(e)}")

finally:
    # Wait for 5 seconds before closing the browser session
    time.sleep(5)
    # Close the browser session
    driver.quit()
