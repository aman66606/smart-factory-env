Write-Host "Smart Factory Environment Deployer" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

$token = Read-Host "Enter your Hugging Face token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$PlainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$username = "amanpathak649"
$space = "smart-factory-env"

Write-Host "`nStep 1: Adding remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin "https://$username`:$PlainToken@huggingface.co/spaces/$username/$space"

Write-Host "`nStep 2: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "`nStep 3: Committing..." -ForegroundColor Yellow
git commit -m "Initial commit: Smart Factory Inventory Management Environment"

Write-Host "`nStep 4: Pushing to Hugging Face..." -ForegroundColor Yellow
git branch -M main
git push -u origin main --force

Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
Write-Host "Your Space: https://huggingface.co/spaces/$username/$space" -ForegroundColor Cyan
