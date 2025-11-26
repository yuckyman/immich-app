# sorter

minimal photo/video review tool for immich.

## features

- **lazy queue** — preloads images ahead, instant switching
- **progressive loading** — thumbnail first, full res in background
- **video support** — inline playback with duration badge
- **metadata sidebar** — date, size, dims, camera, lens, exif data, location
- **logging** — track all actions and api calls
- **ascii-minimal ui** — jade green monochrome terminal aesthetic

## setup

```bash
pip install -r requirements.txt
```

copy `.env.example` to `.env.local` and add your credentials:
```bash
cp .env.example .env.local
```

```env
IMMICH_URL=http://your-immich-host:2283/api
IMMICH_API_KEY=your-api-key-here
```

run:
```bash
uvicorn backend.main:app --reload --port 8000
```

open `http://localhost:8000`

## controls

```
[←]        del      delete asset
[→]        skip     keep, move to next
[↑]        fav      mark as favorite
[↓]        archive  archive asset
[ctrl+z]   undo     undo last action
```

## logs

```bash
./monitor.sh
# or
tail -f logs/app_$(date +%Y%m%d).log
```

logs include: api requests, user actions, errors, asset types.

## ideas

- [x] undo last action
- [ ] stats counter (deleted/kept/fav'd)
- [ ] filter by date range or camera
- [ ] batch mode (grid selection)
- [ ] theme toggle
