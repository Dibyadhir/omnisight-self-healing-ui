const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    const browser = await chromium.launch({ headless: false });

    const page = await browser.newPage({
        viewport: { width: 1280, height: 720 }
    });

    console.log("Opening Her Comfort...");

    await page.goto('http://127.0.0.1:5000', {
        waitUntil: 'networkidle'
    });

    await page.screenshot({
        path: 'screenshots/hercomfort-home.png',
        fullPage: true
    });

    const dom = await page.content();

    fs.writeFileSync(
        'dom_snapshots/hercomfort-home.html',
        dom,
        'utf-8'
    );

    console.log("Screenshot saved:");
    console.log("screenshots/hercomfort-home.png");

    console.log("DOM saved:");
    console.log("dom_snapshots/hercomfort-home.html");

    await browser.close();
})();