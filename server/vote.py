import asyncio, aiotieba, datetime, re, time, json
from collections import defaultdict
from typing import List

START     = datetime.datetime(2023, 8, 27).timestamp()
END       = datetime.datetime(2023, 8, 27, 23).timestamp()
TID       = 8571325172
MAX       = 1
FILE      = 'lst.txt'
RES       = 'result.json'
SLEEP     = 0.01
CUT       = 120

BDUSS     = None

PATTERN   = "(?<=\[)+[^\[\]]+?(?=[\[\]<])"
FLAG      = re.I | re.M

groups    = [set()]
votes     = defaultdict(int)
last_time = defaultdict(int)
voter     = set()
floor     = set()
post_list: List[aiotieba.typing.Post] = []
start     = time.time()


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
    if user.user_id not in voter and post.floor not in floor and user.level >= 9 \
        and parse_vote(post.text, post.create_time):
      voter.add(user.user_id)
      floor.add(post.floor)


async def get_votes():
  pn = 1
  async with aiotieba.Client(BDUSS) as client:
    while True:
      while not (posts := await client.get_posts(TID, pn=pn, comment_rn=0)):
        await asyncio.sleep(SLEEP * 10)
        if time.time() - start > CUT:
          return
      post_list.extend(posts)
      if posts[-1].create_time > END or not posts.has_more:
        return
      await asyncio.sleep(SLEEP)
      pn += 1


def show_result():
  voter_num = len(voter)
  data = {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(post_list[-1].create_time if post_list else START)), 'voter': voter_num, 'votes': []}
  #print("Voter:", voter_num)
  for i, g in enumerate(groups, 1):
    result = sorted([(x, votes[x]) for x in g], key=lambda t: (-t[1], last_time[t[0]]))
    #print("Group", i, "Total:", sum(v for _, v in result))
    for j, (x, v) in enumerate(result, 1):
      rate = round(v / voter_num * 100, 2) if voter_num else 0.0
      #print(j, x, v, f'{rate}%')
      data['votes'].append({'group': i, 'rank': j, 'name': x, 'vote': v, 'rate': rate})
  return data


if __name__ == '__main__':
  start = time.time()
  read_groups()
  asyncio.run(get_votes())
  analyse_votes()
  data = show_result()
  if time.time() - start < CUT:
    with open('result.json', 'w', encoding='utf-8') as fp:
      json.dump(data, fp, ensure_ascii=False)
