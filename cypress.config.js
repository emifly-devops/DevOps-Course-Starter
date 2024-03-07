require('dotenv').config()
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5000',
    testIsolation: false,
  },
  env: {
    OAUTH_USERNAME: process.env.CYPRESS_OAUTH_USERNAME,
    OAUTH_PASSWORD: process.env.CYPRESS_OAUTH_PASSWORD,
    OAUTH_OTP_SECRET: process.env.CYPRESS_OAUTH_OTP_SECRET,
  },
})
