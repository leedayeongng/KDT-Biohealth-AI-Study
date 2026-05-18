import logging

def make_logger(file_nm, name='log'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        #level 설정
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #콘솔 출력 설정
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        logger.addHandler(console)
        #파일
        file_handler = logging.FileHandler(filename=file_nm, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
if __name__ == '__main__':
    log = make_logger('test.log', 'test')
    log.debug('디버그 메세지!!')
    log.info('정보 메세지!!')
    log.error('오류 발생 !!')
    log.critical('심각..bye...')