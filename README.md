# SCHOOL - Project

## DESCRIPTION  
The **Trade** project consists of creating a program that simulates a trading bot. This bot will analyze market data and automatically decide whether to **buy**, **sell**, or **hold** assets based on a given strategy. The objective is to achieve the best profit possible.

---

## FEATURES  
- **Market analysis:**  
  - Process input data to analyze asset prices and trends.  
- **Trading decisions:**  
  - Make decisions to **buy**, **sell**, or **hold** based on implemented strategies.  
- **Input/Output:**  
  - Real-time data is passed through the standard input and results are displayed on the standard output.  
- **Custom strategies:**  
  - Implement and test different trading strategies to optimize profits.  

---

## FUNCTIONS ALLOWED  
- Standard library functions:  
  - `malloc`, `free`, `read`, `write`, `exit`, `fprintf`, `printf`.  
- System calls:  
  - `open`, `close`, `read`, `write`.

---


Trading Strategy
The bot uses the Parabolic SAR (PSAR) indicator to decide trades:

BUY: If the price is above PSAR and USDT is available, the bot buys 50% of the stack.
SELL: If the price is below PSAR and BTC is available, the bot sells 50% of the stack.
NO ACTION: If conditions are not met or trade size is too small (< 0.001 BTC).
This ensures minimal risk while following market trends.
