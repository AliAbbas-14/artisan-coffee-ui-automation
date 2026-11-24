# Artisan Coffee - Web UI Test Automation Framework

Comprehensive Web UI Test Automation Solution built with **Python**, **Microsoft Playwright**, **Behave (BDD)**, **Allure Reporting**, and **Page Object Model (POM)** with multi-source test data integration (Excel, Database, and Redis).

[![UI Test Automation CI Pipeline](https://github.com/AliAbbas/artisan-coffee-automation/actions/workflows/ui_tests.yml/badge.svg)](.github/workflows/ui_tests.yml)

## 🌐 Live Presentation Website
- **Deployed Application Link:** [https://coffee-nu-jade.vercel.app/](https://coffee-nu-jade.vercel.app/)

---

## 🚀 Key Framework Features
- **Playwright Automation Engine:** High-performance, reliable web UI testing without Selenium flakiness.
- **Behavior-Driven Development (BDD):** Natural Gherkin syntax with Scenarios and Scenario Outlines.
- **Page Object Model (POM):** Clean separation of UI locators, interaction methods, and test specifications.
- **Multi-Source Data Integration:** Fetches test data seamlessly from:
  - 📊 **Excel Spreadsheets (`.xlsx`)** via `openpyxl`
  - 🗄️ **Relational Database (`SQLite`)** via SQL queries
  - ⚡ **Redis Cache (`RedisReader`)** with resilient in-memory fallback
- **Enterprise Reporting:** Allure Behave integration with automatic failure screenshot capture + standalone visual HTML report (`test_summary_report.html`).
- **Automated CI/CD Pipeline:** GitHub Actions workflow executing the entire test suite on every branch merge and pull request.

---

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
pip install -r automation_framework/requirements.txt
playwright install chromium
```

### 2. Seed Test Data
```bash
python automation_framework/data/seed_data.py
```

### 3. Run Test Suite
```bash
# Run all BDD scenarios and generate reports
python automation_framework/run_tests.py

# Run specific tags (e.g., @smoke, @datadriven, @forms)
python automation_framework/run_tests.py --tags=@smoke

# Run with visible browser window
python automation_framework/run_tests.py --headed
```

### 4. View Test Reports
- **Interactive HTML Report:** Open `automation_framework/reports/test_summary_report.html` in your browser.
- **Allure Report:**
  ```bash
  allure serve automation_framework/reports/allure-results
  ```

---

## 📖 Comprehensive Documentation
For detailed architecture diagrams, design decisions, group task allocations, and grading rubric alignments, refer to [FRAMEWORK_DOCUMENTATION.md](file:///e:/23F-3037%20Ali%20Abbas%20ST%20Presenatation%20SE-7A/FRAMEWORK_DOCUMENTATION.md).
