/**
 * Global Printer Manager
 * Handles Bluetooth printer connection across all pages
 * Auto-reconnects on page load if printer was previously connected
 */

const PrinterManager = {
    device: null,
    characteristic: null,
    isConnected: false,
    printerName: null,
    reconnectAttempts: 0,
    maxReconnectAttempts: 5,
    reconnectInterval: null,
    
    // Initialize printer manager
    async init() {
        console.log('PrinterManager: Initializing...');
        await this.loadSavedPrinter();
        this.updateStatusUI();
        
        // Start background reconnect checker
        this.startReconnectChecker();
    },
    
    // Start background reconnect checker
    startReconnectChecker() {
        // Check every 5 seconds if we need to reconnect
        this.reconnectInterval = setInterval(async () => {
            if (!this.isConnected && this.printerName && this.reconnectAttempts < this.maxReconnectAttempts) {
                console.log('PrinterManager: Background reconnect attempt', this.reconnectAttempts + 1);
                await this.autoReconnect();
            }
        }, 5000);
    },
    
    // Load saved printer from database and attempt auto-reconnect
    async loadSavedPrinter() {
        try {
            const response = await fetch('/api/printer-status');
            if (response.ok) {
                const data = await response.json();
                if (data.printer_name) {
                    this.printerName = data.printer_name;
                    console.log('PrinterManager: Found saved printer:', this.printerName);
                    // Attempt auto-reconnect immediately
                    this.updateStatusUI('connecting');
                    await this.autoReconnect();
                }
            }
        } catch (error) {
            console.error('PrinterManager: Error loading saved printer:', error);
        }
    },
    
    // Auto-reconnect to previously paired device
    async autoReconnect() {
        if (!navigator.bluetooth) {
            console.log('PrinterManager: Bluetooth not supported');
            this.updateStatusUI('lastknown');
            return false;
        }
        
        // Check if getDevices is supported (Chrome 85+)
        if (!navigator.bluetooth.getDevices) {
            console.log('PrinterManager: getDevices() not supported - please click to connect manually');
            this.updateStatusUI('lastknown');
            return false;
        }
        
        try {
            this.reconnectAttempts++;
            this.updateStatusUI('connecting');
            
            // Get previously paired devices
            const devices = await navigator.bluetooth.getDevices();
            console.log('PrinterManager: Found', devices.length, 'paired devices');
            
            // Find our printer
            const matchingDevice = devices.find(d => d.name === this.printerName);
            
            if (matchingDevice) {
                console.log('PrinterManager: Found matching device:', matchingDevice.name);
                
                // Try direct GATT connection
                try {
                    const connected = await this.connectToDevice(matchingDevice);
                    if (connected) {
                        this.reconnectAttempts = 0; // Reset on successful connection
                        return true;
                    }
                } catch (e) {
                    console.log('PrinterManager: Direct connection failed:', e.message);
                }
                
                // Try watching for advertisements (device might be waking up)
                try {
                    await this.watchAndConnect(matchingDevice);
                } catch (e) {
                    console.log('PrinterManager: Watch advertisements failed:', e.message);
                }
            }
            
            // Show last known status if reconnect failed
            if (!this.isConnected && this.printerName) {
                this.updateStatusUI('lastknown');
            }
            
            return false;
            
        } catch (error) {
            console.error('PrinterManager: Auto-reconnect error:', error);
            if (this.printerName) {
                this.updateStatusUI('lastknown');
            }
            return false;
        }
    },
    
    // Watch for device advertisements and connect when available
    async watchAndConnect(device) {
        return new Promise((resolve, reject) => {
            const abortController = new AbortController();
            const timeout = setTimeout(() => {
                abortController.abort();
                resolve(false);
            }, 3000);
            
            device.addEventListener('advertisementreceived', async (event) => {
                console.log('PrinterManager: Advertisement received from', event.device.name);
                clearTimeout(timeout);
                abortController.abort();
                const connected = await this.connectToDevice(device);
                resolve(connected);
            }, { once: true });
            
            device.watchAdvertisements({ signal: abortController.signal }).catch(e => {
                if (e.name !== 'AbortError') {
                    reject(e);
                }
            });
        });
    },
    
    // Connect to a specific device
    async connectToDevice(device) {
        try {
            this.device = device;
            const server = await device.gatt.connect();
            
            // Try common thermal printer service UUIDs
            const serviceUUIDs = [
                '000018f0-0000-1000-8000-00805f9b34fb',
                '0000ff00-0000-1000-8000-00805f9b34fb',
                '49535343-fe7d-4ae5-8fa9-9fafd205e455',
                '0000ffe0-0000-1000-8000-00805f9b34fb'
            ];
            
            for (const uuid of serviceUUIDs) {
                try {
                    const service = await server.getPrimaryService(uuid);
                    const characteristics = await service.getCharacteristics();
                    
                    for (const char of characteristics) {
                        if (char.properties.write || char.properties.writeWithoutResponse) {
                            this.characteristic = char;
                            this.isConnected = true;
                            this.printerName = device.name;
                            
                            // Save to database
                            await this.savePrinterStatus(device.name);
                            
                            console.log('PrinterManager: Connected to', device.name);
                            this.updateStatusUI('connected');
                            this.showNotification('Printer terhubung: ' + device.name, 'success');
                            
                            // Handle disconnection
                            device.addEventListener('gattserverdisconnected', () => {
                                this.onDisconnected();
                            });
                            
                            return true;
                        }
                    }
                } catch (e) {
                    continue;
                }
            }
            
            throw new Error('No writable characteristic found');
            
        } catch (error) {
            console.error('PrinterManager: Connection error:', error);
            this.isConnected = false;
            this.updateStatusUI('lastknown');
            return false;
        }
    },
    
    // Handle disconnection
    onDisconnected() {
        console.log('PrinterManager: Disconnected');
        this.isConnected = false;
        this.characteristic = null;
        this.updateStatusUI('disconnected');
        this.showNotification('Printer terputus', 'warning');
    },
    
    // Connect to new printer (user initiated)
    async connect() {
        if (!navigator.bluetooth) {
            this.showNotification('Bluetooth tidak didukung di browser ini', 'error');
            return false;
        }
        
        try {
            this.updateStatusUI('connecting');
            
            const device = await navigator.bluetooth.requestDevice({
                acceptAllDevices: true,
                optionalServices: [
                    '000018f0-0000-1000-8000-00805f9b34fb',
                    '0000ff00-0000-1000-8000-00805f9b34fb',
                    '49535343-fe7d-4ae5-8fa9-9fafd205e455',
                    '0000ffe0-0000-1000-8000-00805f9b34fb'
                ]
            });
            
            return await this.connectToDevice(device);
            
        } catch (error) {
            console.error('PrinterManager: Connect error:', error);
            this.isConnected = false;
            this.updateStatusUI('disconnected');
            
            if (error.name !== 'NotFoundError') {
                this.showNotification('Gagal menghubungkan printer: ' + error.message, 'error');
            }
            return false;
        }
    },
    
    // Disconnect printer
    async disconnect() {
        if (this.device && this.device.gatt.connected) {
            this.device.gatt.disconnect();
        }
        this.isConnected = false;
        this.characteristic = null;
        this.printerName = null;
        
        // Clear from database
        await this.savePrinterStatus('');
        
        this.updateStatusUI('disconnected');
        this.showNotification('Printer diputuskan', 'info');
    },
    
    // Save printer status to database
    async savePrinterStatus(printerName) {
        try {
            await fetch('/api/printer-status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ printer_name: printerName })
            });
        } catch (error) {
            console.error('PrinterManager: Error saving printer status:', error);
        }
    },
    
    // Print data
    async print(data) {
        if (!this.isConnected || !this.characteristic) {
            this.showNotification('Printer tidak terhubung', 'error');
            return false;
        }
        
        try {
            const encoder = new TextEncoder();
            const bytes = encoder.encode(data);
            
            // Send in chunks of 100 bytes
            const chunkSize = 100;
            for (let i = 0; i < bytes.length; i += chunkSize) {
                const chunk = bytes.slice(i, i + chunkSize);
                if (this.characteristic.properties.writeWithoutResponse) {
                    await this.characteristic.writeValueWithoutResponse(chunk);
                } else {
                    await this.characteristic.writeValue(chunk);
                }
                await new Promise(resolve => setTimeout(resolve, 50));
            }
            
            return true;
        } catch (error) {
            console.error('PrinterManager: Print error:', error);
            this.showNotification('Gagal mencetak: ' + error.message, 'error');
            return false;
        }
    },
    
    // Update UI status indicator
    updateStatusUI(status) {
        const statusEl = document.getElementById('printer-status');
        const statusText = document.getElementById('printer-status-text');
        const statusDot = document.getElementById('printer-status-dot');
        const actionBtn = document.getElementById('printer-action-btn');
        const autoStatus = document.getElementById('printer-auto-status');
        
        if (!statusEl) return;
        
        statusEl.classList.remove('hidden');
        
        const currentStatus = status || (this.isConnected ? 'connected' : 'disconnected');
        
        switch (currentStatus) {
            case 'connected':
                statusDot.className = 'w-2 h-2 rounded-full bg-green-500';
                statusText.textContent = this.printerName || 'Terhubung';
                statusText.className = 'text-xs text-green-600 truncate max-w-24';
                if (actionBtn) {
                    actionBtn.textContent = 'Putuskan';
                    actionBtn.className = 'text-xs px-2 py-1 rounded bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors';
                }
                if (autoStatus) autoStatus.classList.add('hidden');
                break;
            case 'connecting':
                statusDot.className = 'w-2 h-2 rounded-full bg-yellow-500 animate-pulse';
                statusText.textContent = 'Menghubungkan...';
                statusText.className = 'text-xs text-yellow-600 truncate max-w-24';
                if (actionBtn) {
                    actionBtn.textContent = 'Menunggu...';
                    actionBtn.className = 'text-xs px-2 py-1 rounded bg-yellow-500/20 text-yellow-400';
                }
                if (autoStatus) {
                    autoStatus.textContent = `Auto-reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`;
                    autoStatus.classList.remove('hidden');
                }
                break;
            case 'lastknown':
                statusDot.className = 'w-2 h-2 rounded-full bg-yellow-500';
                statusText.textContent = this.printerName || 'Terakhir terhubung';
                statusText.className = 'text-xs text-yellow-600 truncate max-w-24';
                if (actionBtn) {
                    actionBtn.textContent = 'Hubungkan';
                    actionBtn.className = 'text-xs px-2 py-1 rounded bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors';
                }
                if (autoStatus) {
                    if (this.reconnectAttempts < this.maxReconnectAttempts) {
                        autoStatus.textContent = 'Auto-reconnect aktif...';
                        autoStatus.classList.remove('hidden');
                    } else {
                        autoStatus.textContent = 'Klik tombol untuk hubungkan manual';
                        autoStatus.classList.remove('hidden');
                    }
                }
                break;
            case 'disconnected':
            default:
                statusDot.className = 'w-2 h-2 rounded-full bg-gray-400';
                statusText.textContent = 'Tidak terhubung';
                statusText.className = 'text-xs text-gray-500 truncate max-w-24';
                if (actionBtn) {
                    actionBtn.textContent = 'Hubungkan';
                    actionBtn.className = 'text-xs px-2 py-1 rounded bg-white/10 hover:bg-white/20 transition-colors';
                }
                if (autoStatus) autoStatus.classList.add('hidden');
                break;
        }
    },
    
    // Show notification toast
    showNotification(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-x-full`;
        
        switch (type) {
            case 'success':
                toast.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                toast.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                toast.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                toast.classList.add('bg-blue-500', 'text-white');
        }
        
        toast.innerHTML = `
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
                </svg>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    PrinterManager.init();
});

// Also try to reconnect when page becomes visible (user returns to tab)
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && !PrinterManager.isConnected && PrinterManager.printerName) {
        console.log('PrinterManager: Page visible, attempting reconnect...');
        PrinterManager.reconnectAttempts = 0;
        PrinterManager.autoReconnect();
    }
});

// Expose PrinterManager globally
window.PrinterManager = PrinterManager;
