# MEXC USDC Unfreezer 🔓

A Python tool to diagnose and resolve frozen USDC funds on MEXC exchange. This tool helps users who have USDC showing as "frozen" or "used" when there are no visible open orders in the MEXC interface.

## 🚨 Problem This Solves

Have you ever experienced:
- USDC balance showing as "frozen" or "used" on MEXC
- No visible open orders in the exchange interface
- Unable to trade with your USDC funds
- The "Unfreeze" button in trading bots not working

This tool finds hidden orders across all USDC trading pairs and cancels them, instantly freeing your funds.

## ✨ Features

- **Comprehensive Diagnosis**: Scans all USDC trading pairs for hidden orders
- **Automatic Order Cancellation**: Cancels all found orders with one command
- **Multi-Account Check**: Checks spot, margin, and futures accounts
- **Manual Order Management**: Cancel specific orders by ID
- **Safe & Secure**: Uses official MEXC API, no withdrawal permissions needed

## 📋 Prerequisites

- Python 3.6 or higher
- MEXC account with API access
- API key with spot trading and read permissions (NO withdrawal permission needed)

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/honzastim/mexc-usdc-unfreezer.git
cd mexc-usdc-unfreezer
```

2. Install required dependencies:
```bash
pip install ccxt
```

## 🚀 Usage

1. Run the tool:
```bash
python mexc_usdc_unfreezer.py
```

2. Enter your MEXC API credentials when prompted
3. Choose from the menu options:
   - **Option 1**: Diagnose frozen funds (recommended first step)
   - **Option 2**: Automatically unfreeze USDC
   - **Option 3**: Manually cancel specific orders
   - **Option 4**: Check orders for a specific trading pair

## 🔑 API Key Setup

1. Log in to MEXC
2. Go to API Management
3. Create a new API key with:
   - ✅ Read permission
   - ✅ Spot trading permission
   - ❌ Withdrawal permission (keep disabled for safety)
4. Save your API key and secret

## 📖 How It Works

The tool works by:

1. **Fetching your balance** to see how much USDC is frozen
2. **Scanning all USDC trading pairs** for open orders (BTC/USDC, ETH/USDC, etc.)
3. **Finding hidden orders** that may not show in the web interface
4. **Cancelling all found orders** to release the frozen funds
5. **Checking other account types** (margin, futures) for trapped funds

## 🎯 Real Example

```
Diagnosis Result:
- USDC Total: 159.83454274
- USDC Free: 0.0
- USDC Frozen: 159.83454274
- Found 8 hidden BTC/USDC orders locking exactly 159.83454274 USDC

After running unfreezer:
- Successfully cancelled 8 orders
- USDC Free: 159.83454274 ✅
```

## ❓ Troubleshooting

**"API key invalid" error:**
- Ensure your API key has spot trading permission
- Check that you've copied the key and secret correctly

**"Funds still frozen after running:"**
- Check MEXC website for funds in:
  - Sub-accounts
  - Earn/Savings products
  - Pending withdrawals
- Wait a few minutes and try again (sometimes there's a delay)

**"No orders found but funds still frozen:"**
- Try Option 4 to check specific pairs you've traded
- Contact MEXC support as it might be a platform issue

## ⚠️ Disclaimer

- This tool uses the official MEXC API and is safe to use
- Always keep your API keys secure
- Never share your API secret with anyone
- This tool cannot access withdrawal functions
- Use at your own risk - always verify results on MEXC website

## 🤝 Contributing

Feel free to open issues or submit pull requests if you find bugs or have improvements!

## 📜 License

MIT License - feel free to use and modify as needed

## 🙏 Acknowledgments

- Built using the excellent [CCXT](https://github.com/ccxt/ccxt) library
- Thanks to the MEXC API documentation
- Special thanks to everyone who reports issues and contributes

## 💡 Tips

- Save this tool for future use - MEXC occasionally has this issue
- Consider adding order cleanup to your trading bots
- Set expiration times on your orders to prevent this
- Regularly check for stuck orders if you use API trading

---

**Found this helpful?** Give it a ⭐ and share with others who might need it!

**Having issues?** Open an issue on GitHub or check existing issues for solutions.
