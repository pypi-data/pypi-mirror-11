impay 본인인증
~~~~~~~~~~~~~~

    from impayident import env

    env.CPCODE = ''  # CP code 등등 설정

    ...

    
    from impayident import cert, bill

    response = cert(CPCODE='', ...)  # 매뉴얼 참고
   
    response.RESULT == '0000' # 매뉴얼 상의 응답 값을 가진 namedtuple

    response = bill(CPCODE='', ...)  # 매뉴얼 참고

    response.RESULT == '0000' # 매뉴얼 상의 응답 값을 가진 namedtuple

