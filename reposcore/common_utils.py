import sys
import logging

# logging 모듈 기본 설정 (analyzer.py와 동일한 설정)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
