import os
from c300s import C300S
from h5051 import H5051
from flask import Flask

vesync_id = os.environ['VESYNC_ID']
vesync_password = os.environ['VESYNC_PASSWORD']
vesync_timezone = os.environ['VESYNC_TIMEZONE']

app = Flask(__name__)


@app.route("/")
def environment():
    c300s = C300S(vesync_id, vesync_password, vesync_timezone)
    h5051 = H5051()
    h5051.update()

    body = ""
    body += "<p> 温度 " + str(h5051.temperature) + "度" + "</p>"
    body += "<p> 湿度 " + str(h5051.humidity) + "％" + "</p>"
    body += "<p> PM2.5 " + str(c300s.get_air_quality()) + "ug/㎥" + "</>"

    return body


app.run(host='0.0.0.0', port=5000)
