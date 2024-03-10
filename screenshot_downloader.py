from playwright.sync_api import sync_playwright

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81'


def screenshot_post(subreddit: str, post_id: str, output_path: str):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        # Change user-agent to avoid being detected as a bot
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(
            url=f'https://www.reddit.com/r/{subreddit}/comments/{post_id}')
        page.locator(f'#{post_id}').screenshot(path=output_path)
        browser.close()


def screenshot_comment(subreddit: str, post_id: str, comment_id: str, output_path: str):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        # Change user-agent to avoid being detected as a bot
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(
            url=f'https://www.reddit.com/r/{subreddit}/comments/{post_id}/comment/{comment_id}')
        page.locator(
            f"shreddit-comment[thingid='{comment_id}']").screenshot(path=output_path)
        browser.close()
