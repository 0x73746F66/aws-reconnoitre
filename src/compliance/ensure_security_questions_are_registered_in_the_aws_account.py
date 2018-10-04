import helpers
import time
import pytz
from datetime import datetime


def ensure_security_questions_are_registered_in_the_aws_account(account, rule_config):
  return None, False



def report(record):
  print """
CIS version {version} Level {level} Recommendation {recommendation} ({scored})
Rule                  {rule}
Result                MANUAL ACTION REQUIRED
Rationale             {desc}
Recommended Control   {control}
""".format(
  rule=record['rule']['name'],
  desc=record['rule']['purpose'],
  control=record['rule']['control'],
  version=record['rule']['version'],
  level=record['rule']['level'],
  recommendation=record['rule']['recommendation'],
  scored='Scored' if record['rule']['scored'] else 'Not Scored'
)

