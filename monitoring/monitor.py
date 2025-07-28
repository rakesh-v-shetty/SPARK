# # #!/usr/bin/env python3
# # """
# # OpenHardwareMonitor Web API Monitor - Clean Version
# # No DLL required! Uses only the built-in web server.
# # Requires: pip install requests
# # """

# # import requests
# # import json
# # import time
# # import os
# # from datetime import datetime

# # class OHMWebMonitor:
# #     def __init__(self, host='localhost', port=8085):
# #         self.base_url = f'http://{host}:{port}'
# #         self.data_url = f'{self.base_url}/data.json'
# #         self.connected = False
        
# #     def test_connection(self):
# #         """Test if OpenHardwareMonitor web server is accessible"""
# #         try:
# #             response = requests.get(self.data_url, timeout=3)
# #             if response.status_code == 200:
# #                 self.connected = True
# #                 return True
# #             else:
# #                 print(f"❌ HTTP Error {response.status_code}")
# #                 return False
# #         except requests.exceptions.ConnectionError:
# #             print("❌ Connection failed. OpenHardwareMonitor web server not accessible.")
# #             return False
# #         except Exception as e:
# #             print(f"❌ Error: {e}")
# #             return False
    
# #     def get_sensor_data(self):
# #         """Fetch all sensor data from OpenHardwareMonitor web API"""
# #         if not self.connected:
# #             return None
            
# #         try:
# #             response = requests.get(self.data_url, timeout=3)
# #             if response.status_code == 200:
# #                 return response.json()
# #             return None
# #         except Exception as e:
# #             print(f"⚠️  Error fetching data: {e}")
# #             return None
    
# #     def parse_sensors(self, data):
# #         """Parse and organize sensor data from JSON"""
# #         sensors = {
# #             'cpu': {'temperatures': [], 'loads': [], 'powers': [], 'clocks': []},
# #             'gpu': {'temperatures': [], 'loads': [], 'powers': [], 'clocks': [], 'fans': []},
# #             'mainboard': {'temperatures': [], 'fans': [], 'voltages': []},
# #             'memory': {'loads': [], 'data': []},
# #             'storage': {'temperatures': [], 'loads': []}
# #         }
        
# #         def extract_number(value_str):
# #             """Extract numeric value from strings like '45.2°C', '50%', etc."""
# #             import re
# #             match = re.search(r'([\d.]+)', value_str)
# #             return float(match.group(1)) if match else 0.0
        
# #         def process_children(children, hardware_name="Unknown"):
# #             """Recursively process sensor data"""
# #             for child in children:
# #                 # Process nested children first
# #                 if 'Children' in child and child['Children']:
# #                     child_hw_name = child.get('Text', hardware_name)
# #                     process_children(child['Children'], child_hw_name)
                
# #                 # Process sensor values
# #                 if 'Value' in child and child['Value'] and child['Value'] != '':
# #                     sensor_info = {
# #                         'name': child.get('Text', 'Unknown'),
# #                         'value': child['Value'],
# #                         'numeric_value': extract_number(child['Value']),
# #                         'min': child.get('Min', ''),
# #                         'max': child.get('Max', ''),
# #                         'hardware': hardware_name
# #                     }
                    
# #                     # Categorize sensors
# #                     text_lower = sensor_info['name'].lower()
# #                     hw_lower = hardware_name.lower()
# #                     value_lower = sensor_info['value'].lower()
                    
# #                     # Temperature sensors
# #                     if '°c' in value_lower or 'temperature' in text_lower:
# #                         if any(x in hw_lower for x in ['cpu', 'processor', 'intel', 'amd', 'core']):
# #                             sensors['cpu']['temperatures'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['gpu', 'nvidia', 'radeon', 'graphics']):
# #                             sensors['gpu']['temperatures'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['mainboard', 'motherboard', 'chipset', 'system']):
# #                             sensors['mainboard']['temperatures'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['storage', 'hdd', 'ssd', 'disk', 'toshiba', 'samsung', 'wd']):
# #                             sensors['storage']['temperatures'].append(sensor_info)
                    
# #                     # Load sensors (percentage)
# #                     elif '%' in value_lower:
# #                         if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
# #                             sensors['cpu']['loads'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['gpu', 'graphics']) or 'gpu' in text_lower:
# #                             sensors['gpu']['loads'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['memory', 'ram']) or 'memory' in text_lower:
# #                             sensors['memory']['loads'].append(sensor_info)
# #                         elif 'used space' in text_lower or 'disk' in text_lower:
# #                             sensors['storage']['loads'].append(sensor_info)
                    
