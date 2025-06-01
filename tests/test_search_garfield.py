from playwright.sync_api import expect, Page

def test_search_garfield(page: Page):
    # 1. Navigate to the movies app
    page.goto('https://debs-obrien.github.io/playwright-movies-app')
    
    # 2. Search for 'Garfield'
    search_button = page.get_by_role('search')
    search_button.click()
    
    search_input = page.get_by_role('textbox', name='Search Input')
    search_input.fill('Garfield')
    search_input.press('Enter')
    
    # 3. Verify the movie is in the list
    movie_title = page.get_by_role('heading', name='The Garfield Movie', level=2)
    expect(movie_title).to_be_visible()
