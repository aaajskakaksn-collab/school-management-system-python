# -*- coding: utf-8 -*-
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # debug turned off for production-readiness per request
    app.run(debug=False, host='0.0.0.0')
