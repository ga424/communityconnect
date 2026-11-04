"""Verify expected red evidence; never use this as an implementation pass gate."""
from pathlib import Path
import xml.etree.ElementTree as ET

root = ET.parse(Path('artifacts/pytest.xml')).getroot()
cases = root.findall('.//testcase')
s1 = [c for c in cases if c.attrib.get('classname') == 'tests.test_s1_requests']
s6 = [c for c in cases if c.attrib.get('classname') == 'tests.test_s6_payments']
harness = [c for c in cases if c.attrib.get('classname') == 'tests.test_harness']
assert len(cases) == 15 and len(s1) == 6 and len(s6) == 5 and len(harness) == 4
assert not root.findall('.//error'), 'Collection/setup failure is not a valid red baseline'
assert all(c.find('failure') is not None and '501' in (c.find('failure').text or '') for c in s1)
assert all(c.find('skipped') is not None and 'AC-' in c.find('skipped').attrib.get('message', '') for c in s6)
assert all(not any(c.find(t) is not None for t in ['failure','error','skipped']) for c in harness)
print('EXPECTED RED BASELINE: 4 harness passed; 6 S-1 semantic failures (501 stubs); 5 S-6 AC-labelled skips. No feature completion claimed.')
