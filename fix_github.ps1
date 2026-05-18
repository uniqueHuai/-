# 修复 Obsidian 语法 -> GitHub 兼容
param(
    [string]$FilePath = "java学习篇/Java基础与进阶篇.md"
)

$vaultRoot = "D:\文档\Obsidian Vault"
$fullPath = Join-Path $vaultRoot $FilePath

Write-Host "读取: $fullPath"
$content = Get-Content -Path $fullPath | Out-String

# 1. 转换 Callout 类型
$content = $content -replace '> \[!info\]',    '> [!NOTE]'
$content = $content -replace '> \[!tip\]',     '> [!TIP]'
$content = $content -replace '> \[!warning\]', '> [!WARNING]'
$content = $content -replace '> \[!danger\]',  '> [!CAUTION]'
$content = $content -replace '> \[!success\]', '> [!IMPORTANT]'

# 2. 拆分同一行有内容的 Callout
#    > [!NOTE] 内容 → > [!NOTE]\n> 内容
$content = $content -replace '(> \[!(?:NOTE|TIP|WARNING|CAUTION|IMPORTANT)\])\s(.+)', "`$1`r`n> `$2"

# 3. 转换 WikiLink [[笔记名]] → [笔记名](./笔记名.md)
$content = $content -replace '\[\[([^\]|]+?)\]\]', '[$1](./$1.md)'

# 写回
$content | Set-Content -Path $fullPath
Write-Host "✅ 修复完成: $FilePath"