# #                     # Power sensors
# #                     elif ' w' in value_lower or value_lower.endswith('w'):
# #                         if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
# #                             sensors['cpu']['powers'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['gpu', 'graphics']):
# #                             sensors['gpu']['powers'].append(sensor_info)
                    
# #                     # Clock/Frequency sensors
# #                     elif 'mhz' in value_lower or 'ghz' in value_lower:
# #                         if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
# #                             sensors['cpu']['clocks'].append(sensor_info)
# #                         elif any(x in hw_lower for x in ['gpu', 'graphics']) or 'gpu' in text_lower:
# #                             sensors['gpu']['clocks'].append(sensor_info)
                    
# #                     # Fan sensors
# #                     elif 'rpm' in value_lower or 'fan' in text_lower:
# #                         if any(x in hw_lower for x in ['gpu', 'graphics']):
# #                             sensors['gpu']['fans'].append(sensor_info)
# #                         else:
# #                             sensors['mainboard']['fans'].append(sensor_info)
                    
# #                     # Voltage sensors
# #                     elif ' v' in value_lower and ('voltage' in text_lower or 'vcore' in text_lower or '+' in sensor_info['name']):
# #                         sensors['mainboard']['voltages'].append(sensor_info)
                    
# #                     # Memory data
# #                     elif 'gb' in value_lower and any(x in hw_lower for x in ['memory', 'ram']):
# #                         sensors['memory']['data'].append(sensor_info)
        
# #         # Start processing from root
# #         if 'Children' in data:
# #             process_children(data['Children'])
        
# #         return sensors
    
# #     def display_sensors(self, sensors):
# #         """Display formatted sensor data"""
# #         os.system('cls' if os.name == 'nt' else 'clear')
        
# #         print("=" * 85)
# #         print(f"🌐 OpenHardwareMonitor Web Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# #         print("=" * 85)
        
# #         displayed_sections = False
        
# #         # CPU Section
# #         cpu_data = sensors['cpu']
# #         if any(cpu_data.values()):
# #             displayed_sections = True
# #             print("\n🔥 CPU METRICS:")
            
# #             if cpu_data['temperatures']:
# #                 print("   🌡️  Temperatures:")
# #                 for temp in cpu_data['temperatures']:
# #                     min_max = f" (Min: {temp['min']}, Max: {temp['max']})" if temp['min'] or temp['max'] else ""
# #                     print(f"      {temp['name']}: {temp['value']}{min_max}")
            
# #             if cpu_data['loads']:
# #                 print("   📊 Usage:")
# #                 for load in cpu_data['loads']:
# #                     print(f"      {load['name']}: {load['value']}")
            
# #             if cpu_data['powers']:
# #                 print("   ⚡ Power:")
# #                 for power in cpu_data['powers']:
# #                     print(f"      {power['name']}: {power['value']}")
            
# #             if cpu_data['clocks']:
# #                 print("   ⏱️  Frequencies:")
# #                 for clock in cpu_data['clocks']:
# #                     print(f"      {clock['name']}: {clock['value']}")
        
# #         # GPU Section
# #         gpu_data = sensors['gpu']
# #         if any(gpu_data.values()):
# #             displayed_sections = True
# #             print("\n🎮 GPU METRICS:")
            
# #             if gpu_data['temperatures']:
# #                 print("   🌡️  Temperatures:")
# #                 for temp in gpu_data['temperatures']:
# #                     max_temp = f" (Max: {temp['max']})" if temp['max'] else ""
# #                     print(f"      {temp['name']}: {temp['value']}{max_temp}")
            
# #             if gpu_data['loads']:
# #                 print("   📊 Usage:")
# #                 for load in gpu_data['loads']:
# #                     print(f"      {load['name']}: {load['value']}")
            
# #             if gpu_data['powers']:
# #                 print("   ⚡ Power:")
# #                 for power in gpu_data['powers']:
# #                     print(f"      {power['name']}: {power['value']}")
            
# #             if gpu_data['clocks']:
# #                 print("   ⏱️  Frequencies:")
# #                 for clock in gpu_data['clocks']:
# #                     print(f"      {clock['name']}: {clock['value']}")
            
# #             if gpu_data['fans']:
# #                 print("   🌀 Fans:")
# #                 for fan in gpu_data['fans']:
# #                     print(f"      {fan['name']}: {fan['value']}")
        
