from .models import Task
from datetime import datetime, timezone

def parse_time(time_str):
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

def get_free_slots(busy_slots, deadline, min_hours=1):
  free_slots = []
  now = datetime.now(timezone.utc)
  if not busy_slots:
     return[{'start': now, 'end': deadline, 'time': deadline - now}]
  free_slots.append({
    'time':parse_time(busy_slots[0]["start"])-now,
    'start': now,
    'end': parse_time(busy_slots[0]["start"])
  })
  for i in range(len(busy_slots)-1):
    if parse_time(busy_slots[i+1]["start"])>deadline or parse_time(busy_slots[i]["end"])>deadline:
      break
    free_slots.append({
      'time':parse_time(busy_slots[i+1]["start"])-parse_time(busy_slots[i]["end"]),
      'start': parse_time(busy_slots[i]["end"]),
      'end': parse_time(busy_slots[i+1]["start"])
    })
  if parse_time(busy_slots[-1]["end"])<deadline:
    free_slots.append({
      'time':deadline-parse_time(busy_slots[-1]["end"]),
      'start':parse_time(busy_slots[-1]["end"]),
      'end': deadline
    })
  return free_slots