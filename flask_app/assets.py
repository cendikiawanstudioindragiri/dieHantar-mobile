from flask_assets import Bundle

# CSS bundle: main stylesheet + component-specific CSS can be appended later
main_css = Bundle(
    "css/app.css",
    filters="cssmin",
    output="gen/app.min.css",
)

# JS bundle: main script + page-specific scripts can be appended in templates via block scripts
main_js = Bundle(
    "js/app.js",
    filters="jsmin",
    output="gen/app.min.js",
)