# #         # System/Mainboard Section
# #         mb_data = sensors['mainboard']
# #         if any(mb_data.values()):
# #             displayed_sections = True
# #             print("\n🔧 SYSTEM METRICS:")
            
# #             if mb_data['temperatures']:
# #                 print("   🌡️  Temperatures:")
# #                 for temp in mb_data['temperatures']:
# #                     print(f"      {temp['name']}: {temp['value']}")
            
# #             if mb_data['fans']:
# #                 print("   🌀 System Fans:")
# #                 for fan in mb_data['fans']:
# #                     print(f"      {fan['name']}: {fan['value']}")
            
# #             if mb_data['voltages']:
# #                 print("   🔌 Voltages:")
# #                 for voltage in mb_data['voltages']:
# #                     print(f"      {voltage['name']}: {voltage['value']}")
        
# #         # Memory Section
# #         mem_data = sensors['memory']
# #         if any(mem_data.values()):
# #             displayed_sections = True
# #             print("\n💾 MEMORY METRICS:")
            
# #             for load in mem_data['loads']:
# #                 print(f"   📊 {load['name']}: {load['value']}")
            
# #             for data in mem_data['data']:
# #                 print(f"   💽 {data['name']}: {data['value']}")
        
# #         # Storage Section
# #         storage_data = sensors['storage']
# #         if any(storage_data.values()):
# #             displayed_sections = True
# #             print("\n💽 STORAGE METRICS:")
            
# #             if storage_data['temperatures']:
# #                 for temp in storage_data['temperatures']:
# #                     print(f"   🌡️  {temp['name']}: {temp['value']}")
            
# #             if storage_data['loads']:
# #                 for load in storage_data['loads']:
# #                     print(f"   📊 {load['name']}: {load['value']}")
        
# #         if not displayed_sections:
# #             print("\n⚠️  No sensor data available or sensors not detected.")
# #             print("   Make sure OpenHardwareMonitor is running and detecting hardware.")
        
# #         print("\n" + "=" * 85)
# #         print("Press Ctrl+C to stop monitoring")
    
# #     def check_critical_temps(self, sensors):
# #         """Monitor for critical temperature values"""
# #         warnings = []
        
# #         # Check CPU temperatures
# #         for temp in sensors['cpu']['temperatures']:
# #             if temp['numeric_value'] > 80:
# #                 warnings.append(f"🚨 HIGH CPU TEMP: {temp['name']} = {temp['value']}")
# #             elif temp['numeric_value'] > 70:
# #                 warnings.append(f"⚠️  CPU TEMP WARNING: {temp['name']} = {temp['value']}")
        
# #         # Check GPU temperatures
# #         for temp in sensors['gpu']['temperatures']:
# #             if temp['numeric_value'] > 85:
# #                 warnings.append(f"🚨 HIGH GPU TEMP: {temp['name']} = {temp['value']}")
# #             elif temp['numeric_value'] > 75:
# #                 warnings.append(f"⚠️  GPU TEMP WARNING: {temp['name']} = {temp['value']}")
        
# #         return warnings

# # def main():
# #     """Main monitoring application"""
# #     print("🌐 OpenHardwareMonitor Web API Monitor")
# #     print("=" * 50)
# #     print("Requirements:")
# #     print("  ✅ OpenHardwareMonitor running")
# #     print("  ✅ Remote Web Server enabled (Options → Remote Web Server → Run)")
# #     print("  ✅ Default port 8085")
# #     print()
    
# #     monitor = OHMWebMonitor()
    
# #     # Test connection
# #     print("🔍 Testing connection...")
# #     if not monitor.test_connection():
# #         print("\n💡 TROUBLESHOOTING:")
# #         print("1. Open OpenHardwareMonitor")
# #         print("2. Go to Options → Remote Web Server")
# #         print("3. Check 'Run' checkbox")
# #         print("4. Verify port is 8085 (or change port in script)")
# #         print("5. Try accessing http://localhost:8085/data.json in browser")
# #         return
    
# #     print("✅ Connected successfully!")
# #     print("🚀 Starting live monitoring...\n")
    
# #     try:
# #         update_count = 0
# #         while True:
# #             data = monitor.get_sensor_data()
            
# #             if data:
# #                 sensors = monitor.parse_sensors(data)
# #                 monitor.display_sensors(sensors)
                
# #                 # Check for temperature warnings
# #                 warnings = monitor.check_critical_temps(sensors)
# #                 if warnings:
# #                     print("\n" + "🔥" * 30)
# #                     print("  TEMPERATURE ALERTS:")
# #                     for warning in warnings:
# #                         print(f"    {warning}")
# #                     print("🔥" * 30)
                
