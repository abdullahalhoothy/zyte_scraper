# step2_traffic_analysis.py
"""
Standalone Google Maps Traffic Analysis Module
Modified: Remote webdriver support, optional proxy, ensures screenshot copy to static folder.
"""

import logging
import math
import os
import shutil
import time
from collections import Counter
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GoogleMapsTrafficAnalyzer:
    """Standalone Google Maps traffic analyzer using screenshots and color detection"""

    TRAFFIC_COLORS = {
        "dark_red": [(140, 0, 0), (200, 70, 70)],
        "red": [(220, 50, 40), (255, 110, 90)],
        "yellow": [(230, 170, 40), (255, 230, 100)],
        "green": [(0, 180, 120), (60, 255, 190)],
        "gray": [(160, 170, 180), (200, 210, 220)],
    }

    TRAFFIC_SCORES = {"dark_red": 100, "red": 100, "yellow": 70, "green": 30, "gray": 0}

    def __init__(
        self,
        cleanup_driver: bool = True,
        selenium_url: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """
        Args:
            cleanup_driver: close webdriver at end
            selenium_url: http://host:4444/wd/hub (defaults to SELENIUM_URL env or http://selenium:4444/wd/hub)
            proxy: optional proxy host:port
        """
        self.driver = None
        self.cleanup_driver = cleanup_driver
        self.selenium_url = selenium_url or os.getenv(
            "SELENIUM_URL", "http://localhost:4444/wd/hub"
        )
        self.proxy = proxy or os.getenv("SELENIUM_PROXY", None)

        self.DIRECTION_ANGLES = {
            "north": 0,
            "n": 0,
            "northeast": 45,
            "ne": 45,
            "east": 90,
            "e": 90,
            "southeast": 135,
            "se": 135,
            "south": 180,
            "s": 180,
            "southwest": 225,
            "sw": 225,
            "west": 270,
            "w": 270,
            "northwest": 315,
            "nw": 315,
        }

        self.DAY_MAP = {
            "sunday": 0,
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
        }
        self.TIME_MAP = {"8:30AM": 28, "6:00PM": 135, "10:00PM": 180}

    def setup_webdriver(self) -> Optional[webdriver.Remote]:
        """Setup Selenium Remote Chrome webdriver (containerized selenium)"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1200,800")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")

        # optional proxy
        if self.proxy:
            # logger.info(f"Using proxy: {self.proxy}")
            # proxy = "http://username:password@host:port"
            # chrome_options.add_argument(f"--proxy-server={proxy}")
            ...

        try:
            self.driver = webdriver.Remote(
                command_executor=self.selenium_url,
                options=chrome_options,
            )
            return self.driver
        except Exception as e:
            logger.error(
                f"Could not connect to remote webdriver at {self.selenium_url}: {e}"
            )
            return None

    def cleanup_webdriver(self):
        if self.driver:
            try:
                self.driver.quit()
                time.sleep(0.5)
                self.driver = None
            except Exception as e:
                logger.error(f"Error closing webdriver: {e}")
                self.driver = None

    def get_google_maps_url(self, lat: float, lng: float, zoom: int = 18) -> str:
        base_url = "https://www.google.com/maps"
        params = f"@{lat},{lng},{zoom}z/data=!5m1!1e1"
        return f"{base_url}/{params}?hl=en&gl=us"

    def capture_google_maps_screenshot(
        self,
        lat: float,
        lng: float,
        filename: str = "traffic_screenshot",
        save_to_static: bool = False,
        day_of_week: Optional[Union[str, int]] = None,
        target_time: Optional[str] = None,
    ) -> Tuple[Optional[str], bool]:
        """Capture screenshot and return (path, live_traffic)"""
        live_traffic = True
        if not self.driver:
            logger.error("Webdriver not initialized")
            return None, live_traffic

        try:
            maps_url = self.get_google_maps_url(lat, lng, zoom=18)
            logger.info(f"Loading Google Maps URL: {maps_url}")
            self.driver.get(maps_url)
            time.sleep(5)

            # Try to accept cookies
            try:
                accept_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(., 'Accept') or contains(., 'I agree')]",
                        )
                    )
                )
                accept_button.click()
                time.sleep(2)
            except Exception:
                pass

            time.sleep(3)
            self.driver.execute_script(
                "window.dispatchEvent(new WheelEvent('wheel', {deltaY: -100, bubbles: true}));"
            )
            time.sleep(2)
            self.driver.execute_script(
                "window.dispatchEvent(new WheelEvent('wheel', {deltaY: 100, bubbles: true}));"
            )
            time.sleep(1)
            self.driver.execute_script(
                "window.dispatchEvent(new WheelEvent('wheel', {deltaY: 100, bubbles: true}));"
            )
            time.sleep(2)

            # try to switch to typical traffic mode if requested
            try:
                traffic_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="layer"]/div/div/span/button')
                    )
                )
                traffic_button.click()
                time.sleep(0.3)
                self.driver.find_element(
                    By.XPATH, '//*[@id="action-menu"]/div/div[2]'
                ).click()
                time.sleep(1)
                if day_of_week is not None:
                    days = self.driver.find_element(
                        By.XPATH, '//*[@id="layer"]/div/div/div/div[1]'
                    ).find_elements(By.TAG_NAME, "button")
                    if isinstance(day_of_week, int) and 0 <= day_of_week <= 6:
                        days[day_of_week].click()
                    else:
                        days[
                            self.DAY_MAP.get(str(day_of_week).strip().lower(), 0)
                        ].click()
                    time.sleep(1)
                if target_time is not None:
                    try:
                        pos = self.TIME_MAP.get(
                            target_time.upper().strip().replace(" ", ""), 0
                        )
                        actions = ActionChains(self.driver)
                        slider = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    '//*[@id="layer"]/div/div/div/div[2]/div/div[1]/span[2]',
                                )
                            )
                        )
                        actions.click_and_hold(slider).move_by_offset(
                            -35, 0
                        ).release().perform()
                        time.sleep(0.2)
                        actions.click_and_hold(slider).move_by_offset(
                            pos, 0
                        ).release().perform()
                        time.sleep(1)
                    except Exception:
                        logger.info("Failed to adjust the traffic time slider.")
                live_traffic = False
            except Exception:
                live_traffic = True

            current_dir = os.path.dirname(os.path.abspath(__file__))
            screenshots_dir = os.path.join(current_dir, "traffic_screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            safe_target_time = (
                str(target_time).replace(":", "-").replace(" ", "_")
                if target_time
                else "no_time"
            )
            safe_day_of_week = (
                str(day_of_week).replace(" ", "_")
                if day_of_week is not None
                else "no_day"
            )
            screenshot_filename = (
                f"traffic_{lat}_{lng}_{safe_day_of_week}_{safe_target_time}.png"
            )
            screenshot_path = os.path.join(screenshots_dir, screenshot_filename)

            screenshot_success = False
            for attempt in range(3):
                try:
                    self.driver.save_screenshot(screenshot_path)
                    screenshot_success = True
                    break
                except Exception as screenshot_error:
                    logger.warning(
                        f"Screenshot attempt {attempt + 1} failed: {screenshot_error}"
                    )
                    if attempt < 2:
                        time.sleep(1)

            if not screenshot_success:
                raise Exception("Failed to capture screenshot after 3 attempts")

            logger.info(f"Screenshot captured: {screenshot_path}")
            return screenshot_path, live_traffic

        except Exception as e:
            logger.error(f"Failed to capture Google Maps screenshot: {e}")
            return None, live_traffic

    def classify_traffic_color(self, rgb: Tuple[int, int, int]) -> str:
        for traffic_type, (min_rgb, max_rgb) in self.TRAFFIC_COLORS.items():
            if all(
                min_val <= rgb[i] <= max_val
                for i, (min_val, max_val) in enumerate(zip(min_rgb, max_rgb))
            ):
                return traffic_type
        return "gray"

    def add_pin_to_image(
        self, image_path: str, storefront_direction: str = "north"
    ) -> str:
        try:
            time.sleep(0.2)
            image = Image.open(image_path)
            width, height = image.size
            center_x, center_y = width // 2, height // 2
            self._add_directional_arrow(image, center_x, center_y, storefront_direction)
            pinned_path = image_path.replace(".png", "_pinned.png")
            image_copy = image.copy()
            image.close()
            image_copy.save(pinned_path)
            image_copy.close()
            time.sleep(0.5)
            logger.info(f"Pin and directional cone added: {pinned_path}")
            return pinned_path
        except Exception as e:
            logger.error(f"Failed to add pin to image: {e}")
            return image_path

    def _add_directional_arrow(
        self, image: Image.Image, center_x: int, center_y: int, direction: str
    ):
        from PIL import ImageDraw

        draw = ImageDraw.Draw(image)
        pin_head_size = 8
        draw.ellipse(
            [
                center_x - pin_head_size,
                center_y - pin_head_size,
                center_x + pin_head_size,
                center_y + pin_head_size,
            ],
            fill="purple",
            outline="black",
            width=1,
        )
        direction_angle = self.DIRECTION_ANGLES.get(direction.lower(), 0)
        cone_length = 52
        cone_width_degrees = 25
        angle2 = math.radians(direction_angle - cone_width_degrees)
        p2 = (
            center_x + cone_length * math.sin(angle2),
            center_y - cone_length * math.cos(angle2),
        )
        angle3 = math.radians(direction_angle + cone_width_degrees)
        p3 = (
            center_x + cone_length * math.sin(angle3),
            center_y - cone_length * math.cos(angle3),
        )
        draw.polygon([(center_x, center_y), p2, p3], fill="hotpink", outline="black")
        logger.info(f"Directional cone added pointing {direction}")

    def _analyze_annular_zone(
        self,
        image_array: np.ndarray,
        center_x: int,
        center_y: int,
        height: int,
        width: int,
        inner_radius: int,
        outer_radius: int,
        zone_name: str,
        traffic_analysis: Dict[str, Any],
        excluded_pixels: Optional[set[Tuple[int, int]]] = None,
    ):
        if excluded_pixels is None:
            excluded_pixels = set()
        zone_colors = []
        pixels_in_zone = 0
        for y in range(
            max(0, center_y - outer_radius), min(height, center_y + outer_radius + 1)
        ):
            for x in range(
                max(0, center_x - outer_radius), min(width, center_x + outer_radius + 1)
            ):
                distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                if (
                    inner_radius < distance <= outer_radius
                    and (x, y) not in excluded_pixels
                ):
                    rgb = tuple(image_array[y, x][:3])
                    color_type = self.classify_traffic_color(rgb)
                    zone_colors.append(color_type)
                    pixels_in_zone += 1
        non_gray_colors = [c for c in zone_colors if c != "gray"]
        if non_gray_colors:
            color_counts = Counter(non_gray_colors)
            zone_score = sum(
                count * self.TRAFFIC_SCORES[color]
                for color, count in color_counts.items()
            ) / len(non_gray_colors)
        else:
            zone_score = 0
        traffic_analysis["area_scores"][zone_name] = {
            "score": zone_score,
            "pixels": pixels_in_zone,
            "colors": dict(Counter(zone_colors)),
        }
        for color, count in Counter(zone_colors).items():
            traffic_analysis["color_distribution"][color] += count
        logger.info(
            f"Analyzed {zone_name} zone: Score={zone_score}, Pixels={pixels_in_zone}"
        )

    def find_storefront_traffic(
        self,
        image_array: np.ndarray,
        center_x: int,
        center_y: int,
        storefront_direction: str,
        max_distance: int = 50,
    ) -> Tuple[Dict[str, Any], set]:
        height, width = image_array.shape[:2]
        checked_cone_pixels = set()
        direction_angle = self.DIRECTION_ANGLES.get(storefront_direction.lower(), 0)
        min_angle = (direction_angle - 30 + 360) % 360
        max_angle = (direction_angle + 30) % 360
        angle_range = []
        if min_angle < max_angle:
            angle_range = range(min_angle, max_angle + 1, 5)
        else:
            angle_range = list(range(min_angle, 360, 5)) + list(
                range(0, max_angle + 1, 5)
            )
        for distance in range(1, max_distance + 1):
            for angle in angle_range:
                angle_rad = math.radians(angle)
                x = int(center_x + distance * math.sin(angle_rad))
                y = int(center_y - distance * math.cos(angle_rad))
                if 0 <= x < width and 0 <= y < height:
                    checked_cone_pixels.add((x, y))
                    rgb = tuple(image_array[y, x][:3])
                    color_type = self.classify_traffic_color(rgb)
                    if color_type != "gray":
                        logger.info(
                            f"Storefront traffic found: {color_type} at distance {distance}px"
                        )
                        return {
                            "found": True,
                            "color": color_type,
                            "distance": distance,
                            "score": self.TRAFFIC_SCORES[color_type],
                        }, checked_cone_pixels
        return {
            "found": False,
            "color": "gray",
            "distance": max_distance,
            "score": 0,
        }, checked_cone_pixels

    def analyze_traffic_in_image(
        self,
        image_path: str,
        center_lat: float,
        center_lng: float,
        storefront_direction: str = "north",
    ) -> Dict[str, Any]:
        try:
            image = Image.open(image_path)
            image_array = np.array(image)
            height, width = image_array.shape[:2]
            center_x, center_y = width // 2, height // 2
            pixels_per_meter = 1.5
            storefront_cone_radius_px = int(50 * pixels_per_meter)
            full_50m_circle_radius_px = int(50 * pixels_per_meter)
            outer_100m_zone_radius_px = int(100 * pixels_per_meter)
            outer_150m_zone_radius_px = int(150 * pixels_per_meter)
            traffic_analysis = {
                "storefront_score": 0,
                "area_scores": {},
                "total_pixels_analyzed": 0,
                "color_distribution": {
                    color: 0 for color in self.TRAFFIC_COLORS.keys()
                },
                "storefront_details": {},
            }
            storefront_result, cone_pixels_checked = self.find_storefront_traffic(
                image_array,
                center_x,
                center_y,
                storefront_direction,
                storefront_cone_radius_px,
            )
            traffic_analysis["storefront_details"] = storefront_result
            traffic_analysis["storefront_score"] = storefront_result["score"]
            if storefront_result["found"]:
                traffic_analysis["color_distribution"][storefront_result["color"]] += 1
            zone_colors_50m_full_circle = []
            pixels_in_zone_50m_full_circle = 0
            for y in range(
                max(0, center_y - full_50m_circle_radius_px),
                min(height, center_y + full_50m_circle_radius_px + 1),
            ):
                for x in range(
                    max(0, center_x - full_50m_circle_radius_px),
                    min(width, center_x + full_50m_circle_radius_px + 1),
                ):
                    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                    if (
                        distance <= full_50m_circle_radius_px
                        and (x, y) not in cone_pixels_checked
                    ):
                        rgb = tuple(image_array[y, x][:3])
                        color_type = self.classify_traffic_color(rgb)
                        zone_colors_50m_full_circle.append(color_type)
                        pixels_in_zone_50m_full_circle += 1
            non_gray_colors_50m_full_circle = [
                c for c in zone_colors_50m_full_circle if c != "gray"
            ]
            if non_gray_colors_50m_full_circle:
                color_counts_50m_full_circle = Counter(non_gray_colors_50m_full_circle)
                zone_score_50m_full_circle = sum(
                    count * self.TRAFFIC_SCORES[color]
                    for color, count in color_counts_50m_full_circle.items()
                ) / len(non_gray_colors_50m_full_circle)
            else:
                zone_score_50m_full_circle = 0
            traffic_analysis["area_scores"]["50m"] = {
                "score": zone_score_50m_full_circle,
                "pixels": pixels_in_zone_50m_full_circle,
                "colors": dict(Counter(zone_colors_50m_full_circle)),
            }
            for color, count in Counter(zone_colors_50m_full_circle).items():
                traffic_analysis["color_distribution"][color] += count
            logger.info(
                f"Analyzed 50m full circle: Score={zone_score_50m_full_circle}, Pixels={pixels_in_zone_50m_full_circle}"
            )
            self._analyze_annular_zone(
                image_array,
                center_x,
                center_y,
                height,
                width,
                full_50m_circle_radius_px,
                outer_100m_zone_radius_px,
                "100m",
                traffic_analysis,
            )
            self._analyze_annular_zone(
                image_array,
                center_x,
                center_y,
                height,
                width,
                outer_100m_zone_radius_px,
                outer_150m_zone_radius_px,
                "150m",
                traffic_analysis,
            )
            traffic_analysis["total_pixels_analyzed"] = sum(
                traffic_analysis["color_distribution"].values()
            )
            return traffic_analysis
        except Exception as e:
            logger.error(f"Failed to analyze traffic in image: {e}")
            return {}

    def calculate_final_traffic_score(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        if not analysis:
            return {"score": 0, "details": "Analysis failed"}
        storefront_score = analysis.get("storefront_score", 0)
        storefront_weight = 0.1
        area_weight = 0.9
        area_score = 0
        total_weighted_pixels = 0
        area_scores = analysis.get("area_scores", {})
        multipliers = {"50m": 1.0, "100m": 0.5, "150m": 0.25}
        for zone, multiplier in multipliers.items():
            if zone in area_scores:
                zone_data = area_scores[zone]
                zone_score = zone_data.get("score", 0)
                zone_pixels = zone_data.get("pixels", 0)
                weighted_contribution = zone_score * multiplier * zone_pixels
                area_score += weighted_contribution
                total_weighted_pixels += zone_pixels * multiplier
        if total_weighted_pixels > 0:
            area_score = area_score / total_weighted_pixels
        else:
            area_score = 0
        final_score = (storefront_score * storefront_weight) + (
            area_score * area_weight
        )
        return {
            "score": round(final_score, 2),
            "storefront_score": storefront_score,
            "area_score": round(area_score, 2),
            "storefront_weight": storefront_weight,
            "area_weight": area_weight,
            "total_pixels_analyzed": analysis.get("total_pixels_analyzed", 0),
            "color_distribution": analysis.get("color_distribution", {}),
            "area_details": analysis.get("area_scores", {}),
        }

    def analyze_location_traffic(
        self,
        lat: float,
        lng: float,
        save_to_static: bool = False,
        storefront_direction: str = "north",
        day_of_week: Optional[Union[str, int]] = None,
        target_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Main method to analyze traffic using Google Maps screenshots

        It will:
          - setup remote webdriver (if not already),
          - capture screenshot,
          - add pin,
          - if save_to_static=True copy pinned image to ./static/images/traffic_screenshots and set screenshot path,
          - analyze image and calculate final score,
          - cleanup webdriver if cleanup_driver True.
        """
        try:
            if self.cleanup_driver or not self.driver:
                if not self.setup_webdriver():
                    raise Exception("Failed to setup webdriver")

            screenshot_path, live_traffic = self.capture_google_maps_screenshot(
                lat,
                lng,
                save_to_static=save_to_static,
                day_of_week=day_of_week,
                target_time=target_time,
            )
            if not screenshot_path:
                raise Exception("Failed to capture screenshot")

            pinned_screenshot_path = self.add_pin_to_image(
                screenshot_path, storefront_direction
            )

            image_id = None
            static_screenshot_path = None

            if save_to_static:
                static_dir = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "static",
                    "images",
                    "traffic_screenshots",
                )
                # If running inside container, static is mounted; fallback to repo-level static
                if not os.path.isdir(static_dir):
                    static_dir = os.path.join(
                        os.path.abspath(os.path.dirname(__file__)),
                        "images",
                        "traffic_screenshots",
                    )
                os.makedirs(static_dir, exist_ok=True)

                timestamp = int(time.time())
                static_filename = f"traffic_{timestamp}_{lat}_{lng}_pinned.png"
                static_pinned_path = os.path.join(static_dir, static_filename)
                try:
                    time.sleep(1.0)
                    shutil.copy2(pinned_screenshot_path, static_pinned_path)
                    image_id = os.path.splitext(static_filename)[0]
                    static_screenshot_path = static_pinned_path
                    logger.info(f"Pinned image saved to static: {static_pinned_path}")
                except Exception as copy_error:
                    logger.warning(f"Could not copy to static folder: {copy_error}")
                    static_screenshot_path = pinned_screenshot_path

            analysis = self.analyze_traffic_in_image(
                pinned_screenshot_path, lat, lng, storefront_direction
            )
            if not analysis:
                raise Exception("Failed to analyze traffic")

            try:
                if (
                    os.path.exists(screenshot_path)
                    and screenshot_path != pinned_screenshot_path
                ):
                    os.remove(screenshot_path)
                    logger.info(f"Deleted original screenshot: {screenshot_path}")
            except Exception as cleanup_error:
                logger.warning(f"Could not delete original screenshot: {cleanup_error}")

            result = self.calculate_final_traffic_score(analysis)

            # rename pinned file to include integer storefront and area scores if possible
            storefront_score_int = int(result.get("storefront_score", 0))
            area_score_int = int(result.get("area_score", 0))
            try:
                pinned_dir, pinned_base = os.path.split(pinned_screenshot_path)
                pinned_name, pinned_ext = os.path.splitext(pinned_base)
                if live_traffic:
                    target_time_string = (target_time or "no_time").replace(":", "-")
                    pinned_name = pinned_name.replace(
                        f"_{target_time_string}", "_live"
                    ).replace("no_time", "live")
                new_pinned_name = f"{pinned_name}_frontscore={storefront_score_int}_areascore={area_score_int}{pinned_ext}"
                new_pinned_path = os.path.join(pinned_dir, new_pinned_name)
                os.replace(pinned_screenshot_path, new_pinned_path)
                pinned_screenshot_path = new_pinned_path
            except Exception as rename_error:
                logger.warning(f"Could not rename pinned image: {rename_error}")

            result.update(
                {
                    "method": "google_maps_screenshot",
                    "screenshot_path": static_screenshot_path or pinned_screenshot_path,
                    "image_id": image_id,
                    "coordinates": {"lat": lat, "lng": lng},
                    "analysis_timestamp": time.time(),
                    "storefront_details": analysis.get("storefront_details", {}),
                }
            )

            logger.info(f"Completed analysis for {lat}, {lng}: Score {result['score']}")
            return result

        except Exception as e:
            logger.error(f"Traffic analysis failed: {e}")
            return {
                "score": 0,
                "method": "google_maps_screenshot",
                "error": str(e),
                "coordinates": {"lat": lat, "lng": lng},
            }

        finally:
            if self.cleanup_driver:
                self.cleanup_webdriver()

    # Additional helper methods for traffic layer enabling / verification (kept from original)
    def _ensure_traffic_layer_enabled(self):
        try:
            logger.info("Attempting to enable traffic layer...")
            try:
                traffic_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Traffic']")
                    )
                )
                traffic_button.click()
                time.sleep(2)
                return
            except Exception:
                pass
            try:
                traffic_button = self.driver.find_element(
                    By.XPATH, "//button[contains(text(), 'Traffic')]"
                )
                traffic_button.click()
                time.sleep(2)
                return
            except Exception:
                pass
            try:
                layers_button = self.driver.find_element(
                    By.XPATH,
                    "//button[@aria-label='Layers' or @aria-label='Menu' or contains(@class, 'layers')]",
                )
                layers_button.click()
                time.sleep(1)
                traffic_option = self.driver.find_element(
                    By.XPATH,
                    "//div[contains(text(), 'Traffic') or contains(text(), 'traffic')]",
                )
                traffic_option.click()
                time.sleep(2)
                return
            except Exception:
                pass
            try:
                actions = ActionChains(self.driver)
                actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(
                    "t"
                ).key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
                time.sleep(2)
                return
            except Exception:
                pass
            try:
                traffic_script = """
                var buttons = document.querySelectorAll('button, div');
                for (var i = 0; i < buttons.length; i++) {
                    var btn = buttons[i];
                    if (btn.textContent && (btn.textContent.toLowerCase().includes('traffic') ||
                        btn.getAttribute('aria-label') && btn.getAttribute('aria-label').toLowerCase().includes('traffic'))) {
                        btn.click();
                        break;
                    }
                }
                """
                self.driver.execute_script(traffic_script)
                time.sleep(2)
                return
            except Exception:
                pass
            try:
                current_url = self.driver.current_url
                if "layer=t" not in current_url:
                    if "?" in current_url:
                        traffic_url = current_url + "&layer=t"
                    else:
                        traffic_url = current_url + "?layer=t"
                    self.driver.get(traffic_url)
                    time.sleep(3)
                    return
            except Exception:
                pass
            logger.warning("Traffic layer activation strategies exhausted.")
        except Exception as e:
            logger.error(f"Error enabling traffic layer: {e}")

    def _verify_traffic_loaded(self) -> bool:
        try:
            temp_screenshot = "temp_traffic_check.png"
            self.driver.save_screenshot(temp_screenshot)
            image = Image.open(temp_screenshot)
            image_array = np.array(image)
            height, width = image_array.shape[:2]
            center_x, center_y = width // 2, height // 2
            sample_size = 100
            traffic_pixel_count = 0
            total_sampled = 0
            for y in range(
                max(0, center_y - sample_size // 2),
                min(height, center_y + sample_size // 2),
            ):
                for x in range(
                    max(0, center_x - sample_size // 2),
                    min(width, center_x + sample_size // 2),
                ):
                    rgb = tuple(image_array[y, x][:3])
                    color_type = self.classify_traffic_color(rgb)
                    total_sampled += 1
                    if color_type in ["dark_red", "red", "yellow", "green"]:
                        traffic_pixel_count += 1
            try:
                os.remove(temp_screenshot)
            except Exception:
                pass
            traffic_ratio = (
                traffic_pixel_count / total_sampled if total_sampled > 0 else 0
            )
            traffic_loaded = traffic_ratio > 0.01
            logger.info(
                f"Traffic verification: {traffic_pixel_count}/{total_sampled} ({traffic_ratio:.3f}), loaded: {traffic_loaded}"
            )
            return traffic_loaded
        except Exception as e:
            logger.warning(f"Could not verify traffic loading: {e}")
            return False
