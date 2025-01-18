import os
from imaplib import IMAP4, IMAP4_SSL
from typing import Callable, Optional


class IMAP4Client:
    def __init__(self) -> None:
        self.connection: Optional[IMAP4_SSL]

        self.try_connect(
            host=os.getenv("IMAP_HOST", "host"),
            port=int(os.getenv("IMAP_PORT", 993)),
            user=os.getenv("IMAP_USERNAME", "user"),
            password=os.getenv("IMAP_PASSWORD", "password"),
        )

    def try_connect(self, host: str, port: int, user: str, password: str) -> None:
        """Method that opens a connection if the credentials are correct."""
        try:
            connection = IMAP4_SSL(host=host, port=port)

            connection.login(user=user, password=password)

            self.connection = connection

            print(f"Connected successfully to {host}:{port}.")
        except IMAP4.error as e:
            self.connection = None

            print(f"Connection failed: {e}.")

    def try_close_connection(self) -> None:
        """Method to close an IMAP connection if one is established."""
        if not self.connection:
            return print(f"Connection is not established. Already closed.")
        self.connection.close()
        self.connection = None
        print("Connection closed.")

    def listen(self, _: Callable[[str], None]) -> None:
        """Method to start listening for new emails in real-time."""
        pass