# #                 update_count += 1
# #                 print(f"\n💫 Updates: {update_count} | Refresh rate: 2 seconds")
                
# #             else:
# #                 print("❌ No data received - check OpenHardwareMonitor connection")
            
# #             time.sleep(2)  # Update every 2 seconds
            
# #     except KeyboardInterrupt:
# #         print("\n\n👋 Monitoring stopped by user. Goodbye!")
# #     except Exception as e:
# #         print(f"\n❌ Unexpected error: {e}")
# #         print("💡 Try restarting OpenHardwareMonitor's web server")

# # if __name__ == "__main__":
# #     # Check if requests is available
# #     try:
# #         import requests
# #     except ImportError:
# #         print("❌ Missing dependency!")
# #         print("Install with: pip install requests")
# #         exit(1)
    
# #     main()

# #!/usr/bin/env python3
# """
# OpenHardwareMonitor Temperature Troubleshooting Script
# Helps diagnose why temperature sensors aren't being detected
# """

# import requests
# import json
# import time
# from datetime import datetime

# class OHMTempDebugger:
#     def __init__(self, host='localhost', port=8085):
#         self.base_url = f'http://{host}:{port}'
#         self.data_url = f'{self.base_url}/data.json'
        
#     def get_raw_data(self):
#         """Fetch raw sensor data for analysis"""
#         try:
#             response = requests.get(self.data_url, timeout=3)
#             if response.status_code == 200:
#                 return response.json()
#             return None
#         except Exception as e:
#             print(f"Error fetching data: {e}")
#             return None
    
#     def find_all_sensors(self, data, path="root"):
#         """Recursively find ALL sensors in the JSON data"""
#         sensors = []
        
#         def recursive_search(obj, current_path):
#             if isinstance(obj, dict):
#                 # Check if this is a sensor node
#                 if 'Text' in obj and 'Value' in obj:
#                     sensor_info = {
#                         'path': current_path,
#                         'text': obj.get('Text', ''),
#                         'value': obj.get('Value', ''),
#                         'min': obj.get('Min', ''),
#                         'max': obj.get('Max', ''),
#                         'type': obj.get('SensorType', ''),
#                         'id': obj.get('id', '')
#                     }
#                     sensors.append(sensor_info)
                
#                 # Continue searching in children
#                 for key, value in obj.items():
#                     if key == 'Children' and isinstance(value, list):
#                         for i, child in enumerate(value):
#                             child_path = f"{current_path}/{obj.get('Text', f'item_{i}')}"
#                             recursive_search(child, child_path)
#                     elif isinstance(value, (dict, list)):
#                         recursive_search(value, f"{current_path}/{key}")
            
#             elif isinstance(obj, list):
#                 for i, item in enumerate(obj):
#                     recursive_search(item, f"{current_path}[{i}]")
        
#         recursive_search(data, path)
#         return sensors
    
#     def categorize_sensors(self, sensors):
#         """Categorize sensors by type and hardware"""
#         categories = {
#             'temperature': [],
#             'voltage': [],
#             'fan': [],
#             'load': [],
#             'power': [],
#             'clock': [],
#             'data': [],
#             'other': []
#         }
        
#         for sensor in sensors:
#             value_lower = sensor['value'].lower()
#             text_lower = sensor['text'].lower()
            
#             # Temperature detection
#             if ('°c' in value_lower or 'celsius' in value_lower or 
#                 'temperature' in text_lower or 'temp' in text_lower):
#                 categories['temperature'].append(sensor)
            
#             # Voltage detection
#             elif ('v' in value_lower and any(x in text_lower for x in ['voltage', 'vcore', 'vdd', '+3.3', '+5', '+12'])):
#                 categories['voltage'].append(sensor)
            
#             # Fan detection
#             elif ('rpm' in value_lower or 'fan' in text_lower):
#                 categories['fan'].append(sensor)
            
#             # Load/Usage detection
#             elif '%' in value_lower:
#                 categories['load'].append(sensor)
            
#             # Power detection
#             elif ('w' in value_lower and ('power' in text_lower or 'watt' in text_lower)):
#                 categories['power'].append(sensor)
            
#             # Clock/Frequency detection
#             elif ('mhz' in value_lower or 'ghz' in value_lower or 'clock' in text_lower):
#                 categories['clock'].append(sensor)
            
#             # Data (GB, MB, etc.)
#             elif any(unit in value_lower for unit in ['gb', 'mb', 'kb', 'tb']):
#                 categories['data'].append(sensor)
            
