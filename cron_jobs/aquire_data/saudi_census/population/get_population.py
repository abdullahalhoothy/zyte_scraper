import os
import csv
import logging
import json
import time
from typing import List, Dict, Any
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)

from bs4 import BeautifulSoup

# Add this near the top of the file, after imports
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Change the logging.basicConfig line to:
log_file_path = os.path.join(MODULE_DIR, "get_population.log")
if os.path.exists(log_file_path):
    os.remove(log_file_path)
    print("Log file removed.")
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    encoding="utf-8",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def get_intel_mac_driver():
    """
    Create an Intel Mac-compatible ChromeDriver instance

    Returns:
        Configured WebDriver instance
    """
    # Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    driver_path = "/usr/local/bin/chromedriver"
    service = Service(driver_path)
    # Create and return the driver
    return webdriver.Chrome(service=service, options=chrome_options)


class Map:
    def __init__(self, url: str, locations: List[str]):
        """
        Initialize the scraper with configuration for web scraping

        """
        # Chrome options for headless browsing
        self.chrome_options = Options()
        self.chrome_options.add_argument("--lang=en-US")
        self.chrome_options.add_argument("--start-maximized")

        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")

        # Setup webdriver
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # self.driver =  get_intel_mac_driver()
        self.url = url
        self.locations = locations
        self.wait = WebDriverWait(self.driver, 30)
        self.actions = webdriver.ActionChains(self.driver)

    def navigate_and_extract(self):
        """
        Navigate to each URL and extract endpoint details
        """
        try:
            self.driver.get(self.url)
            time.sleep(3)
            self.driver.execute_script("document.body.style.zoom='60%'")
            self._switch_to_iframe(self.driver)
            # self._hide_unwanted_divs()
            for location in self.locations:
                self._search_by_location(location)
                for zoom_level in range(1, 7):
                    self._systematic_map_navigation(location)
                    self._zoom_in_on_map()
                    logging.info(f"Zoomed {zoom_level} times.")
                    time.sleep(15)
        except Exception as e:
            logging.error(f"Error processing : {e}")

    def _switch_to_iframe(self, driver):
        try:
            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
            )
            logging.info("Switched to iframe successfully.")
        except TimeoutException:
            logging.error("No iframe found or timeout while switching to iframe.")
            raise

    def _search_by_location(self, location):
        try:
            logging.info(msg=f"Searching for location : {location}")
            search_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", search_input
            )
            self.driver.execute_script("arguments[0].click();", search_input)
            search_input.clear()
            search_input.send_keys(f"{location}, Saudi Arabia")
            search_input.submit()
            search_input.clear()
            time.sleep(13)
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error navigating to URL: {e}")
            raise
        except Exception as e:
            logging.error(f"Error searching for location: {str(e)}")
            raise

    def _hover_top_left(self, element):
        try:
            self.driver.execute_script(
                """
            function simulateClickAndHover(element) {
                const rect = element.getBoundingClientRect();
                const events = ['mouseover', 'mousedown', 'mouseup', 'mousemove'];
                events.forEach(eventName => {
                    const event = new MouseEvent(eventName, {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: rect.left,
                        clientY: rect.top
                    });
                    element.dispatchEvent(event);
                });
            }
            simulateClickAndHover(arguments[0]);
            """,
                element,
            )
            time.sleep(0.01)  # Short wait for the popup
            return True
        except Exception as e:
            logging.error(f"Error hovering at top-left: {str(e)}")
            return False

    def _hover_bottom_right(self, element):
        try:
            self.driver.execute_script(
                """
                function simulateClickAndHover(element) {
                const rect = element.getBoundingClientRect();
                const events = ['mouseover', 'mousedown', 'mouseup', 'mousemove'];
                events.forEach(eventName => {
                    const event = new MouseEvent(eventName, {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: rect.right,
                        clientY: rect.bottom
                    });
                    element.dispatchEvent(event);
                });
            }
            simulateClickAndHover(arguments[0]);
            """,
                element,
            )
            time.sleep(0.01)  # Short wait for the popup
            # logging.info("Hovered at bottom-right.")
            return True
        except Exception as e:
            logging.error(f"Error hovering at bottom-right: {str(e)}")
            return False

    def _click_and_hover(self, element):
        try:
            self.driver.execute_script(
                """
            function simulateClickAndHover(element) {
                const rect = element.getBoundingClientRect();
                const events = ['mouseover', 'mousedown', 'click', 'mouseup', 'mousemove'];
                events.forEach(eventName => {
                    const event = new MouseEvent(eventName, {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: rect.left + (rect.width / 2),
                        clientY: rect.top + (rect.height / 2)
                    });
                    element.dispatchEvent(event);
                });
            }
            simulateClickAndHover(arguments[0]);
            """,
                element,
            )
            time.sleep(0.001)  # Short wait for the popup
            return self._verify_popup_appears()
        except Exception as e:
            logging.error(f"Error clicking SVG point using JavaScript: {str(e)}")
            return False

    def _verify_popup_appears(self):
        try:
            logging.info("Waiting for popup to appear...")
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[dojoattachpoint="_description"]')
                )
            )
            logging.info("Popup appeared.")
            return True
        except TimeoutException:
            logging.error("Popup did not appear in time.")
            return False

    def _get_all_map_selectors(self):
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "g[id*='layer'] path")
            logging.info(f"Found {len(elements)}  elements in the current view.")
            # filter out elements that are not visible
            elements = [
                element
                for element in elements
                if element.is_displayed() and element.get_attribute("fill") != "none"
            ]
            logging.info(f"Found {len(elements)} visible elements in the current view.")
            return elements
        except NoSuchElementException:
            logging.error("No elements found.")
        return []

    def _get_selector_path(self, element):
        return self.driver.execute_script(
            """
            function getPathTo(element) {
                if (element.id !== '') return '#' + element.id;
                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element) return getPathTo(element.parentNode) + ' > ' + element.tagName + ':nth-child(' + (ix + 1) + ')';
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                }
            }
            return getPathTo(arguments[0]);
        """,
            element,
        )

    def _get_degree_data(self):
        try:
            degree_element = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="widgets_Coordinate_Widget_4"]/div/div[2]/div[2]',
                    )
                )
            )
            degree = degree_element.text.strip()
            if "Move mouse to get coordinates" in degree or degree == "":
                logging.info("Degree data not loaded correctly.")
                return "N/A"
            return degree
        except TimeoutException:
            logging.error("Degree element not found in time.")
            return "N/A"

    def _scrape_popup_data(self, location, selector):
        data = {
            "Location": location,
            "Selector": selector,
            "Degree": self._get_degree_data(),
            "Male Population": "N/A",
            "Female Population": "N/A",
            "Median Age (Male)": "N/A",
            "Median Age (Female)": "N/A",
            "Total Population": "N/A",
            "Population Density": "N/A",
        }

        if not self._verify_popup_appears():
            logging.warning("Popup not available for data scraping.")
            data["Status"] = "Popup not available"
            return data

        try:
            popup = self.driver.find_element(
                By.CSS_SELECTOR, 'div[dojoattachpoint="_description"]'
            )
            html_content = popup.get_attribute("innerHTML")
            soup = BeautifulSoup(html_content, "html.parser")

            # zoom level
            # Assuming you have the element
            zoom_element = self.driver.find_element(By.CSS_SELECTOR, "#map")
            zoom_level = zoom_element.get_attribute("data-zoom")
            data["Zoom Level"] = zoom_level
            logging.info(f"Zoom Level: {zoom_level}")
            # Total Population
            total_pop = soup.find("span", class_="esriNumericValue")
            data["Total Population"] = (
                total_pop.get_text(strip=True) if total_pop else "N/A"
            )

            # Male and Female Population
            male_pop = soup.find("li", string=lambda t: "Male Population:" in str(t))
            female_pop = soup.find(
                "li", string=lambda t: "Female Population:" in str(t)
            )

            data["Male Population"] = (
                male_pop.find("span")
                .get_text(strip=True)
                .replace("Male Population: ", "")
                if male_pop
                else "N/A"
            )
            data["Female Population"] = (
                female_pop.find("span")
                .get_text(strip=True)
                .replace("Female Population: ", "")
                if female_pop
                else "N/A"
            )

            # Median Age
            median_age_male = soup.find(
                "li", string=lambda t: "Median Age (Male):" in str(t)
            )
            median_age_female = soup.find(
                "li", string=lambda t: "Median Age (Female):" in str(t)
            )

            data["Median Age (Male)"] = (
                median_age_male.get_text(strip=True)
                .replace("Median Age (Male):", "")
                .strip()
                if median_age_male
                else "N/A"
            )
            data["Median Age (Female)"] = (
                median_age_female.get_text(strip=True)
                .replace("Median Age (Female):", "")
                .strip()
                if median_age_female
                else "N/A"
            )

            # Population Density
            try:
                population_density_element = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[3]/span",
                )
                data["Population Density"] = population_density_element.text.strip()
            except NoSuchElementException:
                logging.error("Population Density element not found.")
                data["Population Density"] = "N/A"

            return data
        except Exception as e:
            logging.error(f"Error scraping data from the popup: {str(e)}")
            return {}

    def _write_to_csv(self, data, filename="population_v1.csv"):
        try:
            filepath = os.path.join(MODULE_DIR, filename)
            with open(filepath, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)
        except Exception as e:
            logging.error(f"Error writing to CSV: {str(e)}")

    def _hide_unwanted_divs(self):
        """Hide any unwanted UI elements that might block interaction."""
        script = """
            document.querySelectorAll("[id^='dijit__WidgetBase']").forEach(el => el.style.setProperty('display', 'none', 'important'));
            document.querySelectorAll('.searchBtn, .searchInputGroup, .searchMenu').forEach(el => el.style.setProperty('display', 'none', 'important'));
            var xpaths = [
                "//*[@id='widgets_ZoomSlider_Widget_15']/div[2]",
                "//*[@id='widgets_ExtentNavigate_Widget_16']/div[1]",
                "//*[@id='widgets_ExtentNavigate_Widget_16']/div[2]",
                "//*[@id='esri_dijit_HomeButton_0']/div/div",
                "//*[@id='widgets_MyLocation_Widget_12']/div",
                "//*[@id='widgets_FullScreen_Widget_17']/div"
            ];
            xpaths.forEach(function(xpath) {
                var elements = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                for (var i = 0; i < elements.snapshotLength; i++) {
                    elements.snapshotItem(i).style.setProperty('display', 'none', 'important');
                }
            });
        """
        self.driver.execute_script(script)
        logging.info("Hide unwanted divs.")
        time.sleep(5)

    def _zoom_in_on_map(self):
        try:
            zoom_in_button = self.driver.find_element(By.CSS_SELECTOR, ".zoom.zoom-in")
            self.driver.execute_script("arguments[0].click();", zoom_in_button)
            time.sleep(0.5)
            logging.info(f"Zoomed in.")
        except (NoSuchElementException, TimeoutException, Exception) as e:
            logging.error(f"Error zooming in on map: {str(e)}")

    def _click_and_wait_for_popup(self, element):
        retries = 1
        for _ in range(retries):
            if self._click_and_hover(element):
                if self._verify_popup_appears():
                    return True
            time.sleep(0.001)
        logging.info("Popup did not appear after attempts.")
        return False

    def _pan_map(self, x_offset, y_offset):
        """Pan the map by x and y offset pixels."""
        map_element = self.driver.find_element(By.ID, "map_root")

        self.actions.move_to_element(map_element)
        self.actions.click_and_hold()
        self.actions.move_by_offset(x_offset, y_offset)
        self.actions.release().perform()
        time.sleep(0.001)  # Allow map to adjust

    def _get_map_center_coordinates(self):
        """Get the center coordinates of the map."""
        map_element = self.driver.find_element(By.ID, "map_root")
        rect = map_element.rect
        center_x = rect["width"] / 2
        center_y = rect["height"] / 2
        return center_x, center_y

    def _pan_and_center_map(self, element):
        """Pan the map to center on a specific SVG element."""
        try:
            rect = self.driver.execute_script(
                "return arguments[0].getBoundingClientRect();", element
            )

            map_center_x, map_center_y = self._get_map_center_coordinates()
            element_center_x = rect["left"] + rect["width"] / 2
            element_center_y = rect["top"] + rect["height"] / 2
            x_offset = element_center_x - map_center_x
            y_offset = element_center_y - map_center_y

            # Correctly call pan_map with two arguments: x and y offsets
            self._pan_map(-x_offset, -y_offset)
        except Exception as e:
            logging.error(f"Error centering map on element: {str(e)}")

    def _systematic_map_navigation(self, location):
        processed_selectors = set()
        total_boxes_found = 1
        top_left_degree = "N/A"
        bottom_right_degree = "N/A"
        elements = self._get_all_map_selectors()

        for element in elements:
            try:
                selector_path = self._get_selector_path(element)
                if selector_path and selector_path not in processed_selectors:
                    # self._pan_and_center_map(element)
                    if self._hover_top_left(element):
                        top_left_degree = self._get_degree_data()
                    if self._hover_bottom_right(element):
                        bottom_right_degree = self._get_degree_data()
                    if self._click_and_wait_for_popup(element):
                        degree = self._get_degree_data()
                        data = self._scrape_popup_data(location, selector_path)
                        data["Degree"] = degree
                        data["Top Left Degree"] = top_left_degree
                        data["Bottom Right Degree"] = bottom_right_degree
                        data["id"] = total_boxes_found
                        # logging.info(f"Data scraped: {data}")
                        self._write_to_csv(data)
                        processed_selectors.add(selector_path)
                        total_boxes_found += 1
                        logging.info(f"Total Points Processed: {total_boxes_found}")
            except (
                StaleElementReferenceException,
                TimeoutException,
                NoSuchElementException,
                Exception,
            ) as e:
                logging.error("skipping point.")
                continue
        return total_boxes_found

    def close(self):
        """
        Close the browser driver
        """
        self.driver.quit()


