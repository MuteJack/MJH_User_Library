# 사용자 환경변수 백업
[Environment]::GetEnvironmentVariable("PATH", "User") | Out-File "$env:USERPROFILE\path_user_backup.txt"

# 시스템 환경변수 백업
[Environment]::GetEnvironmentVariable("PATH", "Machine") | Out-File "$env:USERPROFILE\path_system_backup.txt"
