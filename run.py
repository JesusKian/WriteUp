import os
import subprocess
import mysql.connector

from dotenv import dotenv_values
from time import sleep
from sys import exit as error
from colorama import (
    Fore,
    init
)


class Color:
    RED = Fore.RED
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE


class Config(Color):
    def __init__(self, _username: str = str(), _password: str = str(), _distro: int = int()) -> None:
        self._clear()
        print(self._banner())
        sleep(1)

        # Checking Username
        if _username is str():
            error(f"{Config.RED}[!] {Config.CYAN}Invalid Username For MySQL")
        self._USERNAME: str = _username

        # Checking Password
        if _password is str():
            error(f"{Config.RED}[!] {Config.CYAN}Invalid Password For MySQL")
        self._PASSWORD: str = _password

        # Checking Distro
        if _distro not in range(1, 5):
            error(f"{Config.RED}[!] {Config.CYAN}Invalid Distro")
        self._DISTRO: str = _distro

        # Checking MySQL Package
        self._mysql_help() if self._check_mysql() is False else print(
            f"{Config.GREEN}[+] {Config.CYAN}MySQL Package Is Valid On Your System"
        )
        sleep(1)

        # Checking GoLang package
        self._golang_help if self._check_golang() is False else print(
            f"{Config.GREEN}[+] {Config.CYAN}GoLang Package Is Valid On Your System"
        )
        sleep(1)

        # Checking Directories And Files
        self._check_directory_file()

        # ConfigMySQL
        self._config_mysql()

        # Creating Executable File Of main.go
        print(
            f"{Config.GREEN}[+] {Config.CYAN}Creating Executable File Of main.go"
        )
        os.system("go build ./main.go")

    def _banner(self) -> str:
        return f"""
{Color.CYAN} __        __    _ _       _   _       
{Color.GREEN} \ \      / / __(_) |_ ___| | | |_ __  
{Color.MAGENTA}  \ \ /\ / / '__| | __/ _ \ | | | '_ \ 
{Color.RED}   \ V  V /| |  | | ||  __/ |_| | |_) |
{Color.WHITE}    \_/\_/ |_|  |_|\__\___|\___/| .__/ 
                                |_|    
        """

    def _check_mysql(self) -> bool:
        RESULT: str = subprocess.run(
            "command -v mysql",
            shell=True,
            capture_output=True,
        ).stdout.decode()

        return False if RESULT is str() else True

    def _check_golang(self) -> bool:
        RESULT: str = subprocess.run(
            "command -v go",
            shell=True,
            capture_output=True,
        ).stdout.decode()

        return False if RESULT is str() else True

    def _golang_help(self) -> None:
        match self._DISTRO:
            case 1:  # Debian
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install GoLang Package On Your System With -> [dpkg , apt , ...]"
                )

            case 2:  # Arch
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install GoLang Package On Your System With -> [pacman , yay , ...]"
                )

            case 3:  # Fedora
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install GoLang Package On Your System With -> [dnf , yum , ...]"
                )

            case 4:  # Another
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install GoLang Package On Your System With Your Package Manager"
                )

    def _mysql_help(self) -> None:
        match self._DISTRO:
            case 1:  # Debian
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install MySQL Package On Your System With -> [dpkg , apt , ...]"
                )

            case 2:  # Arch
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install MySQL Package On Your System With -> [pacman , yay , ...]"
                )

            case 3:  # Fedora
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install MySQL Package On Your System With -> [dnf , yum , ...]"
                )

            case 4:  # Another
                error(
                    f"{Config.RED}[!] {Config.CYAN}Please Install MySQL Package On Your System With Your Package Manager"
                )

    def _check_directory_file(self) -> None:
        DIRS: tuple = (
            "log",
            "src",
            "src/structure",
            "src/telegram",
            "src/discord",
            "src/request",
            "src/config",
            "src/sql",
            "static",
            "static/txt",
        )

        FILES: tuple = (
            "go.mod",
            "go.sum",
            "main.go",
            "log/log.log",
            "src/config/config.go",
            "src/structure/channel.go",
            "src/structure/secret.go",
            "src/structure/items.go",
            "src/structure/rss.go",
            "src/telegram/telegram.go",
            "src/discord/discord.go",
            "src/request/request.go",
            "src/sql/sql.go",
            "static/txt/urls.txt",
        )

        for directory in DIRS:
            error(
                f"{Config.RED}[-] {Config.CYAN}Invalid Directory ({directory})"
            ) if os.path.exists(directory) is False else print(
                f"{Config.GREEN}[+] {Config.CYAN}Valid Directory ({directory})"
            )
            sleep(1)

        for file in FILES:
            error(
                f"{Config.RED}[-] {Config.CYAN}Invalid File ({file})"
            ) if os.path.exists(file) is False else print(
                f"{Config.GREEN}[+] {Config.CYAN}Valid File ({file})"
            )
            sleep(1)

    def _config_mysql(self) -> None:
        database = mysql.connector.connect(
            host="localhost",
            user=self._USERNAME,
            password=self._PASSWORD
        )
        cursor = database.cursor()

        cursor.execute(
            f"CREATE database IF NOT EXISTS WriteUp"
        )
        database.commit()
        [... for _ in cursor]

        cursor.close()

        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password=self._PASSWORD,
            database="WriteUp"
        )
        cursor = database.cursor()

        cursor.execute(
            "CREATE TABLE if not exists MYSQL_USER_PASS (username VARCHAR(300), password VARCHAR(300))"
        )

        cursor.execute(
            "INSERT INTO MYSQL_USER_PASS (username,password) VALUES (%s, %s)",
            (
                'root',
                self._PASSWORD
            )
        )
        database.commit()
        [... for _ in cursor]

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS data (Title VARCHAR(300), Title VARCHAR(300), Link VARCHAR(300), PublishDate VARCHAR(300))"
        )
        database.commit()
        [... for _ in cursor]

        cursor.execute(
            "SELECT username, password FROM MYSQL_USER_PASS GROUP BY username, password"
        )
        [... for _ in cursor]

    def _clear(self) -> None:
        os.system("clear")


def main() -> None:
    ENV: dict = dotenv_values("config.env")

    Config(
        ENV["MYSQL_USERNAME"],
        ENV["MYSQL_PASSWORD"],
        int(ENV["DISTRO"]),
    )


if __name__ == "__main__":
    init(autoreset=True)
    main()
