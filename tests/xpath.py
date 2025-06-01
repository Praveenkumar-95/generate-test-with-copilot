"""
XPath Healing Logic:
1. Stores original DOM & XPath with element location
2. Generates alternatives based on:
   - ID, role, class, text content, href, src
   - Position and parent relationships
3. Verifies on live webpage with 70% similarity threshold
"""

from playwright.sync_api import sync_playwright
from lxml import etree
from typing import Optional, List, Dict, Tuple
import difflib

class XPathHealer:
    def __init__(self, base_html: str, original_xpath: str, url: str):
        self.base_dom = etree.HTML(base_html)
        self.original_xpath = original_xpath
        self.url = url
        self.original_element = self.base_dom.xpath(original_xpath)[0] if self.base_dom.xpath(original_xpath) else None
        self.original_location = None
        if self.original_element is not None:
            is_valid, element_info = self.verify_xpath_on_page(original_xpath)
            if is_valid:
                self.original_location = element_info.get('position')
        
    def verify_xpath_on_page(self, xpath: str) -> Tuple[bool, Dict]:
        """Verify XPath on actual web page using Playwright."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Set headless=True in production
            page = browser.new_page()
            try:
                page.goto(self.url)
                # Wait for element to be visible
                element = page.wait_for_selector(f"xpath={xpath}", timeout=5000)
                if element:
                    # Get element properties
                    bbox = element.bounding_box()
                    is_visible = element.is_visible()
                    element_info = {
                        'visible': is_visible,
                        'position': bbox,
                        'text': element.text_content(),
                        'tag': element.evaluate('el => el.tagName.toLowerCase()')
                    }
                    browser.close()
                    return True, element_info
            except Exception as e:
                browser.close()
                return False, {'error': str(e)}
            
    def heal_xpath(self, new_html: str) -> str:
        """Find and verify working XPath in the new DOM structure."""
        if not self.original_element:
            return self.original_xpath

        new_dom = etree.HTML(new_html)
        original_attrs = self.get_element_attributes(self.original_element)
        alternate_xpaths = self.generate_alternate_xpaths(self.original_element)
        
        for xpath in alternate_xpaths:
            try:
                # First verify in DOM
                found_elements = new_dom.xpath(xpath)
                if found_elements:
                    found_attrs = self.get_element_attributes(found_elements[0])
                    similarity = difflib.SequenceMatcher(None, 
                                                       str(original_attrs),
                                                       str(found_attrs)).ratio()
                    
                    if similarity > 0.7:
                        # Then verify on actual page
                        is_valid, element_info = self.verify_xpath_on_page(xpath)
                        if is_valid and element_info.get('visible', False):
                            print(f"Found valid xpath: {xpath}")
                            print(f"Element info: {element_info}")
                            return xpath
            except Exception as e:
                print(f"Error checking xpath {xpath}: {str(e)}")
                continue

        return self.original_xpath

# Example usage
if __name__ == "__main__":
    base_html = """
    <html>
        <body>
            <div class="container">
                <button id="search-btn" class="search-button">
                    <svg class="search-icon"></svg>
                    Search
                </button>
            </div>
        </body>
    </html>
    """

    changed_html = """
    <html>
        <body>
            <div class="new-container">
                <button class="search-button modified">
                    <svg class="search-icon"></svg>
                    Search
                </button>
            </div>
        </body>
    </html>
    """    
    url = "https://debs-obrien.github.io/playwright-movies-app"
    original_xpath = "//button[@id='search-btn']"
    
    healer = XPathHealer(base_html, original_xpath, url)
    new_xpath = healer.heal_xpath(changed_html)
    print(f"Original XPath: {original_xpath}")
    print(f"Healed XPath: {new_xpath}")