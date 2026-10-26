#!/usr/bin/env python3
"""PERT/CPM for the exact selected MVP; writes CSV and dependency graph SVG."""
from pathlib import Path
import csv, math, html
from release_planner import load_problem, solve_exact
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DOCS=ROOT/'docs'/'01-planning'
def main():
    config,stories,all_deps=load_problem(); selected=solve_exact(config,stories,all_deps); by={s['id']:s for s in stories}
    deps={sid:[d for d in all_deps.get(sid,[]) if d in selected] for sid in selected}; succ={sid:[] for sid in selected}
    for sid,ds in deps.items():
        for d in ds: succ[d].append(sid)
    duration={sid:(int(by[sid]['o_hours'])+4*int(by[sid]['m_hours'])+int(by[sid]['p_hours']))/6 for sid in selected}
    sd={sid:(int(by[sid]['p_hours'])-int(by[sid]['o_hours']))/6 for sid in selected}
    indegree={sid:len(deps[sid]) for sid in selected}; queue=sorted([sid for sid in selected if indegree[sid]==0]); order=[]
    while queue:
        sid=queue.pop(0); order.append(sid)
        for nxt in sorted(succ[sid]):
            indegree[nxt]-=1
            if indegree[nxt]==0: queue.append(nxt); queue.sort()
    if len(order)!=len(selected): raise RuntimeError('Dependency cycle detected.')
    es={}; ef={}; pred={}
    for sid in order:
        if deps[sid]:
            p=max(deps[sid],key=lambda d:ef[d]); pred[sid]=p; es[sid]=ef[p]
        else: pred[sid]=None; es[sid]=0.0
        ef[sid]=es[sid]+duration[sid]
    project_duration=max(ef.values()); terminal=max(selected,key=lambda sid:ef[sid]); path=[]; cur=terminal
    while cur: path.append(cur); cur=pred[cur]
    path.reverse(); critical=set(path)
    lf={}; ls={}
    for sid in reversed(order):
        lf[sid]=min([ls[n] for n in succ[sid]] or [project_duration]); ls[sid]=lf[sid]-duration[sid]
    slack={sid:ls[sid]-es[sid] for sid in selected}
    total=sum(duration.values()); total_sd=math.sqrt(sum(sd[sid]**2 for sid in selected))
    available=config['weeks_available']*config['hours_per_person_per_week']*config['team_size']*config['focus_factor']
    z=(available-total)/total_sd; probability=.5*(1+math.erf(z/math.sqrt(2)))
    cp_sd=math.sqrt(sum(sd[sid]**2 for sid in path))
    with (DATA/'cpm_results.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','title','story_points','pert_expected_hours','pert_sd_hours','dependencies','early_start_hours','early_finish_hours','late_start_hours','late_finish_hours','slack_hours','critical_path']); w.writeheader()
        for sid in order:
            w.writerow({'id':sid,'title':by[sid]['title'],'story_points':by[sid]['story_points'],'pert_expected_hours':f'{duration[sid]:.2f}','pert_sd_hours':f'{sd[sid]:.2f}','dependencies':','.join(deps[sid]),'early_start_hours':f'{es[sid]:.2f}','early_finish_hours':f'{ef[sid]:.2f}','late_start_hours':f'{ls[sid]:.2f}','late_finish_hours':f'{lf[sid]:.2f}','slack_hours':f'{max(0,slack[sid]):.2f}','critical_path':'yes' if sid in critical else 'no'})
    # SVG: dependency depth sets columns; thicker boxes/edges show the critical path.
    level={}
    for sid in order: level[sid]=0 if not deps[sid] else max(level[d] for d in deps[sid])+1
    columns={}
    for sid in sorted(selected): columns.setdefault(level[sid],[]).append(sid)
    node_w,node_h,col_gap,row_gap=190,66,245,112; margin_x,margin_y=35,55
    max_rows=max(len(v) for v in columns.values()); width=margin_x*2+(max(columns)+1)*col_gap+node_w; height=margin_y*2+max_rows*row_gap+35
    pos={}
    for lev,ids in columns.items():
        ids.sort()
        for idx,sid in enumerate(ids): pos[sid]=(margin_x+lev*col_gap,margin_y+idx*row_gap)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#222"/></marker></defs>','<rect width="100%" height="100%" fill="white"/>','<text x="25" y="25" font-size="17" font-family="Arial, sans-serif" font-weight="bold">Сетевой график MVP · толстая рамка/связь = критический путь</text>']
    for sid in sorted(selected):
        x1,y1=pos[sid]
        for dep in deps[sid]:
            x0,y0=pos[dep]; xstart=x0+node_w; ystart=y0+node_h/2; xend=x1; yend=y1+node_h/2; mid=(xstart+xend)/2
            iscp=dep in critical and sid in critical and path.index(sid)==path.index(dep)+1; sw=3.5 if iscp else 1.5
            svg.append(f'<path d="M {xstart} {ystart} C {mid} {ystart}, {mid} {yend}, {xend} {yend}" fill="none" stroke="#222" stroke-width="{sw}" marker-end="url(#arrow)"/>')
    for sid in sorted(selected):
        x,y=pos[sid]; s=by[sid]; sw=3.5 if sid in critical else 1.5
        svg.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="7" fill="white" stroke="#222" stroke-width="{sw}"/>')
        label=html.escape(f"{sid} · {s['title']}"); lines=[label]
        if len(label)>25:
            split=label.rfind(' ',0,27)
            if split>8: lines=[label[:split],label[split+1:]]
        yy=y+22
        for line in lines[:2]: svg.append(f'<text x="{x+9}" y="{yy}" font-size="11.5" font-family="Arial, sans-serif">{line}</text>'); yy+=14
        svg.append(f'<text x="{x+9}" y="{y+node_h-7}" font-size="11" font-family="Arial, sans-serif">E={duration[sid]:.2f} ч · {s["story_points"]} SP</text>')
    svg.append('</svg>'); (DOCS/'network.svg').write_text('\n'.join(svg),encoding='utf-8')
    print('MVP:',', '.join(sorted(selected))); print('Critical path:',' -> '.join(path))
    print(f'Critical-path expected duration: {project_duration:.2f} h; SD on path: {cp_sd:.2f} h')
    print(f'Total expected effort: {total:.2f} h; SD total: {total_sd:.2f} h')
    print(f'Available focused team effort: {available:.2f} h; z={z:.2f}; PERT probability≈{probability*100:.1f}%')
    print(f'Saved: {DATA/"cpm_results.csv"}'); print(f'Saved: {DOCS/"network.svg"}')
if __name__=='__main__': main()
