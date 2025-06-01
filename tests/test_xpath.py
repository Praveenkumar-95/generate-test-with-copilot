import pytest
from playwright.sync_api import expect, Page
from xpath import XPathHealer

@pytest.mark.browser
def test_xpath_healing_with_real_page(page: Page):
    """Test XPath healing with a real webpage."""
    
    # Original DOM with search button
    base_html = """
    <div class="container">
        <button id="search-btn" class="search-button">
            <svg class="search-icon"></svg>
            Search
        </button>
    </div>
    """

    # Changed DOM where ID is removed but class remains
    changed_html = """
    <div class="new-container">
        <button class="search-button modified">
            <svg class="search-icon"></svg>
            Search
        </button>
    </div>
    """

    # Initialize XPath healer
    url = "https://debs-obrien.github.io/playwright-movies-app"
    original_xpath = "//button[@id='search-btn']"
    healer = XPathHealer(base_html, original_xpath, url)
    
    # Get healed XPath
    new_xpath = healer.heal_xpath(changed_html)
    
    # Verify the new XPath works on the actual page
    page.goto(url)
    element = page.locator(f"xpath={new_xpath}")
    
    # Element should exist and be visible
    expect(element).to_be_visible()
    
    # Should be the search button
    expect(element).to_contain_text("Search")
    
    # Should be clickable
    element.click()
    
    # After clicking, search input should be visible
    search_input = page.get_by_role("textbox", name="Search Input")
    expect(search_input).to_be_visible()
