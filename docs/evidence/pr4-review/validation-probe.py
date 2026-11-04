"""Diagnostic PR4 review against disposable synthetic cc_test; not approved tests."""
import json
import sys
sys.path.insert(0, '/workspace')
from fastapi.testclient import TestClient
from app.main import create_app
from app.seed import reset_fixtures
from app.models import connection

cases = [
 ('plain', json.dumps({'category':'Plumbing','description':'Kitchen sink leaks'})),
 ('blank', json.dumps({'category':'Plumbing','description':' \t\n'})),
 ('unicode', json.dumps({'category':'Plumbing','description':'é'})),
 ('nul', json.dumps({'category':'Plumbing','description':'Kitchen\x00leak'})),
 ('lone_high_surrogate', json.dumps({'category':'Plumbing','description':'\ud800'})),
 ('lone_low_surrogate', json.dumps({'category':'Plumbing','description':'\udfff'})),
 ('nested_invalid_shape', '{"category":"Plumbing","description":'+'['*1100+'0'+']'*1100+'}'),
]
results=[]
for label, raw in cases:
 reset_fixtures()
 with TestClient(create_app(),raise_server_exceptions=False) as client:
  response=client.post('/communities/1/requests',headers={'X-User-Id':'1','Content-Type':'application/json'},content=raw)
 with connection() as conn:
  count=conn.execute('SELECT count(*) AS n FROM maintenance_requests').fetchone()['n']
 result={'case':label,'status':response.status_code,'body':response.text,'persisted_rows':count}
 if response.status_code==500:
  reset_fixtures()
  try:
   with TestClient(create_app()) as client:
    client.post('/communities/1/requests',headers={'X-User-Id':'1','Content-Type':'application/json'},content=raw)
  except Exception as exc: result['exception_type']=type(exc).__name__;result['exception_message']=str(exc)
 results.append(result)
print(json.dumps({'probe_type':'diagnostic, not acceptance baseline','results':results},indent=2))
