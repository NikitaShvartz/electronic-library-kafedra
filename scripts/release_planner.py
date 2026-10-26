#!/usr/bin/env python3
"""Solve the MVP release-selection problem without third-party dependencies."""
from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def load_problem():
    config=json.loads((DATA/'project_config.json').read_text(encoding='utf-8'))
    with (DATA/'stories.csv').open(encoding='utf-8-sig',newline='') as f: stories=list(csv.DictReader(f))
    for s in stories:
        for k in ('story_points','uv','time_criticality','risk_reduction','cost_of_delay','mandatory'): s[k]=int(float(s[k]))
        s['wsjf']=float(s['wsjf'])
    deps={}
    with (DATA/'dependencies.csv').open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f): deps.setdefault(r['story_id'],[]).append(r['depends_on'])
    return config,stories,deps
def valid(selected,config,stories,deps):
    by={s['id']:s for s in stories}
    if len(selected)>config['max_mvp_stories']: return False
    if sum(by[i]['story_points'] for i in selected)>config['release_capacity_story_points']: return False
    if not set(config['mandatory_story_ids']).issubset(selected): return False
    return all(set(deps.get(i,[])).issubset(selected) for i in selected)
def score(selected,by): return sum(by[i]['cost_of_delay'] for i in selected)
def solve_exact(config,stories,deps):
    by={s['id']:s for s in stories}; mandatory=set(config['mandatory_story_ids'])
    optional=[s['id'] for s in stories if s['id'] not in mandatory]; best=None
    for mask in range(1<<len(optional)):
        chosen=set(mandatory)
        for j,sid in enumerate(optional):
            if mask&(1<<j): chosen.add(sid)
        if not valid(chosen,config,stories,deps): continue
        key=(score(chosen,by),-sum(by[i]['story_points'] for i in chosen),tuple(sorted(chosen)))
        if best is None or key>best[0]: best=(key,chosen)
    if best is None: raise RuntimeError('No feasible release; check mandatory stories and capacity.')
    return best[1]
def solve_greedy(config,stories,deps):
    by={s['id']:s for s in stories}; chosen=set(config['mandatory_story_ids'])
    optional=[s for s in stories if s['id'] not in chosen]
    optional.sort(key=lambda s:(-s['wsjf'],-s['cost_of_delay'],s['story_points'],s['id']))
    for s in optional:
        candidate=chosen|{s['id']}
        if valid(candidate,config,stories,deps): chosen=candidate
    return chosen
def main():
    config,stories,deps=load_problem(); by={s['id']:s for s in stories}
    exact=solve_exact(config,stories,deps); greedy=solve_greedy(config,stories,deps)
    print(f"Capacity: {config['release_capacity_story_points']} SP; maximum stories: {config['max_mvp_stories']}")
    for name,chosen in [('Exact knapsack',exact),('Greedy WSJF',greedy)]:
        pts=sum(by[i]['story_points'] for i in chosen); cod=score(chosen,by)
        print(f"{name}: {len(chosen)} stories, {pts} SP, Cost of Delay={cod}")
        print('  '+', '.join(sorted(chosen)))
    with (DATA/'release_selection.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','title','story_points','cost_of_delay','wsjf','mandatory','exact_knapsack','greedy_wsjf']); w.writeheader()
        for s in stories:
            w.writerow({'id':s['id'],'title':s['title'],'story_points':s['story_points'],'cost_of_delay':s['cost_of_delay'],'wsjf':f"{s['wsjf']:.2f}",'mandatory':'yes' if s['mandatory'] else 'no','exact_knapsack':'yes' if s['id'] in exact else 'no','greedy_wsjf':'yes' if s['id'] in greedy else 'no'})
    print(f"Saved: {DATA/'release_selection.csv'}")
if __name__=='__main__': main()
