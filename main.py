import uvicorn
import os

os.environ['Local'] = 'True'

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host='localhost',
        # host='0.0.0.0',
        port=8000,
        reload=True,
    )
