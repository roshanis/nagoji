// Render images/map_source/map_malabar.svg to images/map_malabar.png and .jpg.
// Needs Playwright (npm i -g playwright) and a Chromium it can launch.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const here = __dirname;
  const svg = fs.readFileSync(path.join(here, 'map_malabar.svg'), 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1500, height: 2000 } });
  await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const clip = { x: 0, y: 0, width: 1500, height: 2000 };
  await page.screenshot({ path: path.join(here, '..', 'map_malabar.png'), clip });
  await page.screenshot({ path: path.join(here, '..', 'map_malabar.jpg'), clip, type: 'jpeg', quality: 88 });
  await browser.close();
  console.log('rendered images/map_malabar.png and images/map_malabar.jpg');
})();
