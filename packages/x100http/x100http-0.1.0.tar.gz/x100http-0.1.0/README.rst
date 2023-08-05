NAME
====

x100http - WebFramework support customing file upload processing


SYNOPSIS
========

.. code:: python

    from x100http import X100HTTP

    app = X100HTTP()

    def get_test(req):
        body = req['body']
        abc = req['args']['abc']
        remote_ip = req['remote_ip']

        response = "<html><body>get test succ <br/>" \
            + "body:[" + body + "]<br/>" \
            + "args:[" + abc + "]<br/>" \
            + "ip:[" + remote_ip + "]" \
            + "</body></html>"
        return response


    def post_test(req):
        body = req['body']
        abc = req['args']['abc']
        remote_ip = req['remote_ip']

        response = "<html><body>post test succ <br/>" \
            + "body:[" + body + "]<br/>" \
            + "args:[" + abc + "]<br/>" \
            + "ip:[" + remote_ip + "]" \
            + "</body></html>"
        return response

    def upload_test_init(req):
        print(req['remote_ip'])
        return

    def upload_test_ing(key, body):
        print(key)
        print("write")
        return

    def upload_test_del(req):
        return req['remote_ip']

    app.set_upload_buf_size(8192)
    app.get("/get", get_test)
    app.post("/post", post_test)
    app.upload("/upload", upload_test_init, upload_test_ing, upload_test_del)

    app.run("127.0.0.1", 4321)
     


DESCRIPTION
===========

x100http is a webframework helps you customing HTTP file upload processing.


