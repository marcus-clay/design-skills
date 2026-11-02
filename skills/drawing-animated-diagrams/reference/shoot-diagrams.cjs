const { chromium } = require('playwright')
const S = process.argv[2]
const pages = [
  ['scoping', '/fr/ressources/cadrage-de-conception'],
  ['sync', '/fr/ressources/synchro-po-design'],
  ['teardown', '/fr/ressources/atelier-design-teardown'],
  ['checklist', '/fr/ressources/checklist-conception-fonctionnalite'],
  ['slicing', '/en/ressources/ui-slicing'],
  ['status', '/en/ressources/figma-file-status'],
]
;(async () => { const browser = await chromium.launch()
for (const [vw, suffix] of [[1280, ''], [390, '-m']]) {
  const page = await browser.newPage({ viewport: { width: vw, height: 900 } })
  for (const [name, path] of pages) {
    await page.goto('http://localhost:3000' + path, { waitUntil: 'networkidle' })
    await page.evaluate(() => document.querySelector('[role="img"]')?.scrollIntoView({ block: 'center' }))
    await page.waitForTimeout(3200)
    const panel = page.locator('[role="img"]').first().locator('xpath=ancestor::div[contains(@class,"rounded-2xl")][1]')
    await panel.screenshot({ path: `${S}/diag-${name}${suffix}.png` })
    if (name === 'scoping') {
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800)
      await page.screenshot({ path: `${S}/header-${name}${suffix}.png` })
    }
  }
  await page.close()
}
await browser.close()
console.log('done') })()
