# Local AI-Powered Code Review Tool

FastAPI service that uses Ollama to review code snippets locally.

Testing (#Phase 1):

- Run the app: uvicorn main:app --reload
- Open browser to http://127.0.0.1:8000/ → Should see JSON: {"message": "Welcome to the Local AI Code 
Reviewer! Use POST /review to submit code."}
- Check docs: http://127.0.0.1:8000/docs → Swagger UI loads with the app title/description and a GET / endpoint.

Testing (#Phase 2):

- Ensure Ollama model is pulled: ollama pull deepseek-coder-v2
- Run Ollama: ollama serve
- Run app: uvicorn main:app --reload
- Browser: http://127.0.0.1:8000/docs → See new POST /review endpoint.

- Try it in Swagger: Input code like print("hello"), language python, model deepseek-coder-v2. Should    return a JSON review. If model missing, error in logs.

### Issues 

<pre>

System Freeze

Ollama got hung up! Had to kill the ollama running process.

MacBook-Air:fastapi-pydantic-projects anish$ ps aux  |grep uvicorn
anish            46876   0.0  0.0 408646352   1600 s000  S+    3:33AM   0:00.00 grep uvicorn
MacBook-Air:fastapi-pydantic-projects anish$ ps aux | grep ollam
anish            42395  18.6  0.0 418106400   2128   ??  U     3:19AM   4:12.87 /Applications/Ollama.app/Contents/Resources/ollama runner --model /Users/anish/.ollama/models/blobs/sha256-ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373 --ctx-size 4096 --batch-size 512 --n-gpu-layers 31 --threads 4 --no-mmap --parallel 1 --port 52433
anish            35140   0.0  0.0 408678800    640   ??  S<    3:06AM   0:00.03 /Applications/Ollama.app/Contents/Frameworks/Squirrel.framework/Resources/ShipIt com.electron.ollama.ShipIt /Users/anish/Library/Caches/com.electron.ollama.ShipIt/ShipItState.plist
anish              821   0.0  0.0 409888656   1280   ??  S     2:06AM   3:50.76 /Applications/Ollama.app/Contents/Resources/ollama serve
anish            46899   0.0  0.0 408626896   1328 s000  S+    3:34AM   0:00.00 grep ollam
</pre>
