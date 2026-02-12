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
        # Add stealth args
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

    async def perform_search(self, query: str):
        """
        Performs the search using Google with stealth settings.
        """
        # Stealth context
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
        )
        page = await context.new_page()
        
        try:
            print(f"Searching Google for: {query}")
            
            # Navigate to Google
            await page.goto("https://www.google.com", timeout=120000)
            
            # Handle consent if present (simple attempt)
            try:
                # Accept all button - varies by region, but often 'Accept all' or 'I agree'
                # We try a few common selectors
                await page.click('button:has-text("Accept all")', timeout=5000)
            except:
                pass

            # Type query and search
            # Google uses textarea[name="q"] or input[name="q"]
            await page.fill('[name="q"]', query, timeout=20000)
            await page.press('[name="q"]', 'Enter')
            
            # Wait for results
            # #search is the main container
            await page.wait_for_selector('#search', timeout=40000)
            
            # Click the first organic result
            # div.g represents a result container
            # h3 is the title
            result_selector = 'div.g h3'
            await page.wait_for_selector(result_selector, timeout=40000)
            
            # Click the h3, Playwright will click the center which usually triggers the link
            await page.click(f'{result_selector} >> nth=0')
            
            # Wait for page to load
            await page.wait_for_load_state("domcontentloaded", timeout=120000)
            
            # Extract HTML
            return await page.content()
            
        except Exception as e:
            error_msg = f"Error during automation: {e}"
            if page:
                try:
                    title = await page.title()
                    error_msg += f" | Page Title: {title}"
                    print(f"Debug Info: Title={title}")
                except:
                    pass
            print(error_msg)
            raise Exception(error_msg) from e
        finally:
            await context.close()
            
    async def check_health(self):
        """Simple health check to verify browser connectivity."""
        try:
            context = await self.browser.new_context()
            page = await context.new_page()
            await page.goto("https://example.com", timeout=10000)
            title = await page.title()
            await context.close()
            return title
        except Exception as e:
            return f"Health Check Failed: {e}"

    async def close(self):
        """Closes the browser and playwright instance."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
