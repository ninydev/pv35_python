import sys
sys.path.append('/home/keeper/PycharmProjects/pv35_python/DjangoProjectFromIDE/.venv/lib/python3.12/site-packages')
import django_eventstream
print("DIR:", dir(django_eventstream))
try:
    print("URLS:", getattr(django_eventstream, 'urls', None))
    print("ROUTING:", getattr(django_eventstream, 'routing', None))
except Exception as e:
    print("Error:", e)
