import time

hiredate= '1981-06-03'
pattern = '%Y-%m-%d'
epoch = float(time.mktime(time.strptime(hiredate, pattern)))
print epoch