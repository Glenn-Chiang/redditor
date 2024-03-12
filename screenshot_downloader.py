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

# Handle nsfw

def screenshot_comment(subreddit: str, post_id: str, comment_id: str, output_path: str):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        # Change user-agent to avoid being detected as a bot
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(
            url=f'https://www.reddit.com/r/{subreddit}/comments/{post_id}/comment/{comment_id}')
        
        comment_element = page.locator(f"shreddit-comment[thingid='{comment_id}']")
        # Button that toggles whether to expand or close the comment subtree
        toggle_button = comment_element.get_by_label('Toggle Comment Thread').first
        # If expanded, click on toggle button to collapse the subtree
        if toggle_button.get_attribute('aria-expanded'):
            toggle_button.click()
        
        comment_element.screenshot(path=output_path)
        browser.close()

if __name__ == '__main__':
    screenshot_comment(subreddit='AskReddit', post_id='t3_1b8sfer', comment_id='t1_ktr4wrw', output_path='output/test.png')