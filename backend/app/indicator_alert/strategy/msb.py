from typing import List
import pandas as pd
import pandas_ta as ta


class MSB:
    """
    Market Structure Break aler based on fractal of 3
    """

    def _fractal3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        calculate fractal of 3 high low from ohlcv dataframe

        Args:
            df (pd.DataFrame): ohlcv dataframe

        Returns:
            pd.DataFrame: ohlcv dataframe with fractal3 included
        """
        df["rsi"] = round(ta.rsi(df["close"], 14).dropna(), 2)  # rsi
        df["ema"] = ta.ema(df["close"], length=34)  # ema
        # --- fractal3 ---
        df["zh"] = df.high[
            ((df.high.shift(-1) < df.high) & (df.high.shift(1) < df.high))
        ]
        df["zl"] = df.low[((df.low.shift(-1) > df.low) & (df.low.shift(1) > df.low))]
        df["zh"] = df["zh"].ffill()
        df["zl"] = df["zl"].ffill()
        df["bos_h"] = ta.cross(df.close, df.zh)
        df["bos_l"] = ta.cross(df.zl, df.close)
        return df

    def result(self, dfs: List[pd.DataFrame]) -> dict:
        """
        Calculate result of MSB indicator

        Args:
            dfs (List[pd.DataFrame]): list of pandas.Dataframe

        Returns:
            dict: dict contain result
        """
        result = {"high": [], "low": []}
        for df in dfs:
            df = self._fractal3(df)
            if (df.bos_h[-2:].values[0] == 1) and (
                df.bos_h[-2:].values[0] > df.ema[-2:].values[0]
            ):
                result["high"].append(df.name)
            elif (df.bos_l[-2:].values[0] == 1) and (
                df.bos_l[-2:].values[0] < df.ema[-2:].values[0]
            ):
                result["low"].append(df.name)
        return result
