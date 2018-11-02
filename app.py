# -*- coding: utf-8 -*-
"""
部署启动文件
"""
from app import create_app

app = create_app()

def main():
    app.run(port=5210, debug=False)

if __name__ == '__main__':
    main()