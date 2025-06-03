import json
import re

from openai import OpenAI

from app.models.job_posting import JobPosting
from app.prompts import job_scrape_prompt
from playwright.async_api import async_playwright

GPT_MODEL = "gpt-4o-mini"

async def extract_visible_text(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=20000)
        await page.wait_for_timeout(2000)  # allow JS to settle

        # Extract text from body
        content = await page.locator("body").inner_text()
        await browser.close()

        return content.strip()

async def extract_job_posting(client: OpenAI, url: str, optional_job_text: str | None = None) -> JobPosting:
    print("Beginning url job extraction")
    try:
        if optional_job_text:
            scraped_data = optional_job_text
        else:
            scraped_data = await extract_visible_text(url)

        scrape_prompt = job_scrape_prompt(scraped_data)

        response = client.responses.create(
        model=GPT_MODEL,
        instructions="You are an applicant tracking system and an expert resume analyst",
        input=scrape_prompt
        )

        parsed = None
        match = re.search(r"\{.*\}", response.output[0].content[0].text, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))

        return JobPosting(**parsed)
    except Exception as e:
        print(f"Error while extracting post posting: {e}")
        return None