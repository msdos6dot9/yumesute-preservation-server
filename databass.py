"""Explicit, local-only setup and account management for the release."""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
VENDOR=ROOT/'vendor/server-of-dreams'
PRIVATE=ROOT/'private'
PIN=json.loads((ROOT/'upstream-versions.json').read_text())['server-of-dreams']

def bootstrap():
    if not VENDOR.exists():
        VENDOR.parent.mkdir(exist_ok=True)
        subprocess.run(['git','clone','https://github.com/UnknownSekai/server-of-dreams.git',str(VENDOR)],check=True)
        subprocess.run(['git','-C',str(VENDOR),'checkout','--detach',PIN],check=True)
    actual=subprocess.check_output(['git','-C',str(VENDOR),'rev-parse','HEAD'],text=True).strip()
    if actual!=PIN: raise RuntimeError('Unexpected upstream revision; use a clean release folder')
    sys.path.insert(0,str(VENDOR));sys.path.insert(0,str(ROOT/'tools'))

def prepare(a):
    source=Path(a.db_file).expanduser().resolve()
    if not source.is_file(): raise RuntimeError(f'Database file not found: {source}')
    bootstrap()
    from helpers.mastermemory import unpack
    from helpers.msgpack import from_array
    from models.master_data import TABLES
    tables=unpack(source.read_bytes())
    output=PRIVATE/'dataoutput/_data/masterdata';output.mkdir(parents=True,exist_ok=True)
    for name, rows in tables.items():
        print(f'name: {name}, rows: ({len(rows)}) rows')
        if name in TABLES:
            decoded=[from_array(TABLES[name].__name__,r).model_dump(mode='json',by_alias=True) for r in rows]
            (output/(name+'.json')).write_text(json.dumps(decoded,ensure_ascii=False),encoding='utf-8')
    print('unpack complete')

def unprepare(a):
    bootstrap()
    source=Path(a.data_dir).expanduser().resolve()
    if not source.is_dir(): raise RuntimeError(f'Master data directory not found: {source}')
    from helpers.mastermemory import pack
    from helpers.msgpack import to_wire
    from models.master_data import TABLES
    files=sorted(source.glob('*.json'))
    if not files: raise RuntimeError(f'No JSON table files found in: {source}')
    tables={}
    for path in files:
        if path.stem.endswith('_bak'):
            print(f'Skip backup file: {path.name}')
            continue
        model=TABLES.get(path.stem)
        if model is None: raise RuntimeError(f'Unknown master table JSON file: {path.name}')
        rows=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(rows,list): raise RuntimeError(f'{path.name} must contain a JSON array of rows')
        try:
            tables[path.stem]=[to_wire(model.model_validate(row)) for row in rows]
        except Exception as exc:
            raise RuntimeError(f'Invalid row in {path.name}: {exc}') from exc
    if not tables: raise RuntimeError(f'No recognized master table JSON files found in: {source}')

    output=Path(a.output_db_file).expanduser().resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    temp_path=None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent,prefix=output.name+'.',suffix='.tmp',delete=False) as temp:
            temp_path=Path(temp.name)
            temp.write(pack(tables))
        temp_path.replace(output)
    finally:
        if temp_path is not None: temp_path.unlink(missing_ok=True)
    print(f'Packed {len(tables)} tables into {output}')


def main():
    os.chdir(ROOT);os.umask(0o077)
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('--db-file',required=True)
    p=sub.add_parser('unprepare');p.add_argument('--data-dir',required=True);p.add_argument('--output-db-file',required=True)
    a=parser.parse_args();PRIVATE.mkdir(exist_ok=True,mode=0o700)
    if a.command=='prepare':prepare(a)
    elif a.command=='unprepare':unprepare(a)

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:print('Stopped. Turn off the device WireGuard tunnel.')
    except Exception as e:
        print(f'Stopped: {type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
