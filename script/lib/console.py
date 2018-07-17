#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from script.lib import logger
from script.lib.plugin_manager import PluginManager


class core_class(PluginManager):
    '''
    核心类
    '''

    def __init__(self):
        PluginManager.__init__(self)

    def plugins_enum(self):
        print()
        print('1.查看插件列表')
        print('2.通过关键字搜索插件')
        print('3.选择插件')
        print('4.查看已探测到的所有漏洞信息')
        print('5.清空已探测到的漏洞信息')
        print('6.更新POC库')
        print("输入'exit'退出程序！")
        print()

    def use_enum(self):
        print()
        print('1.显示插件信息')
        print('2.显示当前插件选项')
        print('3.设置当前插件选项')
        print('4.运行当前插件')
        print('4.查看已探测到的漏洞信息')
        print('5.保存已探测到的漏洞信息到文件')
        print("输入'back'返回！")
        print()

    def do_version(self):
        """
        版本信息
        """
        info = ["POC库版本: %s" % self.version(), "CMS数目: %d" % self.cms_num(), "POC数目: %d" % self.plugins_num(),
                self.plugins_enum()]
        return info

    def do_list(self, start, end):
        """
        POC列表
        """
        return self.list_plugins(start, end)

    def do_search(self, keyword):
        """
        搜索POC
        """
        # if keyword:
        #     print("\n匹配的POC\n================\n")
        #     print("%-40s%-40s%s" % ("Name", "Scope", "Description"))
        #     print("%-40s%-40s%s" % ("----", "-------", "-----------"))
        #     for name, scope, description in self.search_plugin(keyword):
        #         print("%-40s%-40s%s" % (name, scope, description))
        #     print('\n')
        # else:
        #     logger.error("\n请输入关键字！\n")

        return self.search_plugin(keyword)

    def do_use(self, plugin):
        """
        加载插件
        :param plugin: string, 插件名称
        :return:
        """
        if plugin:
            try:
                self.load_plugin(plugin)
            except Exception:
                logger.error("请输入正确的POC: %s" % plugin)
        else:
            logger.error("请输入POC插件（不能为空）")

    def do_info(self, plugin):
        """
        POC信息
        :param plugin: string, 插件名称
        :return:
        """
        if not plugin:
            if self.current_plugin:
                plugin = self.current_plugin
            else:
                logger.error("请输入POC文件名")
                return
        if self.info_plugin(plugin):
            name, author, cms, scope, description, reference = \
                self.info_plugin(plugin)
            print("\n%15s: %s" % ("Name", name))
            print("%15s: %s" % ("CMS", cms))
            print("%15s: %s\n" % ("Scope", scope))
            print("Author:\n\t%s\n" % author)
            print("Description:\n\t%s\n" % description)
            print("Reference:\n\t%s\n" % reference)
        else:
            logger.error("无效文件名: %s" % plugin)

    def do_options(self):
        """
        插件设置项
        :return:
        """
        if self.current_plugin:
            rn = self.show_options()
            if isinstance(rn, str):
                logger.error(rn)
            else:
                print("\n\t%-20s%-40s%-10s%s" % ("Name", "Current Setting",
                                                 "Required", "Description"))
                print("\t%-20s%-40s%-10s%s" % ("----", "---------------",
                                               "--------", "-----------"))
                for option in rn:
                    print("\t%-20s%-40s%-10s%s" % (option["Name"],
                                                   option["Current Setting"],
                                                   option["Required"],
                                                   option["Description"]))
                print('\n')
        else:
            logger.error("Select a plugin first.")

    def do_exploit(self):
        """
        执行插件
        :return:
        """
        if self.current_plugin:
            rn = self.exec_plugin()
            if (rn == 'Cookie is required!'):
                return ["", 'Cookie is required!', ""]
            if not rn[0]:
                logger.error(rn[1])
            return rn
        else:
            logger.error("先选择一个POC插件")

    def do_vulns(self, model, plugins):
        """
        漏洞信息
        :param arg: string, 参数
        :return:
        """
        # 查看漏洞信息
        if not (model and plugins):
            vulns = self.show_vulns()
            print("\nVulns\n=====\n")
            print("%-40s%s" % ("Plugin", "Vuln"))
            print("%-40s%s" % ("------", "----"))
            for plugin, vuln in vulns:
                print("%-40s%s" % (plugin, vuln))
            print('\n')
        # 删除漏洞信息
        elif model == "delete":
            self.clear_vulns()
            logger.success("清除漏洞信息成功.")
        # 保存漏洞信息到文件
        elif model == "save":
            plugin_name = plugins
            vulns = self.show_vulns()
            with open("vulns.txt", "a") as f:
                f.write(os.linesep)
                f.write("[%s]" % plugin_name + os.linesep)
                for i in vulns:
                    if i[0] == plugin_name:
                        f.write(i[1] + os.linesep)
                f.write(os.linesep)
            logger.success("保存漏洞信息成功.")

    def do_rebuild_db(self, line):
        """
        重建数据库
        :return:
        """
        logger.process("清除当前数据库")
        logger.process("重建数据库")
        self.db_rebuild()
        logger.success("OK")

    def do_update(self):
        """
        更新
        :return:
        """
        logger.process("")
        logger.process("正在更新POC库")
        logger.process("")
        logger.process("下载POC列表")
        remote_plugins = self.down_plugin_list()
        logger.process("获取本地是POC列表")
        local_plugins = self.get_local_plugin_list()
        logger.process("比较-更新")
        new_plugins = self.down_plugins(remote_plugins, local_plugins)
        logger.success("新的POC库: %s" % str(new_plugins))
        self.do_rebuild_db("")

    def default(self):
        """
        输入错误的选择项
        :return:
        """
        logger.error("[-] 无效的选项!")
        print()

    def process(self, rn):
        '''
        返回选择
        :param rn string,退出提示
        :return:
        '''
        logger.process(rn)
        print()

    def emptychoice(self):
        '''
        输入为空
        :return:
        '''
        logger.error('输入不能为空,请输入你的选择!')
        print()

    def do_exit(self):
        """
        退出
        :return:
        """
        self.exit()
        exit()

    def emptyline(self):
        """
        空行
        :return:
        """
        pass
