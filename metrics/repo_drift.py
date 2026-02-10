import os, json

STATE_FILE = os.path.join('runs','_watch_state.json')

def _load():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE,'r',encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def _save(d):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE,'w',encoding='utf-8') as f:
        json.dump(d,f,indent=2)

def drift_for_repo(name, new_fp):
    st = _load()
    old = st.get(name)
    st[name] = new_fp
    _save(st)
    if old is None:
        return 0.0
    return 0.0 if old == new_fp else 1.0
