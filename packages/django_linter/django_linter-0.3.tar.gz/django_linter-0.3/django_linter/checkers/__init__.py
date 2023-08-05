from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__all__ = ('register',)


def register(linter):
    from .settings import SettingsShecker
    from .models import ModelsChecker
    from .misc import MiscChecker
    from .layout import LayoutChecker
    from .forms import FormsChecker
    from .views import ViewsChecker

    linter.register_checker(SettingsShecker(linter))
    linter.register_checker(ModelsChecker(linter))
    linter.register_checker(MiscChecker(linter))
    linter.register_checker(LayoutChecker(linter))
    linter.register_checker(FormsChecker(linter))
    linter.register_checker(ViewsChecker(linter))
