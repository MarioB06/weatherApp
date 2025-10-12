const { test, expect } = require('@playwright/test');

const historyFixture = [
  {
    city: 'Zürich',
    country: 'CH',
    temp: 12.3,
    timestamp: '2024-04-05T09:30:00.000Z',
  },
];

test.beforeEach(async ({ page }) => {
  await page.route('**/history', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(historyFixture),
    });
  });
});

test('zeigt Fehlermeldung, wenn keine Stadt eingegeben wurde', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Suchen' }).click();
  await expect(page.getByText('Bitte Stadt eingeben')).toBeVisible();
});

test('zeigt Wetterdaten und aktualisiert Verlauf', async ({ page }) => {
  await page.route('**/weather?*', async (route) => {
    const url = new URL(route.request().url());
    const city = url.searchParams.get('city');
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        city,
        country: 'DE',
        temp: 18.5,
        feels_like: 17.2,
        condition: 'Leicht bewölkt',
        timestamp: '2024-04-05T10:00:00.000Z',
      }),
    });
  });

  await page.goto('/');
  await page.getByPlaceholder('Stadt eingeben...').fill('Berlin');
  await page.getByRole('button', { name: 'Suchen' }).click();

  await expect(page.getByText('Berlin, DE')).toBeVisible();
  await expect(page.getByText(/Leicht bewölkt/)).toBeVisible();
  await expect(page.getByRole('heading', { level: 2, name: 'Verlauf' })).toBeVisible();
  await expect(page.getByText(/Zürich, CH/)).toBeVisible();
});