#             else:
#                 categories['other'].append(sensor)
        
#         return categories
    
#     def analyze_temperature_absence(self, categories):
#         """Analyze why temperature sensors might be missing"""
#         temp_sensors = categories['temperature']
        
#         print("\n" + "="*80)
#         print("🔍 TEMPERATURE SENSOR ANALYSIS")
#         print("="*80)
        
#         if temp_sensors:
#             print(f"✅ Found {len(temp_sensors)} temperature sensor(s):")
#             for temp in temp_sensors:
#                 print(f"   📍 {temp['path']}")
#                 print(f"      Name: {temp['text']}")
#                 print(f"      Value: {temp['value']}")
#                 print(f"      Type: {temp['type']}")
#                 print(f"      Min/Max: {temp['min']} / {temp['max']}")
#                 print()
#         else:
#             print("❌ NO TEMPERATURE SENSORS FOUND!")
#             print("\nPossible causes:")
#             print("1. 🔧 Hardware sensors not enabled in BIOS/UEFI")
#             print("2. 💻 Your CPU/Motherboard doesn't expose temp sensors")
#             print("3. 🛠️  OpenHardwareMonitor needs admin privileges")
#             print("4. 🔌 Sensor drivers not installed")
#             print("5. 📊 Sensors exist but with unexpected naming")
            
#             print("\n🔍 Let's check for sensors with suspicious names...")
#             suspicious_sensors = []
            
#             for category, sensors in categories.items():
#                 for sensor in sensors:
#                     if any(keyword in sensor['text'].lower() for keyword in 
#                           ['thermal', 'cpu', 'core', 'die', 'junction', 'tj']):
#                         suspicious_sensors.append(sensor)
            
#             if suspicious_sensors:
#                 print(f"🧐 Found {len(suspicious_sensors)} potentially temperature-related sensors:")
#                 for sensor in suspicious_sensors:
#                     print(f"   ❓ {sensor['text']}: {sensor['value']} (in {category})")
#             else:
#                 print("🤷 No suspicious sensors found either.")
    
#     def run_full_diagnosis(self):
#         """Run complete temperature diagnosis"""
#         print("🌡️  OpenHardwareMonitor Temperature Diagnostics")
#         print("="*60)
#         print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         print()
        
#         # Get raw data
#         print("📡 Fetching sensor data...")
#         raw_data = self.get_raw_data()
        
#         if not raw_data:
#             print("❌ Failed to get sensor data!")
#             print("\nTroubleshooting steps:")
#             print("1. Ensure OpenHardwareMonitor is running")
#             print("2. Enable Remote Web Server (Options → Remote Web Server → Run)")
#             print("3. Check if http://localhost:8085/data.json works in browser")
#             return
        
#         print("✅ Data received successfully!")
        
#         # Find all sensors
#         print("\n🔍 Scanning for all sensors...")
#         all_sensors = self.find_all_sensors(raw_data)
#         print(f"📊 Total sensors found: {len(all_sensors)}")
        
#         # Categorize sensors
#         categories = self.categorize_sensors(all_sensors)
        
#         # Show sensor summary
#         print("\n📋 SENSOR SUMMARY:")
#         print("-" * 40)
#         for category, sensors in categories.items():
#             if sensors:
#                 print(f"   {category.upper()}: {len(sensors)} sensors")
        
#         # Analyze temperature sensors specifically
#         self.analyze_temperature_absence(categories)
        
#         # Show all sensors for debugging
#         print("\n" + "="*80)
#         print("🗂️  COMPLETE SENSOR LIST (for debugging)")
#         print("="*80)
        
#         for category, sensors in categories.items():
#             if sensors:
#                 print(f"\n📁 {category.upper()} SENSORS:")
#                 for sensor in sensors:
#                     print(f"   • {sensor['text']}: {sensor['value']}")
#                     if sensor['type']:
#                         print(f"     Type: {sensor['type']}")
#                     print(f"     Path: {sensor['path']}")
#                     print()
        
#         # Hardware detection tips
#         print("\n" + "="*80)
#         print("💡 HARDWARE-SPECIFIC TIPS")
#         print("="*80)
#         print("🔸 Intel CPUs: Look for 'Intel CPU' or 'Core' in hardware list")
#         print("🔸 AMD CPUs: Look for 'AMD CPU' or processor name")
#         print("🔸 Laptop users: Some laptops block temperature access")
#         print("🔸 Modern systems: May need 'Run as Administrator'")
#         print("🔸 Alternative tools: HWiNFO64, Core Temp, CPU-Z")
        
