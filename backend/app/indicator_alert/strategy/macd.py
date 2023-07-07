from typing import List
import pandas as pd
import pandas_ta as ta


class MacdCross:
    """
    macd cross alert
    """

    def _macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        calculate macd cross from ohlcv dataframe

        Args:
            df (pd.DataFrame): ohlcv dataframe

        Returns:
            pd.DataFrame: ohlcv dataframe with macd cross included
        """
        df_macd = round(ta.macd(df.close), 2)  # macd
        df = df.join(df_macd)
        df.columns = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "macd",
            "hist",
            "signal",
        ]
        df["cross_h"] = ta.cross(df.macd, df.signal)
        df["cross_l"] = ta.cross(df.signal, df.macd)
        return df

    def result(self, dfs: List[pd.DataFrame], candle: int = 1) -> dict:
        """
        Calculate result of MACD Cross indicator

        Args:
            dfs (List[pd.DataFrame]): list of pandas.Dataframe
            candle (int): confirmation candle needed

        Returns:
            dict: dict contain result
        """
        result = {"high": [], "low": []}
        confirm_candle = 0 - candle
        for df in dfs:
            df = self._macd(df)
            if candle == 1:
                if (df.cross_h[confirm_candle:].values[0] == 1) and (
                    df.macd[confirm_candle:].values[0] < 0
                ):
                    result["high"].append(df.name)
                elif (df.cross_l[confirm_candle:].values[0] == 1) and (
                    df.macd[confirm_candle:].values[0] > 0
                ):
                    result["low"].append(df.name)
            elif candle > 1:
                if (df.cross_h[confirm_candle : 1 - candle].values[0] == 1) and (
                    df.macd[confirm_candle : 1 - candle].values[0] < 0
                ):
                    result["high"].append(df.name)
                elif (df.cross_l[confirm_candle : 1 - candle].values[0] == 1) and (
                    df.macd[confirm_candle : 1 - candle].values[0] > 0
                ):
                    result["low"].append(df.name)
        return result
