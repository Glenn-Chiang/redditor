from playwright.sync_api import sync_playwright

def get_screenshot(url: str, output_path: str):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url=url)
        page.locator('').screenshot(path=output_path)


if __name__ == '__main__':
    get_screenshot()