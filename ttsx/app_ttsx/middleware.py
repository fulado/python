class UrlMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path not in ['/user/register/',
                                '/user/register_service/',
                                '/user/login/',
                                '/user/login_server/',
                                '/user/logout/']:
            request.session['path'] = request.get_full_path()
