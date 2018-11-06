# -*- coding: utf-8 -*-
"""
部署启动文件
"""
from app.main import create_app

app = create_app()

def main():
    app.run(host='0.0.0.0', port=5210, debug=False)

if __name__ == '__main__':
    main()