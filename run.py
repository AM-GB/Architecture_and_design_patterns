from wsgiref.simple_server import make_server

from my_first_framework.main import Framework
from patterns.structural_patterns import routes
from urls import fronts
from common.config import DEFAULT_PORT

application = Framework(routes, fronts)

with make_server('', DEFAULT_PORT, application) as httpd:
    print(f"Запуск на порту {DEFAULT_PORT}...")
    httpd.serve_forever()
