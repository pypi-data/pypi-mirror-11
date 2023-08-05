# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class SpiritConfig(AppConfig):
    # TODO: remove this in spirit 0.4

    name = 'spirit'
    verbose_name = "Spirit"

    def ready(self):
        self.register_config()
        self.register_signals()

    def register_config(self):
        import djconfig
        from spirit.admin.forms import BasicConfigForm

        djconfig.register(BasicConfigForm)

    def register_signals(self):
        from .topic.poll import signals as poll
        from .user import signals as user