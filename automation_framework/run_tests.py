import os
import sys
import argparse
import subprocess
import json
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Run Playwright UI Automation Tests with Behave & Allure")
    parser.add_argument("--tags", "-t", default="", help="Run scenarios with specific tags, e.g., @smoke or @regression")
    parser.add_argument("--browser", "-b", default="chromium", choices=["chromium", "firefox", "webkit"], help="Browser engine")
    parser.add_argument("--headed", action="store_true", help="Run tests in headed browser mode (visible UI)")
    parser.add_argument("--base-url", default="https://coffee-nu-jade.vercel.app", help="Target Web App URL")
    parser.add_argument("--generate-report", "-g", action="store_true", default=True, help="Generate HTML summary report")
    return parser.parse_args()

def generate_html_summary(allure_dir: str, output_html: str, duration: float, returncode: int):
    results = []
    if os.path.exists(allure_dir):
        for fname in os.listdir(allure_dir):
            if fname.endswith("-result.json"):
                fpath = os.path.join(allure_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        results.append(json.load(f))
                except Exception:
                    pass

    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "passed")
    failed = sum(1 for r in results if r.get("status") == "failed")
    skipped = sum(1 for r in results if r.get("status") in ("skipped", "broken"))

    rows_html = ""
    for r in results:
        status = r.get("status", "unknown").upper()
        color = "#10b981" if status == "PASSED" else "#ef4444" if status == "FAILED" else "#f59e0b"
        name = r.get("name", "Unnamed Scenario")
        history_id = r.get("uuid", "")
        steps_count = len(r.get("steps", []))
        
        rows_html += f"""
        <tr style="border-bottom: 1px solid #2d3748;">
            <td style="padding: 12px 16px; font-weight: 500;">{name}</td>
            <td style="padding: 12px 16px;"><span style="background: {color}22; color: {color}; border: 1px solid {color}55; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600;">{status}</span></td>
            <td style="padding: 12px 16px; color: #94a3b8;">{steps_count} steps</td>
            <td style="padding: 12px 16px; color: #64748b; font-family: monospace; font-size: 11px;">{history_id[:8]}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Test Automation Report - Artisan Coffee</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 32px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            padding: 28px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        }}
        .title {{
            font-size: 26px;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #f1f5f9;
        }}
        .subtitle {{
            color: #94a3b8;
            font-size: 14px;
            margin: 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: #1e293b;
            border: 1px solid #334155;
            padding: 20px;
            border-radius: 12px;
        }}
        .stat-val {{
            font-size: 28px;
            font-weight: 700;
            margin-top: 4px;
        }}
        .card-table {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            overflow: hidden;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th {{
            background: #1e293b;
            padding: 14px 16px;
            color: #94a3b8;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid #334155;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">☕ Artisan Coffee - UI Automation Test Report</h1>
            <p class="subtitle">Playwright + Behave BDD + Allure Reporting | Target: <a href="https://coffee-nu-jade.vercel.app" style="color: #38bdf8;" target="_blank">coffee-nu-jade.vercel.app</a></p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: #94a3b8; font-size: 13px;">Total Scenarios</div>
                <div class="stat-val" style="color: #f8fafc;">{total}</div>
            </div>
            <div class="stat-card">
                <div style="color: #94a3b8; font-size: 13px;">Passed</div>
                <div class="stat-val" style="color: #10b981;">{passed}</div>
            </div>
            <div class="stat-card">
                <div style="color: #94a3b8; font-size: 13px;">Failed</div>
                <div class="stat-val" style="color: #ef4444;">{failed}</div>
            </div>
            <div class="stat-card">
                <div style="color: #94a3b8; font-size: 13px;">Execution Time</div>
                <div class="stat-val" style="color: #38bdf8;">{duration:.1f}s</div>
            </div>
        </div>

        <div class="card-table">
            <table>
                <thead>
                    <tr>
                        <th>Scenario Name</th>
                        <th>Status</th>
                        <th>Steps</th>
                        <th>UUID</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else '<tr><td colspan="4" style="padding: 24px; text-align: center; color: #64748b;">No test results found.</td></tr>'}
                </tbody>
            </table>
        </div>
        
        <p style="text-align: center; color: #64748b; font-size: 13px; margin-top: 24px;">
            Generated on {time.strftime("%Y-%m-%d %H:%M:%S")} | Playwright Test Automation Framework
        </p>
    </div>
</body>
</html>
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_html)), exist_ok=True)
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n[REPORT] Interactive HTML Test Summary created at: {output_html}")

def main():
    args = parse_args()
    
    # Configure environment
    os.environ["BASE_URL"] = args.base_url
    os.environ["BROWSER"] = args.browser
    os.environ["HEADLESS"] = "false" if args.headed else "true"
    
    framework_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(framework_dir)
    
    allure_results_dir = os.path.join(framework_dir, "reports", "allure-results")
    os.makedirs(allure_results_dir, exist_ok=True)

    cmd = [
        sys.executable, "-m", "behave",
        "--format", "allure_behave.formatter:AllureFormatter",
        "--outfile", "reports/allure-results",
        "--format", "pretty"
    ]
    if args.tags:
        cmd.extend(["--tags", args.tags])
        
    print(f"[TEST RUNNER] Executing: {' '.join(cmd)}")
    start_time = time.time()
    result = subprocess.run(cmd)
    duration = time.time() - start_time
    
    html_report_path = os.path.join(framework_dir, "reports", "test_summary_report.html")
    generate_html_summary(allure_results_dir, html_report_path, duration, result.returncode)
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
