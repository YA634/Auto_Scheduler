from .models import Task
from datetime import datetime, timezone, timedelta

def parse_time(time_str):
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

def get_free_slots(busy_slots, deadline):
  free_slots = []#予定の入っていない時間(辞書)のリスト
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

def assign_task_to_slots(free_slots, task_hours):
  # remaining = timedelta(hours=task_hours)
  remaining = task_hours
  new_slots=[]
  for i in range(len(free_slots)):
    if free_slots[i]["time"]>remaining:
      new_slots.append({"time":remaining,"start":free_slots[i]["start"],"end":free_slots[i]["start"]+remaining})
      break
    else:
      new_slots.append({"time":free_slots[i]["time"],"start":free_slots[i]["start"],"end":free_slots[i]["end"]})
      remaining-=free_slots[i]["time"]
  return new_slots

def schedule_task(task, busy_slots):
  free_slots = get_free_slots(busy_slots, task.deadline)
  new_slots = assign_task_to_slots(free_slots, task.quote_time)
  return new_slots