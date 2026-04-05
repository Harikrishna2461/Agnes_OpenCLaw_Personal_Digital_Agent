#!/usr/bin/env python3
"""
Quick wrapper to start WhatsApp server with TensorFlow disabled.
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import sys
sys.argv.append('--port')
sys.argv.append('5001')

# Run the server
from whatsapp_server import start_server
start_server(host="0.0.0.0", port=5001, debug=False)
