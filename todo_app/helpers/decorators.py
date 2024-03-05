from flask import redirect
from flask_dance.contrib.github import github


def login_required(original_route):
    def protected_route(*args, **kwargs):
        if not github.authorized:
            return redirect("/login")
        return original_route(*args, **kwargs)
    protected_route.__name__ = original_route.__name__
    return protected_route


def logout_required(original_route):
    def protected_route(*args, **kwargs):
        if github.authorized:
            return redirect("/")
        return original_route(*args, **kwargs)
    protected_route.__name__ = original_route.__name__
    return protected_route
