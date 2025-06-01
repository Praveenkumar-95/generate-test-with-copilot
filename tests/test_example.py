from playwright.sync_api import expect

def test_homepage_shows_popular_movies(page):
    page.goto('https://debs-obrien.github.io/playwright-movies-app')
    
    expect(page.get_by_role('main')).to_match_snapshot('homepage.snapshot')
