# Urban Routes — UI Test Automation

UI automation project developed as part of the TripleTen QA Engineering program. The project uses Python, Selenium WebDriver, and pytest to test a taxi-booking workflow.

## Project Objective

Validate the main steps of booking a ride, from entering the route to requesting a taxi and displaying driver information.

## Technologies

- Python
- Selenium WebDriver
- pytest
- Google Chrome
- Git and GitHub
- Page Object Model (POM)

## Test Scenarios

The test suite covers:

1. Entering and checking pickup and destination addresses.
2. Selecting the Comfort fare.
3. Entering a phone number and completing phone verification.
4. Adding a payment card and checking the selected payment method.
5. Entering and checking a message for the driver.
6. Selecting the blanket and handkerchiefs option.
7. Adding two ice creams.
8. Requesting a taxi and waiting for driver information.

## My Contribution

I implemented page locators, reusable page methods, and automated test scenarios using the Page Object Model.

My work included explicit waits, form interactions, UI assertions, and integration of the phone-verification helper provided with the project. I also investigated browser configuration and element-location issues during development.

## Repository Structure

- `main.py`: Page Object, automated tests, browser setup, and phone-verification helper.
- `data.py`: Application URL and test data.
- `.gitignore`: Excludes Python cache files and local test artifacts.
- `README.md`: Project overview and execution instructions.

## Requirements

- Python 3
- Google Chrome
- An active TripleTen Urban Routes training server
- Internet access for the application and initial browser-driver setup

## Installation

Clone the repository:

```bash
git clone https://github.com/GGO88-German/qa-project-Urban-Routes-es.git
cd qa-project-Urban-Routes-es
```

Install the dependencies:

```bash
python -m pip install selenium pytest
```

## Configuration

Start the Urban Routes training server and update `urban_routes_url` in `data.py` with its current URL.

Use only the training application's test data for phone and payment fields.

## Running the Tests

Run the complete suite from the repository directory:

```bash
python -m pytest -v main.py
```

The tests share one browser session and depend on the workflow established by preceding tests. Run the complete suite in its defined order rather than running later scenarios individually.

The application must use Spanish because several locators and assertions match Spanish interface text.

## Results and Limitations

The repository contains eight automated test scenarios with UI interactions and assertions.

Execution results depend on the availability of the training server and the current application behavior. No current pass rate is claimed in this README; run the suite against an active environment to obtain updated results.

The project demonstrates test design, reusable browser interactions, explicit waits, and validation of a multi-step user workflow.

## Author

German Gonzalez Oregel

LinkedIn: https://www.linkedin.com/in/german-gonzalez-oregel-729a0243/

## Educational Context

This project uses the Urban Routes training application and starter materials provided by TripleTen.
