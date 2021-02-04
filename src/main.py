from api_init import app
import werkzeug.datastructures
def main(request):
    with app.app_context():
        headers = werkzeug.datastructures.Headers()
        for key, value in request.headers.items():
            headers.add(key, value)
        test_request_dict = {
            'method':request.method,
            'base_url':request.base_url,
            'path':request.path,
            'query_string':request.query_string,
            'headers':headers
        }
        # JSON與data不可能共存，帶進test_request_context會出錯，故只能選其中一個
        if request.json:
            test_request_dict['json'] = request.json
        else:
            data_dict = {}
            if request.form:
                data_dict.update(request.form.to_dict())
            if request.files:
                data_dict.update(request.files.to_dict())
            if data_dict:
                test_request_dict['data'] = data_dict
        # with app.test_request_context(method=request.method, base_url=request.base_url, path=request.path, query_string=request.query_string, headers=headers, data=request.data):
        with app.test_request_context(**test_request_dict):
            try:
                rv = app.preprocess_request()
                if rv is None:
                    rv = app.dispatch_request()
            except Exception as e:
                rv = app.handle_user_exception(e)
            response = app.make_response(rv)
            return(app.process_response(response))