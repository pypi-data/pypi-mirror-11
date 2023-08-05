About(关于)
============

该包主要是解析迅雷URL中的地址为真实地址。使用方法如下::

    from ThunderParser.parser_thunder import parser
    url = 'The download url of thunder' #迅雷的下载地址
    print parser(url)                             # 获取到真实资源地址
