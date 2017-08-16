# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:31:09 2017

@author: schro
"""
import os
from tweet_harvester import app
app.secret_key = os.urandom(24)
#app.run(debug=True)
# 'app' originates from the line 'app = Flask(__name__)'
#app.run(port=8080)

port = int(os.environ.get('PORT', 5000))
app.secret_key = os.urandom(24)
app.run(host='0.0.0.0', port=port)