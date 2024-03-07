from playwright.sync_api import sync_playwright
import os


def screenshot_post_and_comments(subreddit: str, post_id: str, comment_ids: list[str], output_dir: str):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        # Change user-agent to avoid being detected as a bot
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81')

        page.goto(
            url=f'https://www.reddit.com/r/{subreddit}/comments/{post_id}')

        # Screenshot post title
        page.locator(f'#{post_id}').screenshot(
            path=os.path.join(output_dir, f'{post_id}.png'))

        # Screenshot comments
        for comment_id in comment_ids:
            page.locator(f"shreddit-comment[thingid='{comment_id}']").screenshot(
                path=os.path.join(output_dir, f'{comment_id}.png'))

        browser.close()


if __name__ == '__main__':
    screenshot_post_and_comments(subreddit='AskReddit', post_id='t3_1b843u6', comment_ids=[
                                 't1_ktn6nxx'], output_dir='output/screenshots')
