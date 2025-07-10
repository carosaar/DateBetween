pyinstaller --noconsole --onefile ^
  --hidden-import=holidays ^
  --hidden-import=holidays.utils ^
  --hidden-import=holidays.calendars ^
  --hidden-import=holidays.countries ^
  --hidden-import=holidays.groups ^
  daysbetween.py