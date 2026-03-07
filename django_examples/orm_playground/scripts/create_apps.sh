
APPS=(
core
people
catalog
sales
events
reporting
)

  for APP in "${APPS[@]}"; do
    echo "Create app: $APP"
    python manage.py startapp "$APP"
  done

  echo "All apps created"