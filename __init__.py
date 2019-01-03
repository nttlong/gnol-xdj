#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package này dùng để mở rộng open edx app (dạng micro app)
"""
__apps__={}
__register_apps__ = {}
__controllers__ = []
__pages__ = []
__build_cached__ = None
__controllert_url_build_cache__ = None
from . controllers import Model
def create(urls):
    """
    Tạp app
    :param name:
    :param host_dir:
    :return:
    """
    urlpatterns = ()
    global __build_cached__
    if __build_cached__ == None:
        __build_cached__ = {}

    from django.conf.urls import url
    import django
    for item in __controllers__:

        if not __apps__.has_key(item.instance.app_name):
            import os
            try:
                if item.instance.app_dir != None:
                    server_static_path = os.sep.join([
                        item.instance.app_dir,"static"
                    ])
                    urlpatterns+=(
                        url(r'^' + item.instance.host_dir + '/static/(?P<path>.*)$', django.views.static.serve,
                            {'document_root': server_static_path, 'show_indexes': True}),
                    )
            except Exception as ex:
                raise ex
            __apps__.update({
                item.instance.app_name:item.instance.app_name
            })
        if not __build_cached__.has_key(item.instance.on_get.im_func.func_code.co_filename):
            if item.url=="":
                print item.instance.on_get.im_func.func_code.co_filename
                urlpatterns +=(
                    url(r"^"+item.instance.host_dir + "$", item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir + "/$", item.instance.__view_exec__)
                )
            else:
                urlpatterns += (
                    url(r"^"+item.instance.host_dir +"/"+item.url+"$", item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir +"/"+item.url+"/$", item.instance.__view_exec__)
                )
            for sub_page in item.instance.sub_pages:
                if item.url == "":
                    urlpatterns += (
                        url(r"^" + item.instance.host_dir+"/"+sub_page.url + "$", sub_page.exec_request_get),
                        url(r"^" + item.instance.host_dir +"/"+sub_page.url+ "/$", sub_page.exec_request_get)
                    )
                else:
                    urlpatterns += (
                        url(r"^" + item.instance.host_dir + "/" + item.url+"/"+sub_page.url + "$", sub_page.exec_request_get),
                        url(r"^" + item.instance.host_dir + "/" + item.url+"/"+sub_page.url + "/$", sub_page.exec_request_get)
                    )
            __build_cached__.update({
                item.instance.on_get.im_func.func_code.co_filename:item.instance.on_get
            })
        # urlpatterns += (
        #     url(r'config/self_paced', ConfigurationModelCurrentAPIView.as_view(model=SelfPacedConfiguration)),
        #     url(r'config/programs', ConfigurationModelCurrentAPIView.as_view(model=ProgramsApiConfig)),
        #     url(r'config/catalog', ConfigurationModelCurrentAPIView.as_view(model=CatalogIntegration)),
        #     url(r'config/forums', ConfigurationModelCurrentAPIView.as_view(model=ForumsConfig)),
        # )
    if isinstance(urls,tuple):
        urls+=urlpatterns
    if isinstance(urls, list):
        urls.extend(list(urlpatterns))
    return urls
from . controllers import BaseController,Controller
from .page import Page

def register_INSTALLED_APPS():
    from django.conf import settings
    settings.INSTALLED_APPS.append("xdj_models.models")
    load_config()

def load_apps(path_to_app_dir,urlpatterns=None):
    from django.conf import settings
    if settings.INSTALLED_APPS.count("xdj_models.models") == 0:
        raise Exception("it look like you forgot call xdj.register_INSTALLED_APPS() at manage.py before startup.run()\n"
                        "How to use xdj?\n"
                        "At before startup.run() for dev mode or for deploy mode bottom of '{edx source}/apps/edx/edx-platform/lms/envs/bitnami.py' put follow code:\n"
                        "import sys\n"
                        "sys.path.append(path to parent of xdj package)\n"
                        "import xdj"
                        "xdj.register_INSTALLED_APPS()\n"
                        "")

    if urlpatterns==None:
        urlpatterns=()
    import os
    import sys
    import imp
    import xdj
    global __controllert_url_build_cache__
    if __controllert_url_build_cache__ == None:
        __controllert_url_build_cache__ = {}
    sys.path.append(path_to_app_dir)
    apply_settings()
    def get_all_sub_dir():
        lst=[x for x in os.walk(path_to_app_dir).next()[1] if x.find(".")==-1]
        return lst
    lst_sub_dirs = get_all_sub_dir()
    for item in lst_sub_dirs:
        full_path_to_app = os.sep.join([path_to_app_dir,item])
        sys.path.append(full_path_to_app)
        controller_dir = os.sep.join([path_to_app_dir,item,"controllers"])
        if not hasattr(xdj, "apps"):
            setattr(xdj, "apps", imp.new_module("xdj.apps"))
        if not hasattr(xdj.apps, item):
            setattr(xdj.apps, item, imp.new_module("xdj.apps.{0}".format(item)))
        app_settings = imp.load_source("xdj.apps.{0}.settings".format(item),os.sep.join([path_to_app_dir,item,"settings.py"]))
        if not hasattr(app_settings,"app_name"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "app_name",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"on_authenticate"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "on_authenticate",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not callable(app_settings.on_authenticate):
            raise Exception("{0} in {1} must be a function with one param".format(
                "on_authenticate",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"host_dir"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "host_dir",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not type(app_settings.host_dir) in [str,unicode]:
            raise Exception(
                "{0} in {3} mut be in {1}, not is {2}".format(
                    "host_dir",
                    [str,unicode],
                    app_settings.host_dir,
                    os.sep.join([path_to_app_dir, item, "settings.py"])
                )
            )
        if not hasattr(app_settings,"on_get_language_resource_item"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not callable(app_settings.on_get_language_resource_item):
            raise Exception("'{0}' in '{1}' must be a function like bellow\n"
                            "on_get_language_resource_item(language,appname,view,key,value)".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"rel_login_url"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "rel_login_url",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        import inspect
        if inspect.getargspec(app_settings.on_get_language_resource_item).args.__len__()<4:
            raise Exception("'{0}' in '{1}' must be a function like bellow\n"
                            "on_get_language_resource_item(language,appname,view,key,value)".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))

        _app=getattr(xdj.apps, item)
        if not hasattr(_app,"settings"):
            setattr(_app,"settings",app_settings)

        sys.path.append(controller_dir)
        files = os.listdir(controller_dir)
        for file in files:

            import inspect
            controller_file = os.sep.join([controller_dir,file])
            if not __controllert_url_build_cache__.has_key(controller_file):
                m = imp.load_source("{0}.{1}".format(item,file.split('.')[0]),controller_file)
                controller_instance=__controllers__[__controllers__.__len__()-1].instance
                if inspect.getfile(controller_instance.__class__) == controller_file:
                    __controllers__[__controllers__.__len__() - 1].app_dir = os.sep.join([path_to_app_dir,item])
                    controller_instance.app_dir = os.sep.join([path_to_app_dir,item])
                    controller_instance.host_dir = app_settings.host_dir
                    controller_instance.app_name = app_settings.app_name
                    controller_instance.on_authenticate = app_settings.on_authenticate
                    controller_instance.rel_login_url = app_settings.rel_login_url
                    controller_instance.settings = app_settings
                    controller_instance.param_names = __controllers__[__controllers__.__len__()-1].params
                    print controller_instance.url
                    print inspect.getfile(controller_instance.__class__)

                    from . controllers import Res
                    controller_instance.res = Res(app_settings.on_get_language_resource_item,controller_instance.app_name,controller_instance.template)
                else:
                    print "uncontroller file {0}".format(
                        controller_file
                    )
                __controllert_url_build_cache__.update({
                    controller_file:controller_instance
                })

            """
            # self.controllerClass()
            if self.instance.app_name==None:
                raise Exception("{0} do not have 'app_name'".format(self.controllerClass))
            if self.instance.app_dir==None:
                raise Exception("{0} do not have 'app_dir'".format(self.controllerClass))
            """
            x=1

    return create(urlpatterns)

class dobject(object):
    def __init__(self,*args,**kwargs):
        def feed_data(data):
              for k,v in data.items():
                    if isinstance(v,dict):
                        self.__dict__.update({
                            k:dobject(v)
                        })
                    elif isinstance(v,list):
                        lst =[]
                        for item in v:
                            lst.append(dobject(item))
                        self.__dict__.update({
                            k:lst
                        })
                    else:
                        self.__dict__.update({
                            k:v
                        })
        if args.__len__()==0:
            feed_data(kwargs)
        else:
            feed_data(args[0])

def apply_settings():
    """
    https://openedx.atlassian.net/wiki/spaces/AC/pages/34734726/edX+Feature+Flags
    :return:
    """
    from django.conf import settings
    setattr(settings,"USE_DJANGO_PIPELINE",True)
    """
    http://django-pipeline.readthedocs.org/ – whatever version we specify in our requirements.txt
    """
    setattr(settings,"DISPLAY_DEBUG_INFO_TO_STAFF",True)
    """For large courses this slows down courseware access for staff."""
    setattr(settings,"MILESTONES_APP",True)

def load_config():
    import json
    import os
    import sys
    filet_of_data_config = os.sep.join([os.path.dirname(__file__),"config","data.json"])
    with open( filet_of_data_config,'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        settings.DATABASES['default']['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES['default']['NAME'] = data["sql"]["name"]
        settings.DATABASES['default']['PORT'] = data["sql"]["port"]
        settings.DATABASES['default']['HOST'] = data["sql"]["host"]
        settings.DATABASES['default']['USER'] = data["sql"]["user"]
        settings.DATABASES['default']['PASSWORD'] = data["sql"]["password"]

        settings.DATABASES["read_replica"]['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES["read_replica"]['NAME'] = data["sql"]["name"]
        settings.DATABASES["read_replica"]['PORT'] = data["sql"]["port"]
        settings.DATABASES["read_replica"]['HOST'] = data["sql"]["host"]
        settings.DATABASES["read_replica"]['USER'] = data["sql"]["user"]
        settings.DATABASES["read_replica"]['PASSWORD'] = data["sql"]["password"]

        settings.DATABASES['student_module_history']['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES['student_module_history']['NAME'] = data["sql"]["name"]
        settings.DATABASES['student_module_history']['PORT'] = data["sql"]["port"]
        settings.DATABASES['student_module_history']['HOST'] = data["sql"]["host"]
        settings.DATABASES['student_module_history']['USER'] = data["sql"]["user"]
        settings.DATABASES['student_module_history']['PASSWORD'] = data["sql"]["password"]

        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]

        settings.CONTENTSTORE["OPTIONS"]["db"] = data["mongo"]["name"]
        settings.CONTENTSTORE["OPTIONS"]["host"] = data["mongo"]["host"]
        settings.CONTENTSTORE["OPTIONS"]["user"] = data["mongo"]["user"]
        settings.CONTENTSTORE["OPTIONS"]["password"] = data["mongo"]["password"]
        settings.CONTENTSTORE["OPTIONS"]["port"] = data["mongo"]["port"]

        settings.DOC_STORE_CONFIG["db"] = data["mongo"]["name"]
        settings.DOC_STORE_CONFIG["host"] = data["mongo"]["host"]
        settings.DOC_STORE_CONFIG["user"] = data["mongo"]["user"]
        settings.DOC_STORE_CONFIG["password"] = data["mongo"]["password"]
        settings.DOC_STORE_CONFIG["port"] = data["mongo"]["port"]

        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]

        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]
