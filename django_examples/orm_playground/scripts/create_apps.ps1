
$apps=@(
 "core",
 "people",
 "catalog",
 "sales",
 "events",
 "reporting" 
)

foreach ($app in $apps) {
 python manage.py startapp $app
}
