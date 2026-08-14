/**
 * OmniSight - Playwright Browser Automation Module
 * Mock e-commerce checkout flow, screenshots, and DOM extraction
 *
 * Target site: https://www.saucedemo.com/ (public test e-commerce site)
 *
 * Usage:
 *   npm install
 *   npx playwright install chromium
 *   node checkout.js
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ---- Config ----
const BASE_URL = 'https://www.saucedemo.com/';
const CREDENTIALS = {
  username: 'standard_user',
  password: 'secret_sauce',
};
const SCREENSHOT_DIR = path.join(__dirname, 'screenshots');
const OUTPUT_DIR = path.join(__dirname, 'output');

// Checkout form details (dummy data)
const CHECKOUT_INFO = {
  firstName: 'Dibya',
  lastName: 'Dhir',
  postalCode: '700001',
};

// ---- Helpers ----
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function screenshot(page, name) {
  const filePath = path.join(SCREENSHOT_DIR, `${name}.png`);
  await page.screenshot({ path: filePath, fullPage: true });
  console.log(`  📸 Screenshot saved: ${filePath}`);
}

// ---- Main flow ----
(async () => {
  ensureDir(SCREENSHOT_DIR);
  ensureDir(OUTPUT_DIR);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // 1. Navigate to the mock e-commerce site
    console.log('Step 1: Navigating to site...');
    await page.goto(BASE_URL);
    await screenshot(page, '01-login-page');

    
    
    // 2. Log in
    console.log('Step 2: Logging in...');
    await page.fill('#user-name', CREDENTIALS.username);
    await page.fill('#password', CREDENTIALS.password);
    await page.click('#login-button');
    await page.waitForSelector('.inventory_list');
    await screenshot(page, '02-inventory-page');

    // 3. Extract DOM data — product listings
    console.log('Step 3: Extracting product DOM data...');
    const products = await page.$$eval('.inventory_item', (items) =>
      items.map((item) => ({
        name: item.querySelector('.inventory_item_name')?.textContent.trim(),
        description: item.querySelector('.inventory_item_desc')?.textContent.trim(),
        price: item.querySelector('.inventory_item_price')?.textContent.trim(),
      }))
    );
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'products.json'),
      JSON.stringify(products, null, 2)
    );
    console.log(`  ✅ Extracted ${products.length} products -> output/products.json`);

    // 4. Add first two products to cart
    console.log('Step 4: Adding products to cart...');
    const addButtons = await page.$$('.btn_inventory');
    await addButtons[0].click();
    await addButtons[1].click();
    await screenshot(page, '03-products-added-to-cart');

    // 5. Go to cart
    console.log('Step 5: Opening cart...');
    await page.click('.shopping_cart_link');
    await page.waitForSelector('.cart_list');
    await screenshot(page, '04-cart-page');

    // Extract cart contents
    const cartItems = await page.$$eval('.cart_item', (items) =>
      items.map((item) => ({
        name: item.querySelector('.inventory_item_name')?.textContent.trim(),
        price: item.querySelector('.inventory_item_price')?.textContent.trim(),
        quantity: item.querySelector('.cart_quantity')?.textContent.trim(),
      }))
    );
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'cart.json'),
      JSON.stringify(cartItems, null, 2)
    );
    console.log(`  ✅ Extracted cart contents -> output/cart.json`);

    // 6. Begin checkout
    console.log('Step 6: Starting checkout...');
    await page.click('#checkout');
    await page.waitForSelector('#first-name');
    await screenshot(page, '05-checkout-info-page');

    // 7. Fill checkout form
    console.log('Step 7: Filling checkout information...');
    await page.fill('#first-name', CHECKOUT_INFO.firstName);
    await page.fill('#last-name', CHECKOUT_INFO.lastName);
    await page.fill('#postal-code', CHECKOUT_INFO.postalCode);
    await page.click('#continue');
    await page.waitForSelector('.summary_info');
    await screenshot(page, '06-checkout-overview-page');

    // 8. Extract order summary
    console.log('Step 8: Extracting order summary...');
    const summary = await page.$eval('.summary_info', (el) => el.innerText);
    fs.writeFileSync(path.join(OUTPUT_DIR, 'order-summary.txt'), summary);
    console.log('  ✅ Order summary saved -> output/order-summary.txt');

    // 9. Finish checkout
    console.log('Step 9: Completing checkout...');
    await page.click('#finish');
    await page.waitForSelector('.complete-header');
    await screenshot(page, '07-order-complete-page');

    const confirmationText = await page.$eval('.complete-header', (el) =>
      el.textContent.trim()
    );
    console.log(`  ✅ Checkout complete: "${confirmationText}"`);

    console.log('\n🎉 Full checkout flow completed successfully!');
  } catch (err) {
    console.error('❌ Error during automation:', err);
    await screenshot(page, 'error-state');
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
})();