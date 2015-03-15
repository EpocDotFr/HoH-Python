from datetime import datetime
from HoH import app
import humanize

@app.template_filter('time_ago')
def natural_datetime(dt):
    humanize.i18n.activate('fr_FR')

    return humanize.naturaltime(datetime.now() - dt)
