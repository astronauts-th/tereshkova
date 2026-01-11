import machine
import socket
import network

# Ensure Wi-Fi is connected
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("Wi-Fi not connected. Please run your Wi-Fi connection script first!")
    raise SystemExit
ip = wlan.ifconfig()[0]
print("ESP32 Web Server Running at: http://" + ip)

# Set up LED (for an external LED wired as active-high)
led = machine.Pin(5, machine.Pin.OUT)
led.value(0)  # Assuming active-high: 0 means LED off

# Create and bind socket to port 80
s = socket.socket()
addr = ('0.0.0.0', 80)
s.bind(addr)
s.listen(5)
print("Listening on", addr)

def generate_page(message=""):
    html = """<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tereshkova | Women's Safety Reimagined</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary-green: #8AAD6A;
      --dark-green: #3D4B35;
      --off-white: #F8F9F5;
      --pure-white: #FFFFFF;
      --transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Outfit', sans-serif;
      scroll-behavior: smooth;
    }

    body {
      background-color: var(--off-white);
      color: var(--dark-green);
      overflow-x: hidden;
      transition: background-color 0.5s ease;
    }

    /* --- Utility Classes --- */
    .hidden {
      display: none !important;
    }

    .fade-in {
      animation: fadeIn 0.8s forwards;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(20px);
      }

      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* --- Navigation --- */
    nav {
      position: fixed;
      top: 0;
      width: 100%;
      padding: 30px 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
    }

    .brand {
      font-size: 1.5rem;
      font-weight: 300;
      letter-spacing: 0.4rem;
      text-transform: uppercase;
      cursor: pointer;
      transition: var(--transition);
    }

    .brand:hover {
      opacity: 0.7;
      letter-spacing: 0.5rem;
    }

    /* --- APP VIEW (The Alert Button) --- */
    #app-view {
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: var(--off-white);
    }

    .alert-container {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .alert-button {
      width: 220px;
      height: 220px;
      background-color: var(--primary-green);
      border: 10px solid var(--pure-white);
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 20px 40px rgba(138, 173, 106, 0.2);
      transition: var(--transition);
      z-index: 5;
      outline: none;
    }

    .alert-button:hover {
      transform: translateY(-8px) scale(1.02);
      box-shadow: 0 30px 60px rgba(138, 173, 106, 0.3);
    }

    .alert-button:active {
      transform: translateY(2px) scale(0.95);
    }

    .icon-svg {
      width: 100px;
      height: 100px;
      fill: var(--pure-white);
    }

    .pulse-ring {
      position: absolute;
      width: 200px;
      height: 200px;
      border: 3px solid var(--primary-green);
      border-radius: 50%;
      opacity: 0;
      pointer-events: none;
    }

    .animate-rings {
      animation: pulse-out 1.2s ease-out forwards;
    }

    @keyframes pulse-out {
      0% {
        transform: scale(1);
        opacity: 0.8;
      }

      100% {
        transform: scale(2.8);
        opacity: 0;
      }
    }

    .status {
      margin-top: 50px;
      font-size: 0.9rem;
      font-weight: 700;
      letter-spacing: 0.3rem;
      text-transform: uppercase;
      opacity: 0.4;
    }

    /* --- LANDING VIEW --- */
    #landing-view {
      padding-top: 150px;
      min-height: 100vh;
    }

    .section {
      padding: 100px 60px;
      max-width: 1400px;
      margin: 0 auto;
    }

    .hero {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 80px;
      align-items: center;
      margin-bottom: 100px;
    }

    .hero-text h1 {
      font-size: 5rem;
      font-weight: 700;
      line-height: 0.9;
      margin-bottom: 30px;
      color: var(--dark-green);
    }

    .hero-text p {
      font-size: 1.2rem;
      line-height: 1.6;
      opacity: 0.8;
      max-width: 500px;
    }

    .hero-illustration {
      position: relative;
      height: 500px;
      background: var(--pure-white);
      border-radius: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 40px 100px rgba(0, 0, 0, 0.05);
    }

    /* --- Grid Layout (Inspired by Reference) --- */
    .feature-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 30px;
      margin: 60px 0;
    }

    .feature-item {
      background: var(--dark-green);
      color: var(--pure-white);
      padding: 60px 40px;
      border-radius: 4px;
      transition: var(--transition);
    }

    .feature-item:hover {
      transform: translateY(-10px);
    }

    .feature-item h3 {
      font-size: 1.5rem;
      margin-bottom: 15px;
      color: var(--primary-green);
    }

    .content-block {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 100px;
      margin-top: 150px;
      align-items: center;
    }

    .content-image {
      background: var(--primary-green);
      height: 600px;
      border-radius: 4px;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }

    .content-text h2 {
      font-size: 3rem;
      margin-bottom: 25px;
    }

    /* --- SVGS --- */
    .svg-placeholder {
      width: 100%;
      height: auto;
      max-width: 400px;
    }

    /* --- Footer --- */
    footer {
      padding: 100px 60px;
      border-top: 1px solid rgba(0, 0, 0, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .close-landing {
      background: var(--dark-green);
      color: var(--pure-white);
      border: none;
      padding: 15px 40px;
      border-radius: 30px;
      cursor: pointer;
      font-weight: 500;
      transition: var(--transition);
    }

    .close-landing:hover {
      letter-spacing: 0.1rem;
      opacity: 0.9;
    }

    /* Toast */
    .toast {
      position: fixed;
      top: 40px;
      right: 40px;
      background: var(--dark-green);
      color: var(--pure-white);
      padding: 15px 30px;
      border-radius: 4px;
      transform: translateX(200%);
      transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
      z-index: 2000;
    }

    .toast.show {
      transform: translateX(0);
    }

    /* --- Responsive Styling --- */
    @media (max-width: 1024px) {
      .hero-text h1 {
        font-size: 4rem;
      }

      .content-block {
        gap: 50px;
      }
    }

    @media (max-width: 768px) {
      nav {
        padding: 20px 30px;
      }

      .section {
        padding: 60px 30px;
      }

      .hero {
        grid-template-columns: 1fr;
        gap: 40px;
        text-align: center;
      }

      .hero-text h1 {
        font-size: 3.5rem;
      }

      .hero-text p {
        max-width: 100%;
        margin: 0 auto;
      }

      .hero-illustration {
        height: 350px;
      }

      .feature-grid {
        grid-template-columns: 1fr;
      }

      .content-block {
        grid-template-columns: 1fr;
        gap: 40px;
        margin-top: 80px;
      }

      .content-block,
      .content-block[style*="direction: rtl"] {
        direction: ltr !important;
      }

      .content-image {
        height: 400px;
      }

      .content-text {
        text-align: center;
      }

      .content-text h2 {
        font-size: 2.5rem;
      }

      footer {
        flex-direction: column;
        gap: 30px;
        text-align: center;
        padding: 60px 30px;
      }

      .toast {
        top: auto;
        bottom: 40px;
        right: 20px;
        left: 20px;
        transform: translateY(200%);
      }

      .toast.show {
        transform: translateY(0);
      }
    }

    @media (max-width: 480px) {
      .hero-text h1 {
        font-size: 2.8rem;
      }

      .alert-button {
        width: 180px;
        height: 180px;
      }

      .icon-svg {
        width: 80px;
        height: 80px;
      }

      @keyframes pulse-out {
        0% {
          transform: scale(0.8);
          opacity: 0.8;
        }

        100% {
          transform: scale(2.2);
          opacity: 0;
        }
      }
    }
  </style>
</head>

<body>

  <nav>
    <div class="brand" id="brandBtn">tereshkova</div>
    <div style="font-size: 0.8rem; opacity: 0.5;">V1.0.4</div>
  </nav>

  <!-- MAIN ALERT APP VIEW -->
  <section id="app-view">
    <div class="alert-container" id="alertContainer">
      <button class="alert-button" id="alertBtn" aria-label="Trigger Alert">
        <svg class="icon-svg" viewBox="0 0 24 24">
          <path
            d="M12 22C13.1 22 14 21.1 14 20H10C10 21.1 10.9 22 12 22ZM18 16V11C18 7.93 16.37 5.36 13.5 4.68V4C13.5 3.17 12.83 2.5 12 2.5C11.17 2.5 10.5 3.17 10.5 4V4.68C7.63 5.36 6 7.92 6 11V16L4 18V19H20V18L18 16ZM16 17H8V11C8 8.52 9.51 6.5 12 6.5C14.49 6.5 16 8.52 16 11V17Z" />
        </svg>
      </button>
    </div>
    <div class="status" id="status">Secure Standby</div>
  </section>

  <!-- LANDING PAGE VIEW -->
  <section id="landing-view" class="hidden">
    <div class="section">
      <div class="hero">
        <div class="hero-text fade-in">
          <h1>Silent Presence.</h1>
          <p>Designed for women, Tereshkova provides a discrete way to reclaim your space in public transportation
            without confrontation.</p>
        </div>
        <div class="hero-illustration fade-in">
          <!-- Illustration: User in a train environment -->
          <svg viewBox="0 0 400 400" class="svg-placeholder">
            <rect x="50" y="50" width="300" height="300" rx="20" fill="#f0f2ed" stroke="#8AAD6A" stroke-width="2" />
            <circle cx="200" cy="180" r="60" fill="#8AAD6A" opacity="0.2" />
            <path d="M150 280Q200 240 250 280" stroke="#8AAD6A" stroke-width="4" fill="none" stroke-linecap="round" />
            <rect x="180" y="100" width="40" height="120" rx="5" fill="#8AAD6A" />
          </svg>
        </div>
      </div>

      <div class="feature-grid">
        <div class="feature-item">
          <h3>Discretion First</h3>
          <p>Trigger alerts via your phone or wearable without anyone around you noticing. No shouting, no scene.</p>
        </div>
        <div class="feature-item">
          <h3>Proximity Audio</h3>
          <p>Automatically connects to the nearest public address system or bluetooth station to produce a sharp,
            situational alert sound.</p>
        </div>
        <div class="feature-item">
          <h3>Immediate Reach</h3>
          <p>Low-latency transmission ensures your request for space or attention is heard the moment you feel
            uncomfortable.</p>
        </div>
      </div>

      <div class="content-block">
        <div class="content-image">
          <!-- Illustration: Connection to speaker -->
          <svg viewBox="0 0 400 400" class="svg-placeholder">
            <circle cx="200" cy="200" r="100" fill="white" opacity="0.3" />
            <path d="M200 150V250M150 200H250" stroke="white" stroke-width="8" stroke-linecap="round" />
            <path d="M100 100L300 300" stroke="white" stroke-width="2" stroke-dasharray="10 10" />
          </svg>
        </div>
        <div class="content-text">
          <h2>The House Method.</h2>
          <p>Named after Valentina Tereshkova, the first woman in space, this system is built on the philosophy of
            "Absolute Space". When a woman feels her personal boundaries are being crossed in a train, bus, or metro,
            the system acts as her voice.</p>
          <p style="margin-top: 20px;">The audio alert is designed to be firm but professional—mimicking a station
            announcement—to naturally diffuse uncomfortable situations.</p>
        </div>
      </div>

      <div class="content-block" style="direction: rtl;">
        <div class="content-image" style="background: var(--dark-green);">
          <svg viewBox="0 0 400 400" class="svg-placeholder">
            <rect x="100" y="100" width="200" height="200" fill="#8AAD6A" />
            <circle cx="200" cy="200" r="50" fill="white" />
          </svg>
        </div>
        <div class="content-text" style="direction: ltr;">
          <h2>Public & Private.</h2>
          <p>We blend into the infrastructure. Tereshkova nodes are installed in train bogies, allowing your device to
            handshake with the onboard speaker system locally and securely.</p>
        </div>
      </div>
    </div>

    <footer>
      <div style="font-weight: 300; opacity: 0.6;">&copy; 2026 Tereshkova Systems. All Rights Reserved.</div>
      <button class="close-landing" id="backBtn">Return to Alert Panel</button>
    </footer>
  </section>

  <div class="toast" id="toast">Signal broadcasted to Station Node 04</div>

  <script>
    const appView = document.getElementById('app-view');
    const landingView = document.getElementById('landing-view');
    const brandBtn = document.getElementById('brandBtn');
    const backBtn = document.getElementById('backBtn');
    const alertBtn = document.getElementById('alertBtn');
    const alertContainer = document.getElementById('alertContainer');
    const status = document.getElementById('status');
    const toast = document.getElementById('toast');

    // Logic to switch views
    brandBtn.addEventListener('click', () => {
      appView.classList.add('hidden');
      landingView.classList.remove('hidden');
      window.scrollTo(0, 0);
      document.body.style.backgroundColor = 'var(--off-white)';
    });

    backBtn.addEventListener('click', () => {
      landingView.classList.add('hidden');
      appView.classList.remove('hidden');
    });

    // Alert logic
    let isActive = false;
    alertBtn.addEventListener('click', () => {
      if (isActive) return;
      isActive = true;

      // Pulse effect
      for (let i = 0; i < 2; i++) {
        const ring = document.createElement('div');
        ring.classList.add('pulse-ring', 'animate-rings');
        ring.style.animationDelay = `${i * 0.2}s`;
        alertContainer.appendChild(ring);
        setTimeout(() => ring.remove(), 1200);
      }

      status.textContent = "Transmitting...";
      status.style.opacity = "1";
      toast.classList.add('show');

      setTimeout(() => {
        toast.classList.remove('show');
        status.textContent = "Secure Standby";
        status.style.opacity = "0.4";
        isActive = false;
      }, 3000);
    });
  </script>
</body>

</html>""" % message
    return html

while True:
    conn, client_addr = s.accept()
    print("Client connected from", client_addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    message = ""
    # Process the request to update LED status
    if "GET /on" in request:
        led.value(1)  # Turn LED ON (active-high)
        message = "LED is ON"
    elif "GET /off" in request:
        led.value(0)  # Turn LED OFF (active-high)
        message = "LED is OFF"
    
    # Always serve the main page with the updated status message
    response_body = generate_page(message)
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response_body
    conn.send(response.encode())
    conn.close()
