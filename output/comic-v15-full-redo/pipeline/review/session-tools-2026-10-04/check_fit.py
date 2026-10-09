"""Before assemble b: the fit report's statuses and the panels the planner could not place at any height."""
import json, sys
f = json.load(open(sys.argv[1]))
pr = f.get('probe') or {}
print('fit statuses', f['statuses'], '| probe unplaceable:', pr.get('unplaceable') or 'none', '| unprobed:', pr.get('unprobed') or 'none')
