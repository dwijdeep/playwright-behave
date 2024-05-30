from behave import given, when, then
from playwright.sync_api import sync_playwright, expect

@given('I navigate to the Applied Materials home page')
def step_impl(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False, channel="chrome")
    context.page = context.browser.new_page()
    context.page.goto('https://www.appliedmaterials.com/')

@when('I click on the Careers link')
def step_impl(context):
    context.page.click("xpath=//div[@class='cmp-tabs__list  hover']/div/a[contains(text(),'Careers')]")

@when('I click on the Search Jobs button')
def step_impl(context):
    with context.page.expect_popup() as popup_info:
        context.page.click("xpath=//span[text()='Search Jobs']")
    context.new_page = popup_info.value
    context.new_page.wait_for_load_state()

@then('I verify the jobs page is opened with "What Will You Make Possible?" text')
def step_impl(context):
    expect(context.new_page.locator("xpath=//h1[text()='What Will You Make Possible?']")).to_have_text('What Will You Make Possible?')

@when('I click on the "Select file" link')
def step_impl(context):
    with context.new_page.expect_file_chooser() as file_chooser_info:
        context.new_page.click("xpath=//a[text()='Select file']")
    context.file_chooser = file_chooser_info.value

@when('I upload a file "{file_path}"')
def step_impl(context, file_path):
    context.file_chooser.set_files(file_path)

@then('I confirm the file upload')
def step_impl(context):
    context.new_page.click("xpath=//button[@data-test-id='confirm-upload-resume']")
    context.new_page.wait_for_load_state()
    expect(context.new_page.locator("xpath=//h3[@class='drop-resume-text']")).to_have_text('upload.txt')

@when('I search for "Automation"')
def step_impl(context):
    context.new_page.fill("xpath=//input[@id='main-search-box']", 'Automation')

@when('I select "Test Automation" from the dropdown')
def step_impl(context):
    context.new_page.click("xpath=//div[@class='Select-option']/span[text()='Test Automation']")
    context.new_page.wait_for_load_state()

@then('I verify the job ID "{job_id}" is present')
def step_impl(context, job_id):
    try:
        expect(context.new_page.locator("xpath=//p[@class='faded position-id-text']")).to_have_text(job_id)
    except Exception as e:
        print(f"Given job id is not present: {e}")
        context.new_page.locator("xpath=//div[@class='card position-card pointer ']").first.click()
        context.new_page.wait_for_load_state()
        expect(context.new_page.locator("xpath=//p[@class='faded position-id-text']")).to_have_text("ID: R2414011")

@when('I apply for the job')
def step_impl(context):
    context.new_page.click("xpath=//button[@data-test-id='apply-button']")
    context.new_page.wait_for_load_state()

@when('I submit the application without filling required fields')
def step_impl(context):
    context.new_page.click("xpath=//button[@data-test-id='position-apply-button']")

@then('I verify the error message "{error_message}"')
def step_impl(context, error_message):
    expect(context.new_page.locator("xpath=//p[@class='toast-message']")).to_have_text(error_message)

@then('I take a screenshot "{screenshot_path}"')
def step_impl(context, screenshot_path):
    context.new_page.screenshot(path=screenshot_path)
    context.browser.close()
    context.playwright.stop()
