#!/usr/bin/env python
import uvicorn

from app.settings import APP

if __name__ == "__main__":

    uvicorn.run(
        'app.fastapi_app:app',
        proxy_headers=True,
        forwarded_allow_ips=APP.ALLOW_ORIGINS,
        host=str(APP.HOST.ip),
        port=APP.PORT,
        reload=True,
    )
