# -*- coding: utf-8 -*-
"""
Patches build_complete_game.py and build_engine_assets.py to implement:
1. Portrait Rotation Enforcement Overlay (#rotate-device-overlay)
2. Comprehensive Responsive Landscape CSS for all device screen sizes and aspect ratios (including mobile safe areas and low-height viewports)
3. Fullscreen & Landscape Orientation Lock API integration in JS
"""

import sys

def patch_complete_game():
    with open('build_complete_game.py', 'r', encoding='utf-8') as f:
        content = f.read()

    css_target = """.perf-chip-btn.active {
      border-color: var(--blue-bright);
      background: rgba(56, 189, 248, 0.15);
      color: #fff;
    }
  </style>"""

    responsive_css = """.perf-chip-btn.active {
      border-color: var(--blue-bright);
      background: rgba(56, 189, 248, 0.15);
      color: #fff;
    }

    /* ==========================================================================
       RESPONSIVE LANDSCAPE & ORIENTATION SYSTEM FOR ALL DEVICES
       ========================================================================== */

    /* Portrait Rotation Enforcement Overlay */
    #rotate-device-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: radial-gradient(circle at 50% 35%, #0f1c3f 0%, #060b18 100%);
      z-index: 99999;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 24px;
      text-align: center;
      color: #fff;
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
    }

    /* Auto show in portrait orientation on mobile / tablets */
    @media screen and (orientation: portrait) {
      #rotate-device-overlay {
        display: flex !important;
      }
    }

    .rotate-phone-box {
      position: relative;
      width: 110px;
      height: 110px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;
    }

    .phone-anim-device {
      width: 50px;
      height: 90px;
      border: 3.5px solid var(--gold-light);
      border-radius: 12px;
      background: rgba(15, 23, 42, 0.95);
      position: relative;
      box-shadow: 0 0 35px rgba(245, 158, 11, 0.5);
      animation: rotateDeviceLoop 3s ease-in-out infinite;
      transform-origin: center center;
    }

    .phone-notch {
      width: 18px;
      height: 4px;
      background: var(--gold-light);
      border-radius: 2px;
      position: absolute;
      top: 4px;
      left: 50%;
      transform: translateX(-50%);
    }

    .phone-screen-glare {
      position: absolute;
      top: 12px;
      left: 5px;
      right: 5px;
      bottom: 8px;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.3) 0%, rgba(255, 255, 255, 0.05) 100%);
      border-radius: 6px;
    }

    .rotate-curved-arrow {
      position: absolute;
      font-size: 32px;
      bottom: -4px;
      right: 6px;
      animation: spinArrow 3s linear infinite;
    }

    @keyframes rotateDeviceLoop {
      0%, 15% { transform: rotate(0deg); }
      45%, 70% { transform: rotate(-90deg); }
      85%, 100% { transform: rotate(0deg); }
    }

    @keyframes spinArrow {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .rotate-badge {
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 2px;
      color: var(--gold-primary);
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .rotate-title {
      font-size: clamp(20px, 4vw, 28px);
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #fff;
      margin-bottom: 10px;
    }

    .rotate-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      max-width: 380px;
      line-height: 1.5;
      margin-bottom: 22px;
    }

    .btn-rotate-fullscreen {
      background: linear-gradient(135deg, var(--gold-light), var(--gold-primary));
      color: #000;
      border: none;
      padding: 12px 26px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.5);
      transition: transform 0.15s;
    }

    .btn-rotate-fullscreen:active {
      transform: scale(0.96);
    }

    /* SAFE AREA PADDING FOR NOTCHES & HOME INDICATORS */
    body {
      padding-left: env(safe-area-inset-left);
      padding-right: env(safe-area-inset-right);
      padding-top: env(safe-area-inset-top);
      padding-bottom: env(safe-area-inset-bottom);
    }

    /* COMPACT MOBILE LANDSCAPE (< 540px viewport height) */
    @media (max-height: 540px) {
      .screen-view {
        padding: 10px 16px 52px 16px;
      }
      .main-logo-text {
        font-size: clamp(22px, 4.2vw, 36px);
      }
      .menu-brand-box {
        margin-bottom: 10px;
      }
      .menu-button-group {
        width: 260px;
        gap: 6px;
        margin-bottom: 10px;
      }
      .btn-menu {
        padding: 8px 14px;
        font-size: 12px;
      }
      .menu-quote {
        display: none;
      }

      /* In-Game HUD Elements */
      #hud-overlay {
        padding: 8px 12px;
      }
      .hud-top-left {
        top: 8px;
        left: 8px;
        gap: 8px;
      }
      .radar-circle {
        width: 58px;
        height: 58px;
      }
      .radar-loc-chip {
        padding: 2px 8px;
        font-size: 10px;
      }
      .hud-mission-banner {
        top: 8px;
        padding: 4px 14px;
        border-radius: 20px;
        gap: 8px;
      }
      .mission-badge-icon {
        font-size: 14px;
      }
      .mission-label {
        font-size: 8px;
      }
      .mission-goal {
        font-size: 11px;
      }
      #emote-banner {
        top: 48px;
        padding: 3px 12px;
        font-size: 11px;
      }
      .hud-top-right {
        top: 8px;
        right: 8px;
        gap: 5px;
      }
      .hud-stat-pill {
        padding: 4px 9px;
        font-size: 10px;
        border-radius: 12px;
      }
      .pill-cash, .pill-level {
        display: none;
      }
      
      /* Global Dock */
      #global-dock {
        bottom: 3px;
        padding: 3px 8px;
        gap: 4px;
      }
      .dock-btn {
        padding: 4px 8px;
        font-size: 9px;
        gap: 4px;
      }

      /* Bottom Row Controls */
      .hud-bottom-row {
        bottom: 40px;
        left: 10px;
        right: 10px;
      }
      .hud-chat-box {
        width: 220px;
        padding: 5px 8px;
        font-size: 9px;
        gap: 3px;
        max-height: 45px;
        overflow: hidden;
      }
      .joystick-zone {
        width: 78px;
        height: 78px;
      }
      .joystick-knob {
        width: 32px;
        height: 32px;
      }
      .hud-action-round {
        width: 36px;
        height: 36px;
        font-size: 14px;
      }
      .hud-action-column {
        gap: 5px;
      }
      #action-prompt {
        bottom: 48px;
        padding: 6px 18px;
        font-size: 12px;
      }
      #driving-hud {
        bottom: 48px;
        padding: 6px 18px;
      }
      .speed-gauge {
        font-size: 18px;
      }

      /* Modals on Mobile Landscape */
      #emote-modal {
        max-width: 96vw;
        max-height: 90vh;
        padding: 12px 16px;
      }
      .emote-grid {
        grid-template-columns: repeat(6, 1fr) !important;
        gap: 4px;
        max-height: 62vh;
      }
      .emote-card-btn {
        padding: 5px 3px;
        gap: 2px;
      }
      .emote-card-icon {
        font-size: 16px;
      }
      .emote-card-name {
        font-size: 9px;
      }

      #dialogue-modal {
        bottom: 38px;
        padding: 12px 16px;
        max-height: 72vh;
        overflow-y: auto;
      }
      .dialogue-text {
        font-size: 13px;
        line-height: 1.35;
      }
      .dialogue-opt {
        padding: 8px 12px;
        font-size: 12px;
      }
      #pause-modal {
        max-height: 90vh;
        overflow-y: auto;
        padding: 14px;
      }
    }
  </style>"""

    if css_target in content:
        content = content.replace(css_target, responsive_css, 1)
        print("Patched CSS in build_complete_game.py")
    else:
        print("CSS target not found in build_complete_game.py")

    html_target = """<body>
  <!-- 3D Canvas Container -->
  <div id="canvas-container"></div>"""

    responsive_html = """<body>
  <!-- ROTATE DEVICE TO LANDSCAPE OVERLAY (Mobile & Tablet Portrait Detection) -->
  <div id="rotate-device-overlay">
    <div class="rotate-phone-box">
      <div class="phone-anim-device">
        <div class="phone-notch"></div>
        <div class="phone-screen-glare"></div>
      </div>
      <div class="rotate-curved-arrow">🔄</div>
    </div>
    <div class="rotate-badge">👑 KINGMAKERS OF INDIAN POLITICS</div>
    <h2 class="rotate-title">PLEASE ROTATE TO LANDSCAPE</h2>
    <p class="rotate-subtitle">
      Chennai 3D streets, vehicle simulation, and political campaign missions are optimized for landscape orientation. Turn your device horizontally or click below.
    </p>
    <button class="btn-rotate-fullscreen" id="btn-request-landscape" onclick="requestLandscapeOrientation()">
      🔄 Enter Landscape Fullscreen
    </button>
  </div>

  <!-- 3D Canvas Container -->
  <div id="canvas-container"></div>"""

    if html_target in content:
        content = content.replace(html_target, responsive_html, 1)
        print("Patched HTML overlay in build_complete_game.py")
    else:
        print("HTML target not found in build_complete_game.py")

    with open('build_complete_game.py', 'w', encoding='utf-8') as f:
        f.write(content)


