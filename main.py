#!/usr/bin/env python
import uvicorn

from airflow.settings import APP

if __name__ == "__main__":

    uvicorn.run(
        'airflow.app:app',
        proxy_headers=True,
        forwarded_allow_ips=APP.ALLOW_ORIGINS,
        host=str(APP.HOST.ip),
        port=APP.PORT,
        reload=True,
    )
