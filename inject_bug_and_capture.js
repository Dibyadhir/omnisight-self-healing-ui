/**
 * OmniSight - Week 2 Mid-Project Review: Inject a Deliberate Bug
 * -----------------------------------------------------------------
 * Navigates to the checkout overview page, then injects broken CSS
 * at runtime to simulate real UI bugs a developer might accidentally
 * ship. Captures a screenshot of the broken state so we can test
 * whether the VLM (Gemini) actually catches these visual bugs.
 *
 * Bugs injected:
 *   1. The "Finish" button text becomes invisible (same color as its
 *      background) - a classic low-contrast bug.
 *   2. The order total gets pushed off the visible viewport using a
 *      large negative margin - a classic clipping/overflow bug.
 
 * Usage:
 *   node inject_bug_and_capture.js
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

BASE_URL = "http://localhost:5173/products"  
const CREDENTIALS = {
  username: 'standard_user',
  password: 'secret_sauce',
};
const SCREENSHOT_DIR = path.join(__dirname, 'screenshots');
const DOM_DIR = path.join(__dirname, 'dom_snapshots');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function saveDom(page, name) {
  const filePath = path.join(DOM_DIR, `${name}.html`);
  const html = await page.content();
  fs.writeFileSync(filePath, html, 'utf-8');
  console.log(`  DOM snapshot saved: ${filePath}`);
}

(async () => {
  ensureDir(SCREENSHOT_DIR);
  ensureDir(DOM_DIR);

  const browser = await chromium.launch({ headless: true });
  // Mobile viewport - matches the kind of bug OmniSight is designed to catch
  const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
  const page = await context.newPage();

  try {
    console.log('Logging in and navigating to checkout...');
    await page.goto(BASE_URL);
    await page.fill('#user-name', CREDENTIALS.username);
    await page.fill('#password', CREDENTIALS.password);
    await page.click('#login-button');
    await page.waitForSelector('.inventory_list');

    await page.click('.btn_inventory'); // add first product to cart
    await page.click('.shopping_cart_link');
    await page.waitForSelector('.cart_list');
    await page.click('#checkout');
    await page.waitForSelector('#first-name');

    await page.fill('#first-name', 'Ada');
    await page.fill('#last-name', 'Lovelace');
    await page.fill('#postal-code', '12345');
    await page.click('#continue');
    await page.waitForSelector('.summary_info');

    // --- Capture the CLEAN "before" screenshot + DOM for comparison ---
    console.log('Capturing clean baseline screenshot + DOM...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, 'checkout-overview-CLEAN.png'),
      fullPage: true,
    });
    await saveDom(page, 'checkout-overview-CLEAN');

    // --- Inject deliberate CSS bugs ---
    console.log('Injecting deliberate CSS bugs...');
    await page.addStyleTag({
      content: `
        /* BUG 1: Invisible button text - white text on white background */
        #finish {
          color: #ffffff !important;
          background-color: #ffffff !important;
          border: none !important;
        }

        /* BUG 2: Push the order total off-screen using a large negative margin */
        .summary_total_label {
          margin-left: -600px !important;
        }
      `,
    });

    // Give the browser a moment to apply styles before screenshotting
    await page.waitForTimeout(300);

    // --- Capture the BROKEN "after" screenshot + DOM ---
    console.log('Capturing bugged screenshot + DOM...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, 'checkout-overview-BUGGED.png'),
      fullPage: true,
    });
    await saveDom(page, 'checkout-overview-BUGGED');

    console.log('\nDone. Compare these files:');
    console.log('  screenshots/checkout-overview-CLEAN.png    (working page)');
    console.log('  screenshots/checkout-overview-BUGGED.png   (deliberately broken page)');
    console.log('  dom_snapshots/checkout-overview-CLEAN.html');
    console.log('  dom_snapshots/checkout-overview-BUGGED.html');
  } catch (err) {
    console.error('Error:', err);
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
})();