def patch_engine_assets():
    with open('build_engine_assets.py', 'r', encoding='utf-8') as f:
        content = f.read()

    resize_target = """    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    updateTaskHUD();
    applyGraphicsPreset('medium');
    animate();"""

    responsive_js = """    // Landscape Mode Request & Fullscreen API
    window.requestLandscapeOrientation = function() {
      const docEl = document.documentElement;
      const rfs = docEl.requestFullscreen || docEl.webkitRequestFullscreen || docEl.mozRequestFullScreen || docEl.msRequestFullscreen;
      if (rfs) {
        try {
          rfs.call(docEl).then(() => {
            if (screen.orientation && screen.orientation.lock) {
              screen.orientation.lock('landscape').catch(() => {});
            }
          }).catch(() => {});
        } catch (err) {}
      }
      const overlay = document.getElementById('rotate-device-overlay');
      if (overlay && window.innerWidth > window.innerHeight) {
        overlay.style.display = 'none';
      }
    };

    function checkOrientationChange() {
      const overlay = document.getElementById('rotate-device-overlay');
      const isPortrait = window.innerHeight > window.innerWidth && window.innerWidth <= 1024;
      if (overlay) {
        if (isPortrait) {
          overlay.style.display = 'flex';
        } else {
          overlay.style.display = 'none';
        }
      }
      if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      }
    }

    window.addEventListener('resize', checkOrientationChange);
    window.addEventListener('orientationchange', () => {
      setTimeout(checkOrientationChange, 200);
      setTimeout(checkOrientationChange, 600);
    });

    checkOrientationChange();

    updateTaskHUD();
    applyGraphicsPreset('medium');
    animate();"""

    if resize_target in content:
        content = content.replace(resize_target, responsive_js, 1)
        print("Patched Engine resize & landscape handler in build_engine_assets.py")
    else:
        print("Resize target not found in build_engine_assets.py")

    with open('build_engine_assets.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_complete_game()
    patch_engine_assets()
