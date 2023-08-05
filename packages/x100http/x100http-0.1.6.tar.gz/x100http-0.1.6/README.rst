NAME
====

    x100http - WebFramework support customing file upload processing



SYNOPSIS
========

.. code-block:: python
    :linenos:


    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(req):
        remote_ip = req['remote_ip']
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)



DESCRIPTION
===========

    x100http is a webframework helps you customing HTTP file upload processing.



METHODS
=======

    X100HTTP()
    ----------
    return a instance of x100http which wrapped below functions.


    run(listern_ip, listen_port)
    ----------------------------
    run a forking server on address ``listern_ip``:``listern_port``


    get(url, handler_function)
    --------------------------
    set a route acl of HTTP "GET" method.

    ``handler_function`` will be called when ``url`` be visited.

    ``handler_function`` must return a string as the HTTP response body to the visitor.

    struct ``request`` (will explain below) will be passed to the handlder function when it is called.


    post(url, handler_function)
    ---------------------------
    set a route acl of HTTP "POST" method with header "Content-Type: application/x-www-form-urlencoded".

    ``handler_function`` will be called when HTTP client submit a form with the action ``url``.

    ``handler_function`` must return a string as the HTTP response body to the visitor.

    struct ``request`` (will explain below) will be passed to the handlder function when it is called.


    upload(url, handler_function_init, handler_function_process, handler_function_del)
    ----------------------------------------------------------------------------------
    set a route acl of HTTP "POST" method with header "Content-Type: multipart/form-data".

    ``handler_function_init`` will be called when file upload start.

    struct "request" (will explain below) will be passed to ``handler_function_init``.

    ``handler_function_process`` will be called every time when the buffer is full when file uploading.

    two args will be passed to ``handler_function_process``.

    first arg is the name of the input in the form, second arg is the content of the input in the form.

    the binary content of the upload file will be passed by the second arg.

    struct "request" (will explain below) will NOT be passed to ``handler_function_process``.

    ``handler_function_del`` will be called when file upload finished, this function must return a string as the HTTP response body to the visitor.

    struct "request" (will explain below) will be passed to ``handler_function_del``.


    set_upload_buf_size(buf_size)
    -----------------------------
    set the buffer size of the stream reader while file uploading.

    the unit of ``buf_size`` is byte, default value is 4096 byte.

    ``handler_function_process`` will be called to process the buffer every time when the buffer is full.



STRUCT REQUEST
==============

    ``request`` will be passed into the handler function you set, you can use these informations in your app logic.

    ``request`` is a dictionary filled with key-values below.

    remote_ip
    ---------
    The IP address of the visitor.


    body
    ----
    The body part of the HTTP request.

    ``body`` is a empty string when the request is sent by HTTP method "GET" or "POST - multipart/form-data".


    query_string
    ------------
    The query string, if any, via which the page was accessed.


    args
    ----
    A dictionary of variables passed to the handler function via the URL parameters.

    ``args`` parse from ``query_string`` when the request is sent by HTTP method "GET" or "POST - multipart/form-data".

    ``args`` parse from ``body`` when the request is sent by HTTP method "POST - application/x-www-form-urlencoded".



PROCESS FILE UPLOAD
===================

    x100http is designed for custom file processing, it can be used to optimize the video transcoding process.

    ``handler_function_init``, ``handler_function_process``, ``handler_function_del`` will be called when file upload.

    you can simulate a traditional file upload processing like this:

    1. open a file in ``handler_function_init``

    2. when ``handler_function_init`` be called, write content to the file

    3. close file in ``handle_function_del``


    handler_function_init(request)
    ------------------------------
    this function will be called when file upload start with arg ``request``.


    handler_function_process(name, content)
    ---------------------------------------
    this function will be called every time x100http read something throught network.

    the function will be called many times when big file uploading, it need to process a part of the file every time.

    ``name`` is the html input`s name.

    ``content`` is the html input`s value, binary file content some.


    handler_function_del(request)
    -----------------------------
    this function will be called when file upload finished.

    x100http expect a string from this function ues to construct HTTP response.



HTTP ERROR 500
==============

    visitor will get HTTP error "500" when the handler function of the url he visit raise an error or code something wrong.



SUPPORTED PYTHON VERSIONS
=========================

    x100http only supports python 3.3 or newer.



EXAMPLES
========

.. code-block:: python
    :linenos:

    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(req):
        remote_ip = req['remote_ip']
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)


