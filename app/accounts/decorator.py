from django.shortcuts import render


def unauthenticated_user(template_name='accounts/unauthenticated_error.html'):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Render a custom template for authenticated users
                return render(request, template_name, {'error_message': 'You are already authenticated.'})
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
