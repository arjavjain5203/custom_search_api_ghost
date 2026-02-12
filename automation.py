import asyncio
from playwright.async_api import async_playwright, Browser, Page

class SearchAutomation:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Browser = None
        self.playwright = None

    async def launch_browser(self):
        """Launches the browser instance."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

    async def perform_search(self, query: str):
        """
        Performs the search using DuckDuckGo HTML, clicks the first result, and returns the HTML content.
        """
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"Searching DuckDuckGo for: {query}")
            # Navigate to DuckDuckGo HTML (lite version, easier for automation)
            # Increased timeout for slower environments
            await page.goto("https://html.duckduckgo.com/html/", timeout=60000)
            
            # Type query and search
            await page.fill('input[name="q"]', query, timeout=10000) 
            await page.press('input[name="q"]', 'Enter')
            
            # Wait for results
            # The result link class in HTML version is usually 'result__a'
            result_selector = '.result__a'
            await page.wait_for_selector(result_selector, timeout=20000)
            
            # Click the first result
            # We take the first one
            await page.click(f'{result_selector} >> nth=0')
            
            # Wait for page to load
            await page.wait_for_load_state("domcontentloaded", timeout=60000)
            
            # Extract HTML
            return await page.content()
            
        except Exception as e:
            error_msg = f"Error during automation: {e}"
            if page:
                try:
                    title = await page.title()
                    error_msg += f" | Page Title: {title}"
                    content = await page.content()
                    # We can't save to file on read-only system easily, but we can log
                    print(f"Debug Info: Title={title}")
                except:
                    pass
            print(error_msg)
            raise Exception(error_msg) from e
        finally:
            await context.close()

    async def close(self):
        """Closes the browser and playwright instance."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
