import hashlib #파이썬에서 제공하는 암호화 전문 도구함을 가져오는 것
def hash_pw(pw):
    #이 함수는 원본 비밀번호를 아무도 알아볼 수 없는 '해시값'으로 변환
    """
    :param pw: 비밀번호
    :return: SHA-256 알고리즘으로 단방향암호화
    """
    # encode:문자열을 바이트로, sha256:해시생성, hexdigest:16진수문자열로 리턴
    return hashlib.sha256(pw.encode()).hexdigest()
def check_pw(input_pw, stored_hash):
    """
    :param input_pw:입력 pw
    :param stored_hash: :암호화pw
    :return: bool
    """
    input_hash = hash_pw(input_pw)
    return input_hash == stored_hash
if __name__ == '__main__':
    print("=1.암호화테스트=")
    my_pass = "pass1234"
    print(f"원본:{my_pass}")
    hash = hash_pw(my_pass)
    print(f"암호화된:{hash}")
    input_msg=input("pw 입력하세요!")
    if check_pw(input_msg, hash):
        print("로그인 성공!")
    else:
        print("로그인 실패!")
