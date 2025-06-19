import ccxt
import time
import json
from datetime import datetime

class MEXCUnfreezer:
    def __init__(self, api_key, secret_key):
        self.exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
            }
        })
        
        # Common USDC trading pairs on MEXC
        self.usdc_pairs = [
            'BTC/USDC', 'ETH/USDC', 'BNB/USDC', 'XRP/USDC', 
            'ADA/USDC', 'DOGE/USDC', 'MATIC/USDC', 'SOL/USDC',
            'DOT/USDC', 'AVAX/USDC', 'LINK/USDC', 'UNI/USDC',
            'ATOM/USDC', 'LTC/USDC', 'NEAR/USDC', 'ALGO/USDC',
            'TRX/USDC', 'SHIB/USDC', 'XLM/USDC', 'MANA/USDC',
            'SAND/USDC', 'AXS/USDC', 'FTM/USDC', 'HBAR/USDC',
            'EGLD/USDC', 'THETA/USDC', 'ICP/USDC', 'FIL/USDC',
            'VET/USDC', 'AAVE/USDC', 'USDT/USDC', 'USDC/USDT'
        ]
        
    def get_all_usdc_orders(self):
        """Fetch all open orders for USDC pairs"""
        all_orders = []
        
        print("   Checking USDC trading pairs for open orders...")
        for symbol in self.usdc_pairs:
            try:
                orders = self.exchange.fetch_open_orders(symbol)
                if orders:
                    all_orders.extend(orders)
                    print(f"   ✓ Found {len(orders)} orders in {symbol}")
            except Exception as e:
                # Skip pairs that might not exist or have no orders
                pass
        
        return all_orders
    
    def diagnose_frozen_funds(self):
        """Comprehensive diagnosis of why USDC funds are frozen"""
        print("\n🔍 Starting USDC Frozen Funds Diagnosis...\n")
        
        try:
            # 1. Check account balance details
            print("1. Checking account balances...")
            balance = self.exchange.fetch_balance()
            
            if 'USDC' in balance['total']:
                usdc_free = balance['USDC']['free']
                usdc_used = balance['USDC']['used']
                usdc_total = balance['USDC']['total']
                
                print(f"   USDC Total: {usdc_total}")
                print(f"   USDC Free: {usdc_free}")
                print(f"   USDC Used/Frozen: {usdc_used}")
                
                if usdc_used > 0:
                    print(f"\n   ⚠️  {usdc_used} USDC is frozen!")
            
            # 2. Check all open orders across USDC pairs
            print("\n2. Checking open orders...")
            all_orders = self.get_all_usdc_orders()
            
            if all_orders:
                print(f"\n   Found {len(all_orders)} total open orders:")
                usdc_locked_in_orders = 0
                
                for order in all_orders:
                    if order['side'] == 'buy':
                        # For buy orders, USDC is locked
                        order_value = order['remaining'] * order['price']
                        usdc_locked_in_orders += order_value
                    else:
                        # For sell orders, the other asset is locked, not USDC
                        order_value = 0
                    
                    print(f"   - {order['symbol']} {order['side'].upper()}: {order['remaining']} @ {order['price']} (ID: {order['id']})")
                    if order_value > 0:
                        print(f"     └─ USDC locked: {order_value:.8f}")
                
                print(f"\n   Total USDC locked in orders: {usdc_locked_in_orders:.8f}")
            else:
                print("   No open orders found in common USDC pairs")
            
            # 3. Check all trading pairs (comprehensive search)
            print("\n3. Performing comprehensive order search...")
            try:
                # Get all markets
                markets = self.exchange.load_markets()
                additional_usdc_pairs = [s for s in markets.keys() if 'USDC' in s and s not in self.usdc_pairs]
                
                if additional_usdc_pairs:
                    print(f"   Checking {len(additional_usdc_pairs)} additional USDC pairs...")
                    for symbol in additional_usdc_pairs[:20]:  # Check first 20 to avoid too many requests
                        try:
                            orders = self.exchange.fetch_open_orders(symbol)
                            if orders:
                                all_orders.extend(orders)
                                print(f"   ✓ Found {len(orders)} orders in {symbol}")
                        except:
                            pass
            except Exception as e:
                print(f"   Could not perform comprehensive search: {str(e)}")
            
            # 4. Check specific account endpoints
            print("\n4. Checking account-specific data...")
            try:
                # MEXC specific endpoint for account info
                account_info = self.exchange.private_get_account()
                if 'balances' in account_info:
                    for bal in account_info['balances']:
                        if bal['asset'] == 'USDC':
                            print(f"   Account API shows:")
                            print(f"   - Free: {bal.get('free', 0)}")
                            print(f"   - Locked: {bal.get('locked', 0)}")
            except:
                print("   Could not fetch account-specific data")
            
            # 5. Check sub-accounts
            print("\n5. Checking for sub-accounts...")
            try:
                # Try to get sub-account list
                sub_accounts = self.exchange.private_get_sub_account_list()
                if sub_accounts and 'subAccounts' in sub_accounts:
                    print(f"   Found {len(sub_accounts['subAccounts'])} sub-accounts")
                    print("   Note: Funds might be in a sub-account")
                else:
                    print("   No sub-accounts found")
            except:
                print("   Sub-account check not available")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during diagnosis: {str(e)}")
            return False
    
    def unfreeze_usdc(self):
        """Attempt to unfreeze USDC funds"""
        print("\n🔧 Attempting to unfreeze USDC funds...\n")
        
        try:
            # Step 1: Cancel all open orders
            print("Step 1: Cancelling all open orders...")
            all_orders = self.get_all_usdc_orders()
            
            if all_orders:
                cancelled_count = 0
                for order in all_orders:
                    try:
                        self.exchange.cancel_order(order['id'], order['symbol'])
                        print(f"   ✓ Cancelled order {order['id']} for {order['symbol']}")
                        cancelled_count += 1
                        time.sleep(0.5)  # Rate limiting
                    except Exception as e:
                        print(f"   ✗ Failed to cancel order {order['id']}: {str(e)}")
                
                print(f"\n   Successfully cancelled {cancelled_count} orders")
            else:
                print("   No orders to cancel")
            
            # Step 2: Cancel ALL orders (nuclear option)
            print("\nStep 2: Attempting to cancel ALL orders (all symbols)...")
            try:
                # MEXC specific endpoint to cancel all orders
                result = self.exchange.private_delete_openorders()
                print(f"   ✓ Cancel all orders response: {result}")
                time.sleep(2)  # Wait for cancellation to process
            except Exception as e:
                print(f"   Could not cancel all orders via API: {str(e)}")
            
            # Step 3: Check other account types
            print("\nStep 3: Checking other account types...")
            
            # Check margin account
            try:
                self.exchange.options['defaultType'] = 'margin'
                margin_balance = self.exchange.fetch_balance()
                
                if 'USDC' in margin_balance and margin_balance['USDC']['total'] > 0:
                    print(f"   Found {margin_balance['USDC']['total']} USDC in margin account")
                    # Try to transfer
                    try:
                        amount = margin_balance['USDC']['free']
                        if amount > 0:
                            # MEXC specific transfer
                            transfer_result = self.exchange.private_post_capital_transfer({
                                'asset': 'USDC',
                                'amount': str(amount),
                                'fromAccountType': 'MARGIN',
                                'toAccountType': 'SPOT'
                            })
                            print(f"   ✓ Transferred {amount} USDC from margin to spot")
                    except Exception as e:
                        print(f"   Could not transfer from margin: {str(e)}")
                
                self.exchange.options['defaultType'] = 'spot'
            except:
                self.exchange.options['defaultType'] = 'spot'
            
            # Step 4: Force balance refresh
            print("\nStep 4: Force refreshing balance...")
            time.sleep(3)  # Wait for all operations to complete
            
            # Multiple balance checks to force refresh
            for i in range(3):
                balance = self.exchange.fetch_balance()
                if 'USDC' in balance and balance['USDC']['free'] > 0:
                    break
                time.sleep(1)
            
            # Final balance check
            if 'USDC' in balance:
                print(f"\n📊 Final USDC Balance:")
                print(f"   Total: {balance['USDC']['total']}")
                print(f"   Free: {balance['USDC']['free']}")
                print(f"   Used: {balance['USDC']['used']}")
                
                if balance['USDC']['free'] > 0:
                    print(f"\n✅ Success! {balance['USDC']['free']} USDC is now available for trading!")
                else:
                    print("\n⚠️  USDC still appears frozen.")
                    print("\nPossible reasons:")
                    print("- Funds in sub-account (check MEXC website)")
                    print("- Pending withdrawal")
                    print("- Funds in Earn/Staking products")
                    print("- System delay (try again in a few minutes)")
                    print("\nPlease check MEXC website or contact support.")
            
        except Exception as e:
            print(f"\n❌ Error during unfreeze process: {str(e)}")
    
    def manual_order_cancel(self):
        """Manually cancel orders by ID"""
        print("\n🔧 Manual Order Cancellation")
        
        order_id = input("Enter order ID to cancel (or 'back' to return): ").strip()
        if order_id.lower() == 'back':
            return
        
        symbol = input("Enter trading pair (e.g., BTC/USDC): ").strip().upper()
        
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            print(f"\n✅ Order cancelled successfully: {result}")
        except Exception as e:
            print(f"\n❌ Failed to cancel order: {str(e)}")
    
    def check_specific_pair(self):
        """Check orders for a specific trading pair"""
        symbol = input("\nEnter trading pair to check (e.g., BTC/USDC): ").strip().upper()
        
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            if orders:
                print(f"\nFound {len(orders)} orders for {symbol}:")
                for order in orders:
                    print(f"- ID: {order['id']}, Side: {order['side']}, Amount: {order['amount']}, Price: {order['price']}")
            else:
                print(f"\nNo open orders found for {symbol}")
        except Exception as e:
            print(f"\nError checking {symbol}: {str(e)}")

def main():
    print("=" * 50)
    print("MEXC USDC Unfreezer Tool v2.0")
    print("=" * 50)
    print("\n⚠️  Make sure your API key has:")
    print("- Spot trading permission")
    print("- Read permission")
    print("- NO withdrawal permission (for safety)")
    
    # Get API credentials
    api_key = input("\nEnter MEXC API Key: ").strip()
    secret_key = input("Enter MEXC Secret Key: ").strip()
    
    unfreezer = MEXCUnfreezer(api_key, secret_key)
    
    while True:
        print("\n" + "="*50)
        print("Options:")
        print("1. Diagnose frozen funds")
        print("2. Unfreeze USDC (automatic)")
        print("3. Manual order cancellation")
        print("4. Check specific trading pair")
        print("5. Exit")
        print("="*50)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            unfreezer.diagnose_frozen_funds()
        elif choice == '2':
            unfreezer.unfreeze_usdc()
        elif choice == '3':
            unfreezer.manual_order_cancel()
        elif choice == '4':
            unfreezer.check_specific_pair()
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()