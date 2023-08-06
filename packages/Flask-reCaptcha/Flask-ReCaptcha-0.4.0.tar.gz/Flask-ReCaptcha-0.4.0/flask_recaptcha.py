"""
The new Google ReCaptcha implementation for Flask without Flask-WTF
Can be used as standalone
"""

__NAME__ = "Flask-ReCaptcha"
__version__ = "0.4.0"
__license__ = "MIT"
__author__ = "Mardix"
__copyright__ = "(c) 2015 Mardix"

try:
    from flask import request
    from jinja2 import Markup
    import requests
except ImportError as ex:
    print("Missing dependencies")

class ReCaptcha(object):

    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    site_key = None
    secret_key = None
    is_enabled = True

    def __init__(self, app=None, site_key=None, secret_key=None, is_enabled=True):

        if site_key:
            self.site_key = site_key
            self.secret_key = secret_key
            self.is_enabled = is_enabled

        elif app:
            self.init_app(app=app)

    def init_app(self, app=None):
        self.__init__(site_key=app.config.get("RECAPTCHA_SITE_KEY"),
                      secret_key=app.config.get("RECAPTCHA_SECRET_KEY"),
                      is_enabled=app.config.get("RECAPTCHA_ENABLED", True))

        @app.context_processor
        def get_code():
            return dict(recaptcha=Markup(self.get_code()))

    def get_code(self):
        """
        Returns the new ReCaptcha code
        :return:
        """
        return "" if not self.is_enabled else ("""
        <script src='//www.google.com/recaptcha/api.js'></script>
        <div class="g-recaptcha" data-sitekey="{SITE_KEY}"></div>
        """.format(SITE_KEY=self.site_key))

    def verify(self, response=None, remote_ip=None):
        if not self.is_enabled:
            return True

        data = {
            "secret": self.secret_key,
            "response": response or request.form.get('g-recaptcha-response'),
            "remoteip": remote_ip or request.environ.get('REMOTE_ADDR')
        }

        r = requests.get(self.VERIFY_URL, params=data)
        if r.status_code == 200:
            return r.json()["success"]
        else:
            return False
