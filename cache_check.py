"""
    A standalone module for checking cache validity.
"""
import os


cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'routes')

invalid = '{"version": "1.1", "result": {"stops": [], "lineTraces": {"patternTraces": [], "zoom": {}}}}'

files = os.listdir(cache_dir)

bad_routes = []
for filename in files:
    filepath = os.path.join(cache_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as _file:
            content = _file.read()
            if len(content.strip()) == len(invalid):
                bad_routes.append(int(os.path.splitext(filename)[0]))

print sorted(bad_routes)
