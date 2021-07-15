from flask_assets import Environment, Bundle


BUNDLE_JS = (
    "js/lib/jquery.chained.remote.min.js",
    "js/lib/ajax_memory_cache.js",
    "js/lib/jquery.formalize.min.js",
    "js/lib/jquery.powertip.min.js",
    "js/main.js",
)


js = Bundle(*BUNDLE_JS, filters="jsmin", output="gen/static.js")
assets_env = Environment()
assets_env.register("js", js)