class ParentFinder:
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = None
        self.result_df = None

    def parse_degrees(self, degree_str):

        try:
            parts = degree_str.replace(" Degrees", "").split()
            return float(parts[0]), float(parts[1])
        except:
            return None, None

    def is_point_in_box(self, point, top_left, bottom_right):

        if point is None or top_left is None or bottom_right is None:
            return False

        lon, lat = point
        top_left_lon, top_left_lat = top_left
        bottom_right_lon, bottom_right_lat = bottom_right

        return min(top_left_lon, bottom_right_lon) <= lon <= max(
            top_left_lon, bottom_right_lon
        ) and min(top_left_lat, bottom_right_lat) <= lat <= max(
            top_left_lat, bottom_right_lat
        )

    def load_data(self):
        """
        Load data from CSV file
        """
        try:
            self.df = pd.read_csv(
                self.input_file,
                names=[
                    "Location",
                    "Selector",
                    "Degree",
                    "MalePopulation",
                    "FemalePopulation",
                    "MedianAgeMale",
                    "MedianAgeFemale",
                    "TotalPopulation",
                    "PopulationDensity",
                    "ZoomLevel",
                    "TopLeftDegree",
                    "BottomRightDegree",
                    "ID",
                ],
                header=0,
            )

            # Refactor ID column to include Location-ZoomLevel-Id
            self.df["ID"] = (
                self.df["Location"].astype(str)
                + "-"
                + self.df["ID"].astype(str)
                + "-"
                + self.df["ZoomLevel"].astype(str)
            )
            self.df.drop_duplicates(subset=["ID"], inplace=True)
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def find_parents(self):
        """
        Find parent rows based on zoom levels and degree containment

        :return: DataFrame with parent information
        """
        if self.df is None:
            self.load_data()

        # Sort dataframe by zoom level in descending order
        df_sorted = self.df.sort_values("ZoomLevel", ascending=False).copy()

        # Initialize parent column
        df_sorted["Parent"] = np.nan

        for i, row in df_sorted.iterrows():
            current_point = self.parse_degrees(row["Degree"])
            current_zoom = row["ZoomLevel"]

            # Find potential parent rows (lower zoom levels)
            potential_parents = df_sorted[
                (df_sorted["ZoomLevel"] < current_zoom) & df_sorted["Parent"].isnull()
            ]

            # Find the parent that contains the current point
            for _, parent_row in potential_parents.iterrows():
                top_left = self.parse_degrees(parent_row["TopLeftDegree"])
                bottom_right = self.parse_degrees(parent_row["BottomRightDegree"])

                if self.is_point_in_box(current_point, top_left, bottom_right):
                    df_sorted.at[i, "Parent"] = parent_row.ID
                    break

        self.result_df = df_sorted
        return self.result_df

    def save_results(self, output_file='population.csv'):
        """
        Save results to a CSV file
        
        :param output_file: Path to save the output CSV
        """
        if self.result_df is None:
            self.find_parents()
        
        try:
            output_path = os.path.join(MODULE_DIR, output_file)
            self.result_df.to_csv(output_path, index=False)
            logging.info(f"Results saved to {output_path}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")

    def run(self, output_file="population.csv"):
        self.load_data()
        self.find_parents()
        self.save_results(output_file)
        return self.result_df


