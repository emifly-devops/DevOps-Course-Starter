describe('The index page', () => {
  it('successfully loads', () => {
    cy.visit('/')

    cy.get('input[name="title"]')
      .should('exist')
    cy.get('button:contains("Add to list")')
      .should('exist')
  })

  it('allows adding, editing and removing of a new task', () => {
    cy.visit('/')

    const new_task_title = "This is a new task!"
    cy.get('input[name="title"]').first()
      .type(new_task_title, { force: true })
    cy.get('button:contains("Add to list")')
      .click()

    cy.get(`li:contains("${new_task_title}")`)
      .should('exist')

    const modified_task_title = "This is a modified task!"
    const modified_task_description = "This is the description for the modified task."
    cy.get(`li:contains("${new_task_title}") button[aria-label="Edit"]`).first()
      .click()
    cy.get('.modal.show input[name="title"]')
      .clear({ force: true })
      .type(modified_task_title, { force: true })
    cy.get('.modal.show textarea[name="description"]')
      .type(modified_task_description, { force: true })
    cy.get('.modal.show button[type="submit"]')
      .click()

    cy.get(`li:contains("${modified_task_title}")`)
      .should('exist')
    cy.get(`li:contains("${new_task_title}")`)
      .should('not.exist')

    cy.get(`li:contains("${modified_task_title}") button[aria-label="Delete"]`).first()
      .click()
    cy.get('.modal.show button[type="submit"]')
      .click()

    cy.get(`li:contains("${modified_task_title}")`)
      .should('not.exist')
  })
})
