const { defineConfig } = require("@playwright/test");
const port = Number(process.env.TUNNELBOOKAI_E2E_PORT || 18766);

module.exports = defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  fullyParallel: false,
  workers: 1,
  reporter: "line",
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    channel: "chrome",
    headless: true,
    trace: "retain-on-failure"
  },
  webServer: {
    command: `PYTHONPATH=. .venv/bin/python -m tunnelbookai.dashboard --port ${port}`,
    url: `http://127.0.0.1:${port}/healthz`,
    reuseExistingServer: false,
    timeout: 30_000
  }
});
