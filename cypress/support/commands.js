import { TOTP } from 'totp-generator'

Cypress.Commands.add('login', () => {
  cy.visit('/')

  cy.get('nav.navbar').then((navbar) => {
    if (navbar.find('a:contains("Log in with GitHub")').length > 0) {
      cy.get('a:contains("Log in with GitHub")').click()
    }
  })

  cy.origin('github.com', { args: { otpContainer: TOTP.generate(Cypress.env('OAUTH_OTP_SECRET')) } }, ({ otpContainer }) => {
    cy.location().then((location) => {
      if (location?.pathname === '/login') {
        cy.get('input[name="login"]')
          .type(Cypress.env('OAUTH_USERNAME'))
        cy.get('input[name="password"]')
          .type(Cypress.env('OAUTH_PASSWORD'))
        cy.get('input[type="submit"]')
          .click()
      }
    })
    cy.location().then((location) => {
      if (location?.pathname === '/sessions/two-factor/app') {
        const { otp } = otpContainer
        cy.get('input[name="app_otp"]')
          .type(otp)
      }
    })
    cy.location().then((location) => {
      if (location?.pathname === '/login/oauth/authorize') {
        const randomWaitDurationInMs = Math.floor(2000 * (Math.random() + 1))
        cy.wait(randomWaitDurationInMs)
      }
    })
    cy.location().then((location) => {
      if (location?.pathname === '/login/oauth/authorize') {
        cy.get('button[name="authorize"]').first().click()
      }
    })
  })
})
