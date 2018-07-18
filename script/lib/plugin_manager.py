#!/usr/bin/env python
# -*- coding:utf-8 -*-

import binascii
import json
import sqlite3
import os
from imp import find_module, load_module
from script.lib import requests, threadpool
from os import walk


class PluginManager(object):
    """
    插件管理器
    """

    def __init__(self):
        self.plugins = {}
        self.conn = sqlite3.connect(os.path.dirname(__file__) + "\\..\\database\\core.db")
        self.conn.text_factory = str
        self.cu = self.conn.cursor()
        self.current_plugin = ""

    def version(self):
        """
        插件库版本
        :return: string, 插件库版本
        """
        self.cu.execute("select version from core")
        return self.cu.fetchone()[0]

    def cms_num(self):
        """
        查询 CMS 数量
        :return: int, CMS 数量
        """
        self.cu.execute("select cms from plugins")
        return len(set(self.cu.fetchall()))

    def plugins_num(self):
        """
        查询插件数量
        :return: int, 插件数量
        """
        self.cu.execute("select count(*) from plugins")
        return self.cu.fetchone()[0]

    def list_plugins(self, start=0, end=5):
        """
        显示插件列表
        :return: list, 插件列表
        """
        self.cu.execute("select name, scope, description from plugins limit " + str(start) + ", 5")
        return self.cu.fetchall()

    def search_plugin(self, keyword):
        """
        搜索插件
        :param keyword: string, 插件信息
        :return: list, 插件列表
        """
        keyword = "%" + keyword + "%"
        self.cu.execute("select name, scope, description from plugins where "
                        "name like ? or scope like ? or description like ?", (keyword, keyword, keyword))
        return self.cu.fetchall()

    def info_plugin(self, plugin):
        """
        显示插件信息
        :param plugin: string, 插件名
        :return: string, 插件信息
        """
        self.cu.execute("select name, author, cms, scope, description, "
                        "reference from plugins where name=?", (plugin,))
        return self.cu.fetchone()

    def load_plugin(self, plugin):
        """
        加载插件
        :param plugin: string, 插件名
        """
        if plugin not in self.plugins:
            self.plugins[plugin] = {}
            plugin_name = plugin[plugin.index("_") + 1:]
            plugin_dir = os.path.dirname(__file__) + "\\..\\plugins\\" + plugin[:plugin.index("_")]
            print(os.getcwd())
            module = load_module(plugin_name,
                                 *find_module(plugin_name, [plugin_dir]))
            self.plugins[plugin]["options"] = module.options
            self.plugins[plugin]["exploit"] = module.exploit
        self.current_plugin = plugin

    def show_options(self):
        """
        显示插件设置项
        :return:
        """
        return self.plugins[self.current_plugin]["options"]

    def set_option(self, option, value):
        """
        设置插件选项
        :param option: string, 设置项名称
        :param value: string, 设置值
        :return:
        """
        for op in self.plugins[self.current_plugin]["options"]:
            if op["Name"] == option:
                op["Current Setting"] = value
                return (op["Name"], value)
            else:
                break
        else:
            return "Invalid option: %s" % option

    def exec_plugin(self):
        """
        执行插件
        """
        options = {}
        for option in self.plugins[self.current_plugin]["options"]:
            name = option["Name"]
            current_setting = option["Current Setting"]
            required = option["Required"]
            if required and not current_setting:
                return [self.current_plugin, "%s is required!" % name, "Not Found"]
            else:
                if name == "URL":
                    if current_setting.endswith("/"):
                        options["URL"] = current_setting[:-1]
                    else:
                        options["URL"] = current_setting
                elif name == "Cookie":
                    options["Cookie"] = dict(
                        i.split("=", 1)
                        for i in current_setting.split("; ")
                    )
                elif name == "Thread":
                    options["Thread"] = int(current_setting)
                else:
                    options[name] = current_setting
        try:
            vuln = self.plugins[self.current_plugin]["exploit"](**options)
            if vuln:
                self.cu.execute("insert into vulns values (?, ?)",
                                (self.current_plugin, vuln))
                self.conn.commit()
                result = [self.current_plugin, vuln, "Found"]
                return result
            else:
                return [self.current_plugin, "None", "Not Found"]
        except sqlite3.ProgrammingError:
            return "数据库保存出错"

    def show_vulns(self):
        """
        显示当前漏洞信息
        :return:
        """
        self.cu.execute("select plugin, vuln from vulns")
        return self.cu.fetchall()

    def clear_vulns(self):
        """
        清空漏洞信息
        :return:
        """
        self.cu.execute("delete from vulns")
        self.conn.commit()

    def db_rebuild(self):
        """
        重建数据库
        :return:
        """
        self.cu.execute("delete from plugins")
        self.conn.commit()
        for dirpath, dirnames, filenames in walk("plugins/"):
            if dirpath == "plugins/":
                continue
            db = {
                "cms": dirpath.split("/")[1],
                "plugins": []
            }
            for fn in filenames:
                if fn.endswith("py"):
                    db["plugins"].append(fn.split(".")[0])
            for plugin in db["plugins"]:
                p = load_module(plugin, *find_module(plugin, [dirpath]))
                name = db["cms"] + "_" + plugin
                author = p.author
                scope = p.scope
                description = p.description
                reference = p.reference
                self.cu.execute("insert into plugins values (?, ?, ?, ?, ?, ?)",
                                (name, author, db["cms"], scope, description,
                                 reference))
                self.conn.commit()

    def down_plugin_list(self):
        """
        获取远程插件列表
        :param dirs: 所有插件目录
        :return: list, 远程插件列表
        """
        # 远程url
        base_url = "https://xxx.com"
        plugin_dirs = []
        remote_plugins = []

        def down_plugin_dirs():
            """
            获取远程插件目录
            :return:
            """
            r = requests.get(base_url + "plugins")
            r.close()
            j = json.loads(r.text)
            for i in j:
                plugin_dirs.append(i["path"])

        def down_single_dir(plugin_dir):
            """
            下载单个目录插件列表
            :param plugin_dir: list, 插件目录
            """
            remote_plugins = []
            r = requests.get(base_url + plugin_dir)
            r.close()
            j = json.loads(r.text)
            for i in j:
                remote_plugins.append(i["path"])
            return remote_plugins

        def log(request, result):
            """
            threadpool callback
            """
            remote_plugins.extend(result)

        down_plugin_dirs()
        pool = threadpool.ThreadPool(10)
        reqs = threadpool.makeRequests(down_single_dir, plugin_dirs, log)
        for req in reqs:
            pool.putRequest(req)
        pool.wait()
        return remote_plugins

    def get_local_plugin_list(self):
        """
        获取本地插件列表
        :return:
        """
        local_plugins = []
        for dirpath, dirnames, filenames in walk("plugins/"):
            if dirpath == "plugin/":
                continue
            for fn in filenames:
                if fn.endswith(".py"):
                    local_plugins.append(dirpath + "/" + fn)
        return local_plugins

    def down_plugins(self, remote_plugins, local_plugins):
        """
        下载插件
        :param remote_plugins: list, 远程插件列表
        :param local_plugins: list, 本地插件列表
        :return: list, 新增插件列表
        """

        def down_single_plugin(plugin):
            """
            下载单个插件
            :return:
            """
            base_url = "https://xxx.com/"
            r = requests.get(base_url + plugin)
            r.close()
            j = json.loads(r.text)
            data = binascii.a2b_base64(j["content"])
            with open(plugin, "w") as f:
                f.write(data)

        for plugin in local_plugins:
            if plugin in remote_plugins:
                remote_plugins.remove(plugin)
        pool = threadpool.ThreadPool(10)
        reqs = threadpool.makeRequests(down_single_plugin, remote_plugins)
        for req in reqs:
            pool.putRequest(req)
        pool.wait()
        return remote_plugins

    def exit(self):
        """
        退出插件管理器
        :return:
        """
        self.conn.close()