#         # Save detailed log
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         log_file = f'ohm_debug_{timestamp}.json'
        
#         try:
#             with open(log_file, 'w') as f:
#                 debug_data = {
#                     'timestamp': datetime.now().isoformat(),
#                     'total_sensors': len(all_sensors),
#                     'categories': {k: len(v) for k, v in categories.items()},
#                     'all_sensors': all_sensors,
#                     'raw_data': raw_data
#                 }
#                 json.dump(debug_data, f, indent=2)
#             print(f"\n💾 Detailed debug data saved to: {log_file}")
#         except Exception as e:
#             print(f"\n⚠️  Could not save debug log: {e}")

# def main():
#     debugger = OHMTempDebugger()
#     debugger.run_full_diagnosis()

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
OpenHardwareMonitor Web API Monitor - Fixed Temperature Detection
Works with your Dell Latitude 7 system!
"""

import requests
import json
import time
import os
from datetime import datetime

class OHMWebMonitor:
    def __init__(self, host='localhost', port=8085):
        self.base_url = f'http://{host}:{port}'
        self.data_url = f'{self.base_url}/data.json'
        self.connected = False
        
    def test_connection(self):
        """Test if OpenHardwareMonitor web server is accessible"""
        try:
            response = requests.get(self.data_url, timeout=3)
            if response.status_code == 200:
                self.connected = True
                return True
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed. OpenHardwareMonitor web server not accessible.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_sensor_data(self):
        """Fetch all sensor data from OpenHardwareMonitor web API"""
        if not self.connected:
            return None
            
        try:
            response = requests.get(self.data_url, timeout=3)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"⚠️  Error fetching data: {e}")
            return None
    
    def parse_sensors(self, data):
        """Parse and organize sensor data from JSON - FIXED TEMPERATURE DETECTION"""
        sensors = {
            'cpu': {'temperatures': [], 'loads': [], 'powers': [], 'clocks': []},
            'gpu': {'temperatures': [], 'loads': [], 'powers': [], 'clocks': [], 'fans': []},
            'mainboard': {'temperatures': [], 'fans': [], 'voltages': []},
            'memory': {'loads': [], 'data': []},
            'storage': {'temperatures': [], 'loads': []}
        }
        
        def extract_number(value_str):
            """Extract numeric value from strings like '45.2°C', '50%', etc."""
            import re
            if not value_str:
                return 0.0
            match = re.search(r'([\d.]+)', str(value_str))
            return float(match.group(1)) if match else 0.0
        
        def process_children(children, hardware_name="Unknown", parent_path=""):
            """Recursively process sensor data with better detection"""
            for child in children:
                current_path = f"{parent_path}/{child.get('Text', 'Unknown')}"
                
                # Process nested children first
                if 'Children' in child and child['Children']:
                    child_hw_name = child.get('Text', hardware_name)
                    process_children(child['Children'], child_hw_name, current_path)
                
                # Process sensor values - ONLY if there's an actual value
                if ('Value' in child and child['Value'] and 
                    child['Value'] != '' and child['Value'] is not None):
                    
                    sensor_info = {
                        'name': child.get('Text', 'Unknown'),
                        'value': child['Value'],
                        'numeric_value': extract_number(child['Value']),
                        'min': child.get('Min', ''),
                        'max': child.get('Max', ''),
                        'hardware': hardware_name,
                        'path': current_path
                    }
                    
                    # Better categorization logic
                    text_lower = sensor_info['name'].lower()
                    hw_lower = hardware_name.lower()
                    value_str = str(sensor_info['value']).lower()
                    
                    # FIXED: Temperature detection (look for °C in value OR temperature keywords)
                    if ('°c' in value_str or 'celsius' in value_str or 
                        'temperature' in text_lower or 'temp' in text_lower or
                        ('cpu core' in text_lower and sensor_info['numeric_value'] > 20)):
                        
                        # Determine hardware category
                        if any(x in hw_lower for x in ['cpu', 'processor', 'intel', 'amd', 'core']) or 'cpu' in text_lower:
                            sensors['cpu']['temperatures'].append(sensor_info)
                        elif any(x in hw_lower for x in ['gpu', 'nvidia', 'radeon', 'graphics']):
                            sensors['gpu']['temperatures'].append(sensor_info)
                        elif any(x in hw_lower for x in ['storage', 'hdd', 'ssd', 'disk', 'toshiba', 'samsung', 'wd', 'nvme', 'm.2']):
                            sensors['storage']['temperatures'].append(sensor_info)
                        else:
                            sensors['mainboard']['temperatures'].append(sensor_info)
                    
                    # Load sensors (percentage)
                    elif '%' in value_str:
                        if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
                            sensors['cpu']['loads'].append(sensor_info)
                        elif any(x in hw_lower for x in ['gpu', 'graphics']) or 'gpu' in text_lower:
                            sensors['gpu']['loads'].append(sensor_info)
                        elif any(x in hw_lower for x in ['memory', 'ram']) or 'memory' in text_lower:
                            sensors['memory']['loads'].append(sensor_info)
                        elif 'used space' in text_lower or 'disk' in text_lower:
                            sensors['storage']['loads'].append(sensor_info)
                    
                    # Power sensors
                    elif ' w' in value_str or value_str.endswith('w'):
                        if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
                            sensors['cpu']['powers'].append(sensor_info)
                        elif any(x in hw_lower for x in ['gpu', 'graphics']):
                            sensors['gpu']['powers'].append(sensor_info)
                    
                    # Clock/Frequency sensors
                    elif 'mhz' in value_str or 'ghz' in value_str:
                        if any(x in hw_lower for x in ['cpu', 'processor']) or 'cpu' in text_lower:
                            sensors['cpu']['clocks'].append(sensor_info)
                        elif any(x in hw_lower for x in ['gpu', 'graphics']) or 'gpu' in text_lower:
                            sensors['gpu']['clocks'].append(sensor_info)
                    
                    # Fan sensors
                    elif 'rpm' in value_str or 'fan' in text_lower:
                        if any(x in hw_lower for x in ['gpu', 'graphics']):
                            sensors['gpu']['fans'].append(sensor_info)
                        else:
                            sensors['mainboard']['fans'].append(sensor_info)
                    
                    # Voltage sensors
                    elif ' v' in value_str and ('voltage' in text_lower or 'vcore' in text_lower or '+' in sensor_info['name']):
                        sensors['mainboard']['voltages'].append(sensor_info)
                    
                    # Memory data
                    elif 'gb' in value_str and any(x in hw_lower for x in ['memory', 'ram']):
                        sensors['memory']['data'].append(sensor_info)
        
        # Start processing from root
        if 'Children' in data:
            process_children(data['Children'])
        
        return sensors
    
    def display_sensors(self, sensors):
        """Display formatted sensor data with temperatures!"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 85)
        print(f"🌐 OpenHardwareMonitor Web Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 85)
        
        displayed_sections = False
        
        # CPU Section
        cpu_data = sensors['cpu']
        if any(cpu_data.values()):
            displayed_sections = True
            print("\n🔥 CPU METRICS:")
            
            if cpu_data['temperatures']:
                print("   🌡️  Temperatures:")
                for temp in cpu_data['temperatures']:
                    min_max = f" (Min: {temp['min']}, Max: {temp['max']})" if temp['min'] or temp['max'] else ""
                    # Color coding for temperature
                    temp_val = temp['numeric_value']
                    if temp_val > 80:
                        status = "🚨"
                    elif temp_val > 70:
                        status = "⚠️ "
                    elif temp_val > 60:
                        status = "🔶"
                    else:
                        status = "✅"
                    print(f"      {status} {temp['name']}: {temp['value']}{min_max}")
            
            if cpu_data['loads']:
                print("   📊 Usage:")
                for load in cpu_data['loads']:
                    print(f"      {load['name']}: {load['value']}")
            
            if cpu_data['powers']:
                print("   ⚡ Power:")
                for power in cpu_data['powers']:
                    print(f"      {power['name']}: {power['value']}")
            
            if cpu_data['clocks']:
                print("   ⏱️  Frequencies:")
                for clock in cpu_data['clocks']:
                    print(f"      {clock['name']}: {clock['value']}")
        
        # GPU Section (if any GPU detected)
        gpu_data = sensors['gpu']
        if any(gpu_data.values()):
            displayed_sections = True
            print("\n🎮 GPU METRICS:")
            
            if gpu_data['temperatures']:
                print("   🌡️  Temperatures:")
                for temp in gpu_data['temperatures']:
                    max_temp = f" (Max: {temp['max']})" if temp['max'] else ""
                    print(f"      {temp['name']}: {temp['value']}{max_temp}")
            
            if gpu_data['loads']:
                print("   📊 Usage:")
                for load in gpu_data['loads']:
                    print(f"      {load['name']}: {load['value']}")
        
        # System/Mainboard Section
        mb_data = sensors['mainboard']
        if any(mb_data.values()):
            displayed_sections = True
            print("\n🔧 SYSTEM METRICS:")
            
            if mb_data['temperatures']:
                print("   🌡️  System Temperatures:")
                for temp in mb_data['temperatures']:
                    print(f"      {temp['name']}: {temp['value']}")
            
            if mb_data['fans']:
                print("   🌀 System Fans:")
                for fan in mb_data['fans']:
                    print(f"      {fan['name']}: {fan['value']}")
        
        # Memory Section
        mem_data = sensors['memory']
        if any(mem_data.values()):
            displayed_sections = True
            print("\n💾 MEMORY METRICS:")
            
            for load in mem_data['loads']:
                print(f"   📊 {load['name']}: {load['value']}")
            
            for data in mem_data['data']:
                print(f"   💽 {data['name']}: {data['value']}")
        
        # Storage Section
        storage_data = sensors['storage']
        if any(storage_data.values()):
            displayed_sections = True
            print("\n💽 STORAGE METRICS:")
            
            if storage_data['temperatures']:
                print("   🌡️  SSD Temperature:")
                for temp in storage_data['temperatures']:
                    temp_val = temp['numeric_value']
                    status = "🔥" if temp_val > 50 else "❄️" if temp_val < 30 else "✅"
                    min_max = f" (Range: {temp['min']} - {temp['max']})" if temp['min'] or temp['max'] else ""
                    print(f"      {status} {temp['name']}: {temp['value']}{min_max}")
            
            if storage_data['loads']:
                for load in storage_data['loads']:
                    print(f"   📊 {load['name']}: {load['value']}")
        
        if not displayed_sections:
            print("\n⚠️  No sensor data available.")
        
        print("\n" + "=" * 85)
        print("Press Ctrl+C to stop monitoring")
    
    def check_critical_temps(self, sensors):
        """Monitor for critical temperature values"""
        warnings = []
        
        # Check CPU temperatures
        for temp in sensors['cpu']['temperatures']:
            if temp['numeric_value'] > 80:
                warnings.append(f"🚨 HIGH CPU TEMP: {temp['name']} = {temp['value']}")
            elif temp['numeric_value'] > 75:
                warnings.append(f"⚠️  CPU TEMP WARNING: {temp['name']} = {temp['value']}")
        
        # Check storage temperatures
        for temp in sensors['storage']['temperatures']:
            if temp['numeric_value'] > 60:
                warnings.append(f"🚨 HIGH SSD TEMP: {temp['name']} = {temp['value']}")
            elif temp['numeric_value'] > 50:
                warnings.append(f"⚠️  SSD TEMP WARNING: {temp['name']} = {temp['value']}")
        
        return warnings

def main():
    """Main monitoring application"""
    print("🌐 OpenHardwareMonitor Web API Monitor - FIXED VERSION")
    print("=" * 60)
    print("✅ Temperature detection fixed for your Dell Latitude!")
    print()
    
    monitor = OHMWebMonitor()
    
    # Test connection
    print("🔍 Testing connection...")
    if not monitor.test_connection():
        print("\n💡 TROUBLESHOOTING:")
        print("1. Open OpenHardwareMonitor")
        print("2. Go to Options → Remote Web Server")
        print("3. Check 'Run' checkbox")
        print("4. Verify port is 8085")
        return
    
    print("✅ Connected successfully!")
    print("🚀 Starting live monitoring with TEMPERATURE data...\n")
    
    try:
        update_count = 0
        while True:
            data = monitor.get_sensor_data()
            
            if data:
                sensors = monitor.parse_sensors(data)
                monitor.display_sensors(sensors)
                
                # Check for temperature warnings
                warnings = monitor.check_critical_temps(sensors)
                if warnings:
                    print("\n" + "🔥" * 30)
                    print("  TEMPERATURE ALERTS:")
                    for warning in warnings:
                        print(f"    {warning}")
                    print("🔥" * 30)
                
                update_count += 1
                print(f"\n💫 Updates: {update_count} | Refresh rate: 2 seconds")
                
                # Quick debug info
                cpu_temps = len(sensors['cpu']['temperatures'])
                storage_temps = len(sensors['storage']['temperatures'])
                if cpu_temps or storage_temps:
                    print(f"🌡️  Tracking {cpu_temps} CPU + {storage_temps} SSD temperature sensors")
                
            else:
                print("❌ No data received - check connection")
            
            time.sleep(2)  # Update every 2 seconds
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()