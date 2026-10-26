#!/usr/bin/env python3
"""Bootstrap a throughput-based Monte Carlo forecast."""
from pathlib import Path
from datetime import date,timedelta
import csv,json,math,random,statistics
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def percentile(values,p): return values[max(0,math.ceil(p*len(values))-1)]
def main():
    config=json.loads((DATA/'project_config.json').read_text(encoding='utf-8'))
    with (DATA/'stories.csv').open(encoding='utf-8-sig',newline='') as f: stories=list(csv.DictReader(f))
    count=sum(1 for s in stories if s['in_mvp']=='1')
    with (DATA/'throughput_history.csv').open(encoding='utf-8-sig',newline='') as f: history=[int(r['completed_stories']) for r in csv.DictReader(f)]
    if not history or any(x<1 for x in history): raise ValueError('Throughput history must contain positive counts.')
    rng=random.Random(config['random_seed']); n=config['throughput_simulations']; durations=[]
    for _ in range(n):
        remaining=count; weeks=0
        while remaining>0: remaining-=rng.choice(history); weeks+=1
        durations.append(weeks)
    durations.sort(); p50,p85,p95=(percentile(durations,p) for p in (.50,.85,.95)); start=date.fromisoformat(config['start_date'])
    summary=[('stories_in_mvp',count,''),('simulation_count',n,''),('mean_weeks',f'{statistics.mean(durations):.2f}',''),('P50_weeks',p50,(start+timedelta(weeks=p50)).isoformat()),('P85_weeks',p85,(start+timedelta(weeks=p85)).isoformat()),('P95_weeks',p95,(start+timedelta(weeks=p95)).isoformat())]
    with (DATA/'monte_carlo_summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['metric','value','forecast_date']); w.writerows(summary)
    with (DATA/'monte_carlo_distribution.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['weeks_to_complete','simulations','probability'])
        for weeks in sorted(set(durations)):
            nweek=durations.count(weeks); w.writerow([weeks,nweek,f'{nweek/len(durations):.5f}'])
    print(f'MVP stories: {count}; simulations: {n}; mean: {statistics.mean(durations):.2f} weeks')
    print(f'P50: {p50} weeks -> {(start+timedelta(weeks=p50)).isoformat()}')
    print(f'P85: {p85} weeks -> {(start+timedelta(weeks=p85)).isoformat()}')
    print(f'P95: {p95} weeks -> {(start+timedelta(weeks=p95)).isoformat()}')
    print(f'Saved: {DATA/"monte_carlo_summary.csv"}'); print(f'Saved: {DATA/"monte_carlo_distribution.csv"}')
if __name__=='__main__': main()
