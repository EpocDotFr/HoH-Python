from datetime import datetime
from HoH import app
import humanize

@app.template_filter('time_ago')
def natural_datetime(dt):
    return humanize.naturaltime(datetime.utcnow() - dt)
