$ErrorActionPreference = "Stop"

python -m py_compile `
    solution.py `
    run_experiment.py `
    test_solution.py `
    benchmark.py `
    make_report.py `
    make_pdf.py

python -m unittest test_solution.py -v

python run_experiment.py

Write-Host ""
Write-Host "ALL CHECKS PASSED" -ForegroundColor Green