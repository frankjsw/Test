from playwright.sync_api import sync_playwright
import os, pytest

def test_login():
    url = os.getenv("SITE_URL")
    user = os.getenv("TEST_USER")
    pwd  = os.getenv("TEST_PASS")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)      # headless 可用，因为 Turnstile 在测试环境被绕过
        page = browser.new_page()
        page.goto(url + "/login")
        page.fill("input#email", user)
        page.fill("input#password", pwd)
        page.click("button[type=submit]")
        page.wait_for_url("**/dashboard", timeout=10000)
        assert "dashboard" in page.url
        browser.close()
