class HCIHandler:
    def __init__(self, credentials: dict[str, str]) -> None:
        for key, value in credentials.items():
            setattr(self, key, value)
    
    def get_token(self) -> str:
        pass

    def get_index(self, token, index = "all") -> None:
        pass

    def query(self, token, index_name, query_string) -> None:
        pass