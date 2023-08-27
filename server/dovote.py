import time
import os

def main():
  last = time.localtime()
  while True:
    curr = time.localtime()
    if curr.tm_hour != last.tm_hour or curr.tm_min != last.tm_min:
      last = curr
      if (curr.tm_hour == 0 and (
        curr.tm_min in [1, 3, 5] or
        (5 < curr.tm_min <= 30 and curr.tm_min % 5 in [0, 2]) or
        curr.tm_min % 5 == 0
      )) or (
        1 <= curr.tm_hour <= 2 and curr.tm_min % 10 == 0
      ) or (
        3 <= curr.tm_hour <= 19 and curr.tm_min % 15 == 0
      ) or (
        20 <= curr.tm_hour <= 21 and curr.tm_min % 10 == 0
      ) or (
        curr.tm_hour == 22 and curr.tm_min % 5 == 0
      ) or (
        curr.tm_hour == 23 and curr.tm_min == 0
      ):
        os.system('python3 vote.py')
    time.sleep(1)

if __name__ == "__main__":
  main()
