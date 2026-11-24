# Web UI Test Automation Framework - Comprehensive Documentation

**Project:** Building a UI Test Automation Solution (Project Phase 2)  
**Domain:** Artisan Coffee Web Application  
**Live Deployed Application:** [https://coffee-nu-jade.vercel.app/](https://coffee-nu-jade.vercel.app/)  
**Automation Engine:** Microsoft Playwright (Python)  
**BDD Framework:** Behave (Gherkin syntax)  
**Reporting Tool:** Allure + Standalone Interactive HTML Reports  
**Repository Architecture:** Page Object Model (POM) with Multi-Source Data Management (Excel, SQLite, Redis)

---

## 1. Project Overview & Group Task Allocation Matrix

This test automation framework delivers an enterprise-grade Web UI automation solution adhering to modern software testing standards. Although developed by a solo engineer (**Ali Abbas - Roll No: 23F-3037**), the project structure strictly adheres to the course requirements by breaking down into specialized modules assigned across a balanced 2-member collaborative delivery matrix:

| Task Area | Module Scope & Deliverables | Primary Assignee | Status |
|:---|:---|:---|:---:|
| **Core Architecture & POM** | BasePage setup, Playwright browser engine lifecycle, Page Object classes (`HomePage`, `MenuPage`, `BlendPage`, `NewsletterPage`, `LocationsPage`) | **Member 1** (Ali Abbas) | **Completed** |
| **BDD & Gherkin Specifications** | Feature files (`.feature`), Scenarios, Scenario Outlines with Examples tables, Step Definitions under `features/steps/` | **Member 1** (Ali Abbas) | **Completed** |
| **Data Source Integration** | Excel reader (`openpyxl`), SQLite database query engine, Redis cache client & resilient in-memory fallback, `DataManager` facade | **Member 2** (Ali Abbas) | **Completed** |
| **Reporting & Allure Integration** | Allure Behave lifecycle hooks, automatic failure screenshot attachments, interactive standalone HTML test dashboard | **Member 2** (Ali Abbas) | **Completed** |
| **CI/CD & GitHub Management** | GitHub Actions workflow (`.github/workflows/ui_tests.yml`), PR template, Issue templates, Git version control | **Member 1 & 2** | **Completed** |

---

## 2. Framework Architecture & Design Decisions

### A. Page Object Model (POM) Pattern
The framework decouples web locators and UI interactions from the test scenario logic:
- **`BasePage` (`automation_framework/pages/base_page.py`)**: Centralizes core Playwright operations: element waiting, clicking, text retrieval, input population, and screenshot captures.
- **Dedicated Page Objects**:
  - `HomePage`: Hero section, brand logo, navigation buttons (`MENU`, `STORY`, `BLEND`, `REVIEWS`, `LOCATIONS`), Order CTAs.
  - `MenuPage`: Signature menu items ("Black Label Espresso", "Velvet Oat Latte", "Midnight Cold Brew"), roast origin profiles, and pricing.
  - `BlendPage`: "The Blend Lab" roast decoder, interactive roast ordering buttons (`ORDER ESPRESSO NOIR`, `ORDER MORNING GOLD`, `ORDER VELVET HOUR`).
  - `NewsletterPage`: The Coffee Letter email subscription form, input verification, and submission handlers.
  - `LocationsPage`: Flagship locations (Lahore, MM Alam Road, Gulberg III), directions buttons.

### B. Behavior-Driven Development (BDD) with Gherkin
Tests are written in natural human-readable Gherkin syntax within `features/*.feature`:
- **Scenario Outline**: Enables data-driven test cases executing the same user journey with multiple input datasets.
- **Clean Step Definitions**: Modular Python functions in `features/steps/` mapping `Given`, `When`, `Then` steps directly to Page Object methods.

### C. Multi-Source Data Management Pattern (Facade)
The `DataManager` facade (`automation_framework/data/data_manager.py`) allows tests to consume test data uniformly regardless of the persistence medium:
1. **Excel Integration (`ExcelReader`)**: Reads structured multi-sheet test datasets from `automation_framework/data/test_data.xlsx` (`MenuProducts`, `NewsletterData`, `BlendData`) using `openpyxl`.
2. **Database Integration (`DatabaseReader`)**: Connects directly to SQLite (`dev.db`), executing parameterized queries against `CoffeeMenu` and `NewsletterSubscribers` tables.
3. **Redis Caching (`RedisReader`)**: Connects to Redis with automatic fallback to a resilient in-memory cache to guarantee test stability across any local machine or CI runner without external Redis service dependencies.

---

## 3. Directory Structure

```text
23F-3037 Ali Abbas ST Presenatation SE-7A/
├── .github/
│   ├── workflows/
│   │   └── ui_tests.yml                # Automated GitHub Actions CI workflow
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md               # GitHub Issue template for bug tracking
│   └── pull_request_template.md        # Pull request template with QA checklist
├── automation_framework/
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py                   # Central environment & browser configuration
│   ├── data/
│   │   ├── __init__.py
│   │   ├── excel_reader.py             # OpenPyXL Excel data reader
│   │   ├── db_reader.py                # SQLite relational database client
│   │   ├── redis_reader.py             # Redis client with resilient in-memory cache
│   │   ├── data_manager.py             # Unified DataManager facade
│   │   ├── test_data.xlsx              # Excel test dataset (Menu, Newsletter, Blends)
│   │   └── seed_data.py                # Script to generate test data and seed DB
│   ├── features/
│   │   ├── environment.py              # Behave lifecycle hooks & Allure screenshot integration
│   │   ├── landing_and_navigation.feature
│   │   ├── menu_catalog.feature
│   │   ├── blend_lab.feature
│   │   ├── newsletter_form.feature
│   │   ├── data_sources.feature
│   │   └── steps/
│   │       ├── __init__.py
│   │       ├── landing_and_navigation_steps.py
│   │       ├── menu_steps.py
│   │       ├── blend_steps.py
│   │       ├── newsletter_steps.py
│   │       └── data_source_steps.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py                # Playwright Base Page Object
│   │   ├── home_page.py                # Landing & Hero view
│   │   ├── menu_page.py                # Signature Menu catalog
│   │   ├── blend_page.py               # Blend Lab interactive profiles
│   │   ├── newsletter_page.py          # Email subscription form
│   │   └── locations_page.py           # Store locations view
│   ├── reports/
│   │   ├── allure-results/             # Allure raw JSON and screenshot attachments
│   │   └── test_summary_report.html    # Standalone visual HTML test dashboard
│   ├── behave.ini                      # Behave BDD runner settings
│   ├── requirements.txt                # Python dependencies
│   └── run_tests.py                    # All-in-one test execution and report generation CLI
├── FRAMEWORK_DOCUMENTATION.md          # Technical framework specifications
└── README.md                           # Quick start and project overview
```

---

## 4. Setup and Installation

### Prerequisites
- Python 3.10+ (Python 3.12 verified)
- Git

### Installation Steps
```bash
# 1. Clone repository
git clone <your-repo-url>
cd "23F-3037 Ali Abbas ST Presenatation SE-7A"

# 2. Install Python dependencies
pip install -r automation_framework/requirements.txt

# 3. Install Playwright browser binaries
playwright install chromium

# 4. Generate & seed test datasets (Excel, SQLite, Redis fallback)
python automation_framework/data/seed_data.py
```

---

## 5. Test Execution Guide

### Run All Tests with Allure & HTML Report Generation
```bash
python automation_framework/run_tests.py
```

### Run by Specific Tags
```bash
# Smoke tests only
python automation_framework/run_tests.py --tags=@smoke

# Data-driven scenarios only
python automation_framework/run_tests.py --tags=@datadriven

# Form automation scenarios only
python automation_framework/run_tests.py --tags=@forms
```

### Run in Headed Browser Mode (Watch UI live)
```bash
python automation_framework/run_tests.py --headed
```

---

## 6. Test Reports & Verification Outcomes

### Verified Execution Results
- **Features Tested:** 5 Features
- **Scenarios Executed:** 21 Scenarios
- **Steps Verified:** 73 Steps
- **Success Rate:** **100% Passed (0 Failures, 0 Skipped)**
- **Execution Time:** ~53 seconds

### Visual Reporting
1. **Interactive HTML Dashboard:** Open `automation_framework/reports/test_summary_report.html` directly in any web browser to view pass/fail statistics, execution timing, and scenario breakdowns.
2. **Allure Visual Reports:** The raw results are captured in `automation_framework/reports/allure-results/`. If the Allure CLI is installed, serve the full interactive web report with:
   ```bash
   allure serve automation_framework/reports/allure-results
   ```

---

## 7. Continuous Integration (GitHub Actions)

The framework includes a fully automated CI pipeline defined in [`.github/workflows/ui_tests.yml`](file:///.github/workflows/ui_tests.yml):
- **Triggers:** Automatically runs on every `push` and `pull_request` targeting `main`/`master`, as well as on branch merges.
- **Workflow Steps:**
  1. Checks out repository code.
  2. Sets up Python 3.12 environment with caching.
  3. Installs dependencies from `requirements.txt`.
  4. Downloads Playwright Chromium browser binaries and system libraries.
  5. Seeds test data into Excel and SQLite.
  6. Executes the complete test suite against `https://coffee-nu-jade.vercel.app/`.
  7. Archives and uploads Allure test artifacts and HTML reports for review.

---

## 8. Live Application Link for Presentation
- **Target Deployed Website:** [https://coffee-nu-jade.vercel.app/](https://coffee-nu-jade.vercel.app/)