def main():
    url = "https://maps.saudicensus.sa/arcportal/apps/experiencebuilder/experience/?id=f80f2d4e40e149718461492befc96bf9&page=Population"
    locations = [
        "Jeddah",
        "Al-Riyadh",
        "Makkah",
        # "Al-Madinah", "Al-Qaseem",
        # "Eastern Region", "Aseer", "Tabouk", "Najran",
        # "Al-Baha", "Jazan", "Al-Jouf", "Hail",
        # "Al-Ahsa", "Al-Qatif", "Al-Jubail"
    ]
    try:
        # remove file before starting
        temp_file_path = os.path.join(MODULE_DIR, 'population_v1.csv')
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    except Exception as e:
        logging.error(f"Error removing file: {e}")
        logging.warning("Please remove population_v1.csv manually before running the script.")
        exit(1)
    scraper = Map(url=url, locations=locations)
    try:
        scraper.navigate_and_extract()
    except Exception as e:
        logging.error(f"Scraping failed: {e}")

    finally:
        scraper.close()

    try:
        # Find parent rows
        logging.info("post scraping process started.")
        parent_finder = ParentFinder("population_v1.csv")
        parent_finder.run()
    except Exception as e:
        logging.error(f"Parent finding failed: {e}")
    finally:
        logging.info("Process completed.")
        temp_file_path = os.path.join(MODULE_DIR, 'population_v1.csv')
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        logging.shutdown()
        

if __name__ == "__main__":
    main()
