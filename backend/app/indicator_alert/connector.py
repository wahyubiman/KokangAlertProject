""" connector for exchange """
import ccxt
import requests
import asyncio
import pandas as pd
from typing import List


class ExchangeConnector:
    """
    Exchange Connnector
    """

    def __init__(self, exchange: str, market_type: str = "spot"):
        """
        _summary_

        Args:
            exchange (str): exchange name supported by ccxt
            market_type (str, optional): market type ex: spot, future, etc. Defaults to 'spot'.

        Raises:
            ccxt.ExchangeNotAvailable: exchange not supported
        """

        if exchange in ccxt.exchanges:
            self.exchange = getattr(ccxt, exchange)(
                {
                    "options": {"defaultType": market_type},
                }
            )
        else:
            raise ccxt.ExchangeNotAvailable(
                f"{exchange} exchange not supported by CCXT"
            )

    def get_symbol_list(self, quote: str = "USDT") -> List[str]:
        """
        Get supported symbol on exchange defined in constructor

        Args:
            quote (str, optional): quote symbol. Defaults to 'USDT'.

        Raises:
            EmptySymbol: symbol empty
            Exception: exception

        Returns:
            List[str]: list of symbols
        """

        try:
            if "/" not in quote:
                quote = "/" + quote
            elif "/" in quote:
                quote = quote
            self.exchange.load_markets()
            result = [symbol for symbol in self.exchange.symbols if quote in symbol]
            if len(result) == 0:
                raise EmptySymbol
            return result
        except EmptySymbol:
            raise EmptySymbol
        except Exception as e:
            raise Exception(e)

    async def _get_ohlcv(
        self, symbol: str, timeframe: str = "1h", **kwargs
    ) -> pd.DataFrame:
        """
        fetch single OHLCV data

        Args:
            symbol (str): symbol name
            timeframe (str, optional): timeframe. Defaults to '1h'.

        Raises:
            ccxt.BadSymbol: symbol does not exist
            ccxt.NetworkError: network error
            requests.exceptions.SSLError: ssl failed / network error
            Exception: exception

        Returns:
            pandas.DataFrame: pandas dataframe
        """

        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, **kwargs)
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df.fillna(0)
            df.name = symbol
            return df
        except ccxt.BadSymbol:
            raise ccxt.BadSymbol(f"{symbol} not supported")
        except ccxt.NetworkError:
            raise ccxt.NetworkError(f"Please check your network connection")
        except requests.exceptions.SSLError:
            raise requests.exceptions.SSLError(
                "SSL Error, please check your network properly"
            )
        except Exception as e:
            raise Exception(e)

    async def _get_data(
        self, timeframe: str = "1h", quote: str = "USDT"
    ) -> List[pd.DataFrame]:
        """
        Bulk fecth OHLCV data in async

        Args:
            timeframe (str, optional): timeframe. Defaults to '1h'.
            quote (str, optional): quote symbol. Defaults to 'USDT'.

        Returns:
            List[pandas.DataFrame]: list of ohlcv dataframe
        """

        symbol_list = self.get_symbol_list(quote=quote)
        task = [
            asyncio.create_task(self._get_ohlcv(symbol, timeframe=timeframe))
            for symbol in symbol_list  # [-20:]
        ]
        result = await asyncio.gather(*task)
        return result

    def data(self, timeframe: str = "1h", quote: str = "USDT") -> List[pd.DataFrame]:
        """
        Get all ohlcv data

        Args:
            timeframe (str, optional): timeframe. Defaults to '1h'.
            quote (str, optional): quote symbol. Defaults to 'USDT'.

        Returns:
            List[pandas.DataFrame]: list of OHLCV dataframe
        """

        result = asyncio.run(self._get_data(timeframe, quote))
        return result


# -------------- Exception -----------------
class ExchangeConnectorException(Exception):
    pass


class EmptySymbol(ExchangeConnectorException):
    def __init__(self):
        super().__init__(
            "return symbol must not be empty, please  check the quote, maybe typo or unsupported quote currency"
        )
