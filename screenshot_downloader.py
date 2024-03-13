import time
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
load_dotenv()

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81'
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')


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

        comment_element = page.locator(
            f"shreddit-comment[thingid='{comment_id}']")
        # Button that toggles whether to expand or close the comment subtree
        toggle_button = comment_element.get_by_label(
            'Toggle Comment Thread').first
        # If expanded, click on toggle button to collapse the subtree
        if toggle_button.get_attribute('aria-expanded'):
            toggle_button.click()

        comment_element.screenshot(path=output_path)
        browser.close()


# Download screenshot of post and comments while launching 1 browser
def screenshot_thread(subreddit: str, post_id: str, comment_ids: list[str], output_dir: str, nsfw: bool = False):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()

        # Change user-agent to avoid being detected as a bot
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(
            url=f'https://www.reddit.com/r/{subreddit}/comments/{post_id}')

        # If post is marked as nsfw, we need to login
        if nsfw:
            page.locator('#login-button').click()
            page.locator('input#login-username').first.fill(REDDIT_USERNAME)
            page.locator('input#login-password').first.fill(REDDIT_PASSWORD)
            page.locator(
                '#login > faceplate-tabpanel > auth-flow-modal:nth-child(1) > div.w-100 > faceplate-tracker > button').click()

        # Screenshot post
        page.locator(f'#{post_id}').click()
        page.locator(f'#{post_id}').screenshot(
            path=os.path.join(output_dir, f'{post_id}.png'))
        print('Downloaded screenshot for post title')

        # Screenshot comments
        for comment_id in comment_ids:
            try:
                comment_element = page.locator(
                    f"shreddit-comment[thingid='{comment_id}']")
                # Button that toggles expansion of comment subtree
                toggle_button = comment_element.get_by_label(
                    'Toggle Comment Thread').first
                
                # If subtree is expanded, click on toggle button to collapse the subtree
                if toggle_button.is_visible() and toggle_button.get_attribute('aria-expanded') == 'true':
                    toggle_button.click()

                comment_element.screenshot(
                    path=os.path.join(output_dir, f'{comment_id}.png'))
                print(f'Downloaded screenshot for comment {comment_id}')

            except Exception as error:
                print(
                    f"Error downloading screenshot for comment {comment_id}:", error)
                continue

        browser.close()