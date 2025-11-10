from playwright.sync_api import sync_playwright
import os, pytest

def test_login():
    url = os.getenv("SITE_URL")
    user = os.getenv("TEST_USER")
    pwd  = os.getenv("TEST_PASS")

    print(f"🔍 Testing login page: {url}/login")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 打开页面
        page.goto(url + "/login", wait_until="load", timeout=60000)

        # 调试：输出当前URL和标题
        print("📍 Current URL:", page.url)
        print("📄 Page title:", page.title())

        # 等待输入框出现（最长60秒）
        try:
            page.wait_for_selector("input#email", timeout=60000)
        except Exception as e:
            html = page.content()
            print("❗ 页面源码片段（前1000字符）:")
            print(html[:1000])
            raise AssertionError("未找到 input#email。可能是Cloudflare拦截或页面未渲染。")

        # 正常执行填表
        page.fill("input#email", user)
        page.fill("input#password", pwd)
        page.click("button[type=submit]")

        # 等待跳转到 dashboard
        page.wait_for_url("**/dashboard", timeout=10000)
        assert "dashboard" in page.url

        browser.close()
