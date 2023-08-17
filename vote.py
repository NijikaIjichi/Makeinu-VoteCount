import asyncio, aiotieba, datetime, re
from collections import defaultdict
from typing import List

START     = datetime.datetime(2023, 8, 18).timestamp()
END       = datetime.datetime(2023, 8, 18, 23).timestamp()
TID       = 8556607638
MAX       = 1
FILE      = 'lst.txt'
SLEEP     = 0.01

PATTERN   = "(?<=\[)+[^\[\]]+?(?=[\[\]<])"
FLAG      = re.I | re.M

groups    = [set()]
votes     = defaultdict(int)
last_time = defaultdict(int)
voter     = set()
post_list: List[aiotieba.typing.Post] = []


def read_groups():
  with open(FILE, encoding='utf-8') as fp:
    for line in fp:
      if s := re.search(PATTERN, line, FLAG):
        groups[-1].add(s[0])
      elif groups[-1]:
        groups.append(set())


def parse_vote(s, t):
  vote = set(re.findall(PATTERN, s, FLAG))
  if not vote or any(len(vote & g) > MAX for g in groups):
    return False
  for v in vote:
    votes[v] += 1
    last_time[v] = t
  return True


def analyse_votes():
  for post in post_list:
    if post.create_time < START or post.create_time > END:
      continue
    user = post.user
    if user.user_id not in voter and user.level >= 9 \
        and parse_vote(post.text, post.create_time):
      voter.add(user.user_id)


async def get_votes():
  pn, last = 1, -1
  async with aiotieba.Client() as client:
    while True:
      posts = await client.get_posts(TID, pn=pn, comment_rn=0)
      if not posts or last == posts[0].floor:
        return
      last = posts[0].floor
      post_list.extend(posts)
      await asyncio.sleep(SLEEP)
      pn += 1


def show_result():
  voter_num = len(voter)
  print("Voter:", voter_num)
  for i, g in enumerate(groups, 1):
    result = sorted([(x, votes[x]) for x in g], key=lambda t: (-t[1], last_time[t[0]]))
    print("Group", i, "Total:", sum(v for _, v in result))
    for j, (x, v) in enumerate(result, 1):
      print(j, x, v, f'{round(v / voter_num * 100, 2)}%')


if __name__ == '__main__':
  read_groups()
  asyncio.run(get_votes())
  analyse_votes()
  show_result()
