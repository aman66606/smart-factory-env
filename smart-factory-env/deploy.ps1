# deploy.ps1
Write-Host "Smart Factory Environment Deployer" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

$token = "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"
$username = "amanpathak649"
$space = "smart-factory-env"

Write-Host "`nStep 1: Creating files if missing..." -ForegroundColor Yellow

# Create files if they don't exist
$files = @("app.py", "environment.py", "tasks.py", "inference.py", "requirements.txt", "Dockerfile", "README.md", "openenv.yaml", ".gitignore")
foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        Write-Host "  Creating $file" -ForegroundColor Red
        New-Item -Path $file -ItemType File -Force | Out-Null
    } else {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
    }
}

Write-Host "`nStep 2: Initializing git..." -ForegroundColor Yellow
git init

Write-Host "`nStep 3: Adding remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin "https://$username`:$token@huggingface.co/spaces/$username/$space"

Write-Host "`nStep 4: Adding files..." -ForegroundColor Yellow
git add .

Write-Host "`nStep 5: Committing..." -ForegroundColor Yellow
git commit -m "Initial commit: Smart Factory Inventory Management Environment"

Write-Host "`nStep 6: Pushing to Hugging Face..." -ForegroundColor Yellow
git branch -M main
git push -u origin main --force

Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
Write-Host "Your Space: https://huggingface.co/spaces/$username/$space" -ForegroundColor Cyan
Write-Host "Build logs: https://huggingface.co/spaces/$username/$space/logs" -ForegroundColor Cyan