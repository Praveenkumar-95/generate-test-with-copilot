from typing import Dict

def pytest_configure(config):
    config.option.markexpr = 'not slow'

def pytest_generate_tests(metafunc):
    # This is called for every test function
    if "browser_name" in metafunc.fixturenames:
        metafunc.parametrize("browser_name", ["chromium", "firefox", "webkit"])

def pytest_playwright_configure(config: Dict):
    config["browser_configs"] = [
        {"name": "chromium", "use": {"headless": True}},
        {"name": "firefox", "use": {"headless": True}},
        {"name": "webkit", "use": {"headless": True}},
    ]
    
    config["use"] = {
        "trace": "on-first-retry",
        "screenshot": "only-on-failure",
    }
