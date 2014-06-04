__all__ = ['IncompleteConfigError', 'Config']

import configparser


class IncompleteConfigError(Exception):
    def __init__(self, section, option):
        self.section = section
        self.option = option

    def __str__(self):
        if self.option is not None:
            return ">> Missing option {option} in section {section}" + \
                "of config file".format(option=self.option,
                                        section=self.section)
        else:
            return ">> Missiong section {section} in config file".format(
                section=self.section)


class Config(configparser.ConfigParser):

    def __init__(self, location="silpa.conf"):
        configparser.ConfigParser.__init__(self)
        self.read(location)
        self.verify()

    def verify(self):
        self._verify_item("main", "site")
        self._verify_item("main", "baseurl")
        self._verify_item("logging", "log_level")
        self._verify_item("logging", "log_folder")
        self._verify_item("logging", "log_name")

        if not self.has_section("modules"):
            raise IncompleteConfigError("modules", None)

        if not self.has_section("module_display"):
            raise IncompleteConfigError("module_display", None)

    def _verify_item(self, section, option):
        if not self.has_option(section, option):
            raise IncompleteConfigError(section, option)
