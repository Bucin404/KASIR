import midtransclient
from flask import current_app
import qrcode
from io import BytesIO
import base64
import uuid
from datetime import datetime

class PaymentService:
    """Service untuk mengelola pembayaran"""
    
    def __init__(self):
        self.snap_client = None
        self.core_api_client = None
    
    def init_midtrans(self, server_key, is_production=False):
        """Initialize Midtrans client"""
        try:
            # Snap API client
            self.snap_client = midtransclient.Snap(
                is_production=is_production,
                server_key=server_key
            )
            
            # Core API client
            self.core_api_client = midtransclient.CoreApi(
                is_production=is_production,
                server_key=server_key
            )
            
            return True
        except Exception as e:
            print(f"Error initializing Midtrans: {e}")
            return False
    
    def create_transaction(self, order_id, amount, customer_details, item_details):
        """
        Create Midtrans transaction
        
        Args:
            order_id: Unique order ID
            amount: Total amount
            customer_details: Dict with customer info
            item_details: List of items
        """
        if not self.snap_client:
            return None, "Midtrans not initialized"
        
        try:
            transaction_details = {
                'order_id': order_id,
                'gross_amount': int(amount)
            }
            
            param = {
                'transaction_details': transaction_details,
                'customer_details': customer_details,
                'item_details': item_details,
                'credit_card': {
                    'secure': True
                }
            }
            
            transaction = self.snap_client.create_transaction(param)
            
            return {
                'token': transaction['token'],
                'redirect_url': transaction['redirect_url']
            }, None
            
        except Exception as e:
            print(f"Error creating Midtrans transaction: {e}")
            return None, str(e)
    
    def get_transaction_status(self, order_id):
        """Get transaction status from Midtrans"""
        if not self.core_api_client:
            return None, "Midtrans not initialized"
        
        try:
            status_response = self.core_api_client.transactions.status(order_id)
            return status_response, None
        except Exception as e:
            print(f"Error getting transaction status: {e}")
            return None, str(e)
    
    def cancel_transaction(self, order_id):
        """Cancel transaction"""
        if not self.core_api_client:
            return None, "Midtrans not initialized"
        
        try:
            cancel_response = self.core_api_client.transactions.cancel(order_id)
            return cancel_response, None
        except Exception as e:
            print(f"Error cancelling transaction: {e}")
            return None, str(e)

class QRCodeService:
    """Service untuk generate QR Code"""
    
    @staticmethod
    def generate_qr_code(data, size=10):
        """
        Generate QR code image
        
        Args:
            data: String data to encode
            size: Size of QR code (default 10)
        
        Returns:
            Base64 encoded image string
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    @staticmethod
    def generate_order_url(order_id, base_url):
        """Generate URL for online order"""
        return f"{base_url}/order/{order_id}"

def generate_unique_id(prefix=''):
    """Generate unique ID with prefix"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique = str(uuid.uuid4().hex)[:6].upper()
    return f"{prefix}{timestamp}{unique}"

def format_currency(amount):
    """Format number as Indonesian Rupiah"""
    return f"Rp {amount:,.0f}".replace(',', '.')

def calculate_tax(subtotal, tax_rate=0.10):
    """Calculate tax amount"""
    return round(subtotal * tax_rate)

def calculate_total(subtotal, tax=0, discount=0):
    """Calculate total amount"""
    return subtotal + tax - discount
