from pprint import pprint
from os import getcwd

print(getcwd())

with open('todo.txt', 'r') as f:
  tasks = f.readlines()

tasks = [t for t in tasks if t.strip() != ""] # removes blank lines

done_tasks = [t for t in tasks if t.startswith("x =")]
tasks = [t for t in tasks if not t.startswith("x =")]
with open('done.txt', 'a') as f:
  f.write(''.join(done_tasks))

def sort_tasks(tasks, char): # char is either @ or +
  sorted_tasks = {}
  for t in tasks:
    proj_or_context_list = []
    words = t.split()
    for w in words:
      if w.startswith(char) and len(w) != 1:
        proj_or_context_list.append(w)
    
    special_proj_or_context_list = tuple(filter(lambda x: x.startswith('+_'), proj_or_context_list))
    if special_proj_or_context_list != ():
      if "+_done" in proj_or_context_list:
        proj_or_context = "+_done"
      elif "+_failed" in proj_or_context_list:
        proj_or_context = "+_failed"
      else:
        proj_or_context = special_proj_or_context_list[0]
    else:
      proj_or_context = '' if proj_or_context_list == [] else proj_or_context_list[0]

    if proj_or_context not in sorted_tasks:
      sorted_tasks[proj_or_context] = []
    sorted_tasks[proj_or_context].append(t)

  return sorted_tasks

def sort_by_priority(tasks):
  with_deadlines = []
  with_letters = []
  finished = []
  others = []
  for t in tasks:
    if t[0:2] == "x ":
      finished.append(t)
    elif " due:" in t:
      with_deadlines.append(t)
    elif t[0] == '(' and t[2] == ')':
      with_letters.append(t)
    else:
      others.append(t)

  with_letters.sort(key=lambda x: x[1])

  def get_date(task):
    return [w for w in task.split() if w.startswith('due:')][0][4:]
  with_deadlines.sort(key=get_date)

  return with_deadlines + with_letters + others + finished

sorted_by_proj = sort_tasks(tasks, "+")

full_sorted = {}
project_names = sorted(sorted_by_proj.keys(), key=str.lower)
print(project_names)
for proj in project_names:
  sorted_by_context = sort_tasks(sorted_by_proj[proj], '@')
  for context in sorted_by_context.keys():
    sorted_by_context[context] = sort_by_priority(sorted_by_context[context])
  full_sorted[proj] = sorted_by_context

# pprint(full_sorted)

new_file = ""
for proj in project_names:
  new_file += """
x ================================================================================
x = {}
x ================================================================================\n""".format(proj.upper().replace('+', ''))

  contexts = sorted(full_sorted[proj].keys())
  for c in contexts:
    new_file += "".join(full_sorted[proj][c]) + "\n\n"

with open('todo.txt', 'w') as f:
  f.write(new_file)
