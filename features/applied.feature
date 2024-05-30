Feature: Applied Materials Test

  Scenario: Verify job search and application process
    Given I navigate to the Applied Materials home page
    When I click on the Careers link
    And I click on the Search Jobs button
    Then I verify the jobs page is opened with "What Will You Make Possible?" text
    When I click on the "Select file" link
    And I upload a file "./resources/upload.txt"
    Then I confirm the file upload
    When I search for "Automation"
    And I select "Test Automation" from the dropdown
    Then I verify the job ID "ID: R2413936" is present
    When I apply for the job
    And I submit the application without filling required fields
    Then I verify the error message "Please fill all required fields (marked with *)"
    And I take a screenshot "resources/screenshots/screenshot.png"
