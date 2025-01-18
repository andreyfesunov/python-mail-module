import os
from imaplib import IMAP4, IMAP4_SSL
from typing import Callable


class IMAP4Client:
    def __init__(self) -> None:
        self.connection: IMAP4_SSL | None
        self._should_listen = False

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

            _ = connection.login(user=user, password=password)

            self.connection = connection

            print(f"Connected successfully to {host}:{port}.")
        except IMAP4.error as e:
            self.connection = None

            print(f"Connection failed: {e}.")

    def try_close_connection(self) -> None:
        """Method to close an IMAP connection if one is established."""
        if not self.connection:
            print(f"Connection is not established. Already closed.")
            return
        self.connection.logout()
        self.connection = None
        print("Connection closed.")

    def listen(self, callback: Callable[[str], None]) -> None:
        """Method to start listening for new emails in real-time."""
        if not self.connection:
            print("No connection established.")
            return

        self._should_listen = True

        try:
            # Select the mailbox (INBOX)
            self.connection.select("inbox")

            print("Listening for new emails from 'inbox'...")
            while self._should_listen:
                response = self.connection.idle()

                if response[0].decode() == "OK":
                    print("New email detected!")
                    callback("New email received.")

        except Exception as e:
            print(f"An error occurred while listening: {e}")
            self.try_close_connection()

    def stop_listening(self) -> None:
        """Method to stop the listening loop."""
        print("Stopping listening...")
        self._should_listen = False
        self.try_close_connection()
