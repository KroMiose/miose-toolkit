from typing import List

import pkg_resources


def get_pkg_version(pkg_name: str) -> str:
    """获取包的版本"""
    return pkg_resources.get_distribution(pkg_name).version


class Version:

    def __init__(self, version: str):
        self.version = version
        self.major, self.minor, self.patch = [int(x) for x in version.split(".")]

    def __lt__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) < 0

    def __le__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) <= 0

    def __eq__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) == 0

    def __ne__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) != 0

    def __gt__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) > 0

    def __ge__(self, other: "Version") -> bool:
        return self.__compare_versions(self.version, other.version) >= 0

    def __str__(self) -> str:
        return self.version

    def __repr__(self) -> str:
        return self.version

    @classmethod
    def __compare_versions(cls, v1: str, v2: str) -> int:
        """
        Compare two version strings and return -1 if v1 < v2, 0 if v1 == v2, and 1 if v1 > v2.
        """

        def normalize(v: str) -> List[int]:
            return [int(x) for x in v.split(".")]

        v1n: List[int] = normalize(v1)
        v2n: List[int] = normalize(v2)

        if v1n < v2n:
            return -1
        if v1n > v2n:
            return 1
        return 0

