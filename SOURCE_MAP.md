# Original `restrict_bot.py` source map

Every original Python source line is accounted for below. The dashboard string payload is moved verbatim to `web/templates/dashboard.html`.

- `1-156` → `main.py` bootstrap
- `157-292` → `config.py`
- `293-606` → `database/mongo.py`
- `609-844` → `main.py` client/global state
- `846-1230` and `1327-1425` → `bot/utils.py`
- `1231-1325` → `media/editor.py`
- `1426-1676`, `2053-2392`, `2727-3586` → `bot/plugins/downloader.py`
- `1677-2052`, `2393-2472`, `14527-14942`, `15109-15217` → `bot/plugins/admin.py`
- `2473-2726` → `bot/plugins/watchers.py`
- `3587-4202` → `core/batch_engine.py`
- `4203-4903` → `core/router.py`
- `4904-4911`, `10563-11711`, `13877-14526` → `web/server.py`
- `4912-10562` → `web/templates/dashboard.html` payload + original triple-quote delimiters; `web/server.py` replaces the Python assignment with a file read
- `11712-12245` → `streaming/direct_stream.py`
- `12246-12759` → `media/probe.py`
- `12760-13074` → `media/transcode.py`
- `13075-13609` → `streaming/tg_stream.py`
- `13610-13876` → `streaming/zip_engine.py`
- `14943-15108` → `media/dsp_analyzer.py`
- `15218-15573` → `core/live_engine.py`
- `15574-15827` → `main.py` main entry / startup

Lines `607-608`, `845`, and `1326` are original blank/separator lines and are intentionally not emitted as standalone content.
