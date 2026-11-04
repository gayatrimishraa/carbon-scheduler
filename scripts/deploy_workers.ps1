$regions = @("ap-south-1", "eu-north-1", "us-east-1")

foreach ($region in $regions) {
    Write-Host ""
    Write-Host "Deploying to $region ..." -ForegroundColor Cyan

    sam deploy `
        --template-file worker\template.yaml `
        --stack-name carbon-worker-$region `
        --region $region `
        --capabilities CAPABILITY_IAM `
        --resolve-s3 `
        --no-confirm-changeset

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Done: $region" -ForegroundColor Green
    } else {
        Write-Host "FAILED: $region" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "All deployments complete. Fetching ARNs..." -ForegroundColor Cyan

$config = @{}
foreach ($region in $regions) {
    $arn = aws cloudformation describe-stacks `
        --stack-name carbon-worker-$region `
        --region $region `
        --query "Stacks[0].Outputs[?OutputKey=='WorkerFunctionArn'].OutputValue" `
        --output text
    $config[$region] = $arn
    Write-Host "$region => $arn"
}

$config | ConvertTo-Json | Out-File -FilePath "config.json" -Encoding utf8
Write-Host ""
Write-Host "ARNs saved to config.json" -ForegroundColor Green