from rest_framework.exceptions import ValidationError

class AtLeastOneAssetRequiredError(ValidationError):
    def __init__(self):
        super().__init__("At least one of received_asset or transacted_asset must be provided.")

class MissingAssetQuantityError(ValidationError):
    def __init__(self, field):
        super().__init__(f"Quantity must be provided for {field}.")

class CryptocurrencyNotFoundError(ValidationError):
    def __init__(self, field, ticker_symbol):
        super().__init__({field: [f"Cryptocurrency with the ticker symbol '{ticker_symbol}' does not exist."]})