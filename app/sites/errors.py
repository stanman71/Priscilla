from flask import json, url_for, redirect, render_template, flash, g, session, jsonify, request

from app import app


def http_err(err_code):
	
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
	
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
    
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
    

@app.errorhandler(400)
def e400(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 400)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )


@app.errorhandler(401)
def e401(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 401)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )


@app.errorhandler(403)
def e403(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 403)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )


@app.errorhandler(404)
def e404(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 404)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )


@app.errorhandler(410)
def e410(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 410)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )


@app.errorhandler(500)
def e500(e):

    # custommize your page title / description here
    page_title = 'Login - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, login page.'

    data          = {'navigation': 'None'}
    error_message = http_err( 500)

    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,
                            content=render_template( 'pages/errors.html', 
                                                     error_message=error_message) 
                            )