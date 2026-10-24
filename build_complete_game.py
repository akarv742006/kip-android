# -*- coding: utf-8 -*-
"""
Kingmakers of Indian Politics - Comprehensive Game Builder
Assembles the complete, state-of-the-art WebGL simulation into:
  - index.html
  - docs/index.html
  - WebPreview/index.html
"""
import sys

print("Writing complete game code...")

# We will construct the parts and join them
part_css_html = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0">
  <title>Kingmakers of Indian Politics - Chennai City & Character Simulation</title>
  <style>
    :root {
      --bg-dark: #070d18;
      --bg-card: rgba(13, 23, 42, 0.94);
      --bg-card-hover: rgba(22, 38, 70, 0.98);
      --border-subtle: rgba(255, 255, 255, 0.1);
      --border-glow: rgba(56, 189, 248, 0.45);
      --gold-primary: #f59e0b;
      --gold-light: #fbbf24;
      --gold-restrained: #d97706;
      --blue-accent: #0284c7;
      --blue-bright: #38bdf8;
      --blue-navy: #0f172a;
      --green-accent: #10b981;
      --purple-accent: #8b5cf6;
      --red-accent: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: var(--bg-dark);
      color: var(--text-main);
    }

    /* 3D WebGL Canvas */
    #canvas-container {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }

    /* Overlay Screens */
    .screen-view {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 20;
      display: none;
      background: radial-gradient(circle at 50% 30%, rgba(15, 25, 48, 0.96) 0%, rgba(4, 8, 18, 0.99) 100%);
      backdrop-filter: blur(16px);
      overflow-y: auto;
      padding: 24px 24px 80px 24px;
      animation: fadeIn 0.25s ease forwards;
    }
    .screen-view.active {
      display: flex;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.99); }
      to { opacity: 1; transform: scale(1); }
    }

    /* Bottom Master Navigation Dock */
    #global-dock {
      position: absolute;
      bottom: 8px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 100;
      display: flex;
      gap: 6px;
      background: rgba(10, 18, 34, 0.95);
      border: 1px solid var(--border-glow);
      border-radius: 40px;
      padding: 6px 14px;
      backdrop-filter: blur(18px);
      box-shadow: 0 10px 40px rgba(0,0,0,0.85);
      max-width: 96vw;
      overflow-x: auto;
    }
    .dock-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 7px 13px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .dock-btn:hover {
      color: #fff;
      background: rgba(255,255,255,0.08);
    }
    .dock-btn.active {
      color: #000;
      background: linear-gradient(135deg, var(--gold-light), var(--gold-primary));
      box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }

    /* MAIN MENU SCREEN */
    #screen-main-menu {
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      padding-left: clamp(30px, 8vw, 100px);
      background: linear-gradient(90deg, rgba(4, 9, 20, 0.96) 0%, rgba(7, 14, 28, 0.8) 50%, rgba(4, 8, 16, 0.96) 100%),
                  radial-gradient(ellipse at 70% 50%, rgba(245, 158, 11, 0.15) 0%, transparent 60%);
    }
    .menu-brand-box {
      margin-bottom: 24px;
    }
    .crown-icon {
      font-size: 36px;
      color: var(--gold-primary);
      margin-bottom: -4px;
      display: inline-block;
      animation: floatGently 3s ease-in-out infinite alternate;
    }
    @keyframes floatGently {
      from { transform: translateY(0); }
      to { transform: translateY(-4px); }
    }
    .main-logo-text {
      font-size: clamp(32px, 5.5vw, 56px);
      font-weight: 900;
      letter-spacing: 2px;
      line-height: 1.05;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, var(--gold-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-transform: uppercase;
    }
    .main-tagline {
      font-size: 13px;
      letter-spacing: 4px;
      color: var(--text-muted);
      font-weight: 700;
      margin-top: 6px;
      text-transform: uppercase;
    }
    .menu-button-group {
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 290px;
      margin-bottom: 24px;
    }
    .btn-menu {
      background: rgba(15, 25, 48, 0.85);
      border: 1px solid var(--border-subtle);
      color: #fff;
      padding: 13px 20px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 700;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.2s;
    }
    .btn-menu:hover {
      background: var(--bg-card-hover);
      border-color: var(--blue-bright);
      transform: translateX(6px);
    }
    .btn-menu.primary {
      background: linear-gradient(135deg, var(--gold-light), var(--gold-primary));
      color: #000;
      border: none;
      box-shadow: 0 6px 25px rgba(245, 158, 11, 0.4);
    }
    .menu-quote {
      font-style: italic;
      color: var(--text-muted);
      font-size: 14px;
      border-left: 3px solid var(--gold-primary);
      padding-left: 12px;
      max-width: 400px;
      line-height: 1.5;
    }

    /* IN-GAME AAA HUD OVERLAY */
    #hud-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      pointer-events: none;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px;
    }
    .hud-top-left {
      position: absolute;
      top: 16px;
      left: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      pointer-events: auto;
    }
    .radar-circle {
      width: 88px;
      height: 88px;
      border-radius: 50%;
      background: rgba(10, 18, 34, 0.88);
      border: 2px solid var(--border-glow);
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
      position: relative;
      overflow: hidden;
    }
    .radar-north-tag {
      position: absolute;
      top: 4px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 9px;
      font-weight: 900;
      color: var(--blue-bright);
    }
    .radar-loc-chip {
      background: rgba(10, 18, 34, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 700;
      color: var(--gold-light);
    }
    .hud-mission-banner {
      position: absolute;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(13, 23, 42, 0.92);
      border: 1px solid var(--border-glow);
      border-radius: 30px;
      padding: 8px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      pointer-events: auto;
      cursor: pointer;
      transition: all 0.2s;
    }
    .hud-mission-banner:hover {
      background: rgba(22, 38, 70, 0.98);
      border-color: var(--gold-primary);
    }
    .mission-badge-icon {
      font-size: 18px;
    }
    .mission-texts {
      display: flex;
      flex-direction: column;
    }
    .mission-label {
      font-size: 10px;
      font-weight: 800;
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .mission-goal {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
    }
    #emote-banner {
      position: absolute;
      top: 76px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(14, 165, 233, 0.92);
      color: #fff;
      padding: 6px 18px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      display: none;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(14, 165, 233, 0.5);
      pointer-events: none;
      animation: bounceIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes bounceIn {
      0% { transform: translate(-50%, -10px) scale(0.9); opacity: 0; }
      100% { transform: translate(-50%, 0) scale(1); opacity: 1; }
    }
    .hud-top-right {
      position: absolute;
      top: 16px;
      right: 16px;
      display: flex;
      gap: 8px;
      align-items: center;
      pointer-events: auto;
    }
    .hud-stat-pill {
      background: rgba(13, 23, 42, 0.88);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
      backdrop-filter: blur(10px);
    }
    .pill-cash {
      color: var(--green-accent);
    }
    .pill-level {
      color: var(--gold-light);
    }
    .pill-perf {
      font-family: monospace;
      font-size: 11px;
      color: var(--blue-bright);
      cursor: pointer;
    }
    .pill-btn {
      cursor: pointer;
      transition: background 0.2s;
    }
    .pill-btn:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--blue-bright);
    }

    #action-prompt {
      position: absolute;
      bottom: 110px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(13, 23, 42, 0.95);
      border: 2px solid var(--gold-primary);
      border-radius: 30px;
      padding: 10px 28px;
      color: #fff;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.5px;
      box-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
      pointer-events: auto;
      cursor: pointer;
      display: none;
      animation: pulseGlow 1.5s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { transform: translateX(-50%) scale(1); box-shadow: 0 0 20px rgba(245, 158, 11, 0.4); }
      50% { transform: translateX(-50%) scale(1.04); box-shadow: 0 0 35px rgba(245, 158, 11, 0.8); }
    }

    #driving-hud {
      position: absolute;
      bottom: 90px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(10, 18, 34, 0.92);
      border: 1px solid var(--border-glow);
      border-radius: 18px;
      padding: 12px 28px;
      display: none;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      pointer-events: auto;
    }
    .speed-gauge {
      font-size: 26px;
      font-weight: 900;
      font-family: monospace;
      color: var(--gold-light);
    }

    .hud-bottom-row {
      position: absolute;
      bottom: 60px;
      left: 16px;
      right: 16px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      pointer-events: none;
    }
    .hud-chat-box {
      width: clamp(260px, 32vw, 360px);
      background: rgba(10, 18, 34, 0.78);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 11px;
      backdrop-filter: blur(8px);
      pointer-events: auto;
    }
    .chat-row {
      line-height: 1.35;
    }
    .chat-user {
      font-weight: 700;
      color: var(--blue-bright);
      margin-right: 4px;
    }
    .chat-msg {
      color: #cbd5e1;
    }

    .joystick-zone {
      width: 110px;
      height: 110px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.06);
      border: 2px dashed rgba(255, 255, 255, 0.2);
      position: relative;
      pointer-events: auto;
      touch-action: none;
    }
    .joystick-knob {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--gold-light), var(--gold-primary));
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      box-shadow: 0 4px 15px rgba(245, 158, 11, 0.5);
    }

    .hud-action-column {
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: auto;
    }
    .hud-action-round {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: rgba(13, 23, 42, 0.9);
      border: 2px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 18px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
      transition: all 0.15s;
    }
    .hud-action-round:active {
      transform: scale(0.92);
      background: var(--blue-accent);
      border-color: var(--blue-bright);
    }

    /* EMOTE MODAL (EXACT 6x3 GRID OF 18 EMOTES MATCHING REFERENCE IMAGE) */
    #emote-modal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 92%;
      max-width: 660px;
      background: rgba(13, 23, 42, 0.98);
      backdrop-filter: blur(20px);
      border: 1.5px solid var(--border-glow);
      border-radius: 20px;
      padding: 22px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.85);
      display: none;
      flex-direction: column;
      gap: 14px;
      pointer-events: auto;
      z-index: 120;
    }
    .emote-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 10px;
    }
    .emote-modal-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--gold-light);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .emote-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
      font-weight: 700;
    }
    .emote-close-btn:hover {
      color: #fff;
    }
    .emote-grid {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      max-height: 56vh;
      overflow-y: auto;
      padding-right: 4px;
    }
    @media (max-width: 680px) {
      .emote-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    .emote-card-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 10px 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      color: #e2e8f0;
      cursor: pointer;
      transition: all 0.18s;
      text-align: center;
    }
    .emote-card-btn:hover {
      background: rgba(56, 189, 248, 0.18);
      border-color: var(--blue-bright);
      transform: translateY(-2px);
      color: #fff;
    }
    .emote-card-icon {
      font-size: 24px;
    }
    .emote-card-name {
      font-size: 11px;
      font-weight: 700;
      line-height: 1.2;
    }

    /* PAUSE MENU MODAL */
    #pause-modal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 88%;
      max-width: 440px;
      background: rgba(13, 23, 42, 0.98);
      backdrop-filter: blur(20px);
      border: 1.5px solid var(--border-glow);
      border-radius: 20px;
      padding: 26px;
      box-shadow: 0 25px 70px rgba(0,0,0,0.9);
      display: none;
      flex-direction: column;
      gap: 14px;
      pointer-events: auto;
      z-index: 150;
      text-align: center;
    }
    .pause-title {
      font-size: 22px;
      font-weight: 900;
      letter-spacing: 1.5px;
      color: var(--gold-light);
    }
    .pause-button-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 8px;
    }

    /* Dialogue Modal */
    #dialogue-modal {
      position: absolute;
      bottom: 60px;
      left: 50%;
      transform: translateX(-50%);
      width: 92%;
      max-width: 720px;
      background: rgba(13, 23, 42, 0.98);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 16px;
      padding: 22px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.85);
      display: none;
      flex-direction: column;
      gap: 14px;
      pointer-events: auto;
      z-index: 60;
    }
    .dialogue-speaker {
      font-size: 16px;
      font-weight: 800;
      color: var(--gold-light);
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .dialogue-text {
      font-size: 15px;
      line-height: 1.55;
      color: #e2e8f0;
    }
    .dialogue-options {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .dialogue-opt {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 10px;
      padding: 12px 16px;
      color: #cbd5e1;
      font-size: 14px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s;
    }
    .dialogue-opt:hover {
      background: #1e3a8a;
      border-color: var(--blue-bright);
      color: #fff;
      transform: translateX(5px);
    }

    /* Level Complete Victory Modal */
    #level-complete-modal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 90%;
      max-width: 540px;
      background: rgba(13, 23, 42, 0.98);
      border: 2px solid var(--green-accent);
      border-radius: 24px;
      padding: 30px;
      box-shadow: 0 0 60px rgba(16, 185, 129, 0.4);
      display: none;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      text-align: center;
      pointer-events: auto;
      z-index: 100;
    }

    /* Shared Card & Dashboards */
    .grid-dashboard {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 18px;
      width: 100%;
      max-width: 1280px;
      margin: 0 auto;
    }
    .screen-header-title {
      font-size: 22px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 18px;
      color: #fff;
    }
    .dash-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .card-top-title {
      font-size: 14px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .action-row-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(18, 30, 54, 0.7);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 10px;
      padding: 10px 14px;
      gap: 12px;
    }
    .action-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .action-icon-circle {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: rgba(255,255,255,0.08);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 16px;
    }
    .action-info h4 {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
    }
    .action-info p {
      font-size: 11px;
      color: var(--text-muted);
    }
    .btn-action-trigger {
      background: var(--blue-accent);
      border: none;
      color: #fff;
      padding: 7px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
      white-space: nowrap;
    }
    .btn-action-trigger:hover {
      background: #0284c7;
    }

    /* SCENARIO CARDS (MATCHING REFERENCE IMAGE) */
    .scenario-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 18px;
      width: 100%;
      max-width: 1280px;
      margin: 0 auto;
    }
    .scenario-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      transition: transform 0.2s, border-color 0.2s;
    }
    .scenario-card:hover {
      transform: translateY(-4px);
      border-color: var(--blue-bright);
    }
    .scenario-banner {
      height: 120px;
      background: linear-gradient(135deg, #1e3a8a, #0369a1);
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 42px;
    }
    .scenario-content {
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
    }
    .scenario-tag {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--gold-light);
    }
    .scenario-title {
      font-size: 17px;
      font-weight: 800;
      color: #fff;
    }
    .scenario-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.45;
      flex: 1;
    }
    .scenario-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid var(--border-subtle);
    }

    /* CHARACTER ROSTER CARDS (13 ROSTER MEMBERS MATCHING REFERENCE IMAGE) */
    .roster-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      width: 100%;
      max-width: 1280px;
      margin: 0 auto;
    }
    .char-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
      transition: all 0.2s;
      cursor: pointer;
    }
    .char-card:hover {
      border-color: var(--gold-primary);
      transform: translateY(-3px);
      background: var(--bg-card-hover);
    }
    .char-card-header {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .char-avatar-circle {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 2px solid var(--gold-light);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 24px;
      flex-shrink: 0;
    }
    .char-meta h3 {
      font-size: 15px;
      font-weight: 800;
      color: #fff;
    }
    .char-meta span {
      font-size: 11px;
      font-weight: 700;
      color: var(--blue-bright);
    }
    .char-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.4;
    }
    .char-stats-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #cbd5e1;
      background: rgba(0,0,0,0.25);
      padding: 6px 10px;
      border-radius: 8px;
    }

    /* ELECTION RESULTS TV SCREEN (EXACT MATCH TO REFERENCE IMAGE) */
    .election-broadcast-screen {
      background: linear-gradient(180deg, #0b1528 0%, #060a14 100%);
      border: 2px solid var(--border-glow);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 15px 50px rgba(0,0,0,0.8);
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .broadcast-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid rgba(255,255,255,0.1);
      padding-bottom: 12px;
    }
    .live-badge {
      background: #ef4444;
      color: #fff;
      font-size: 11px;
      font-weight: 900;
      padding: 3px 10px;
      border-radius: 4px;
      letter-spacing: 1px;
      animation: pulseLive 1s infinite alternate;
    }
    @keyframes pulseLive {
      from { opacity: 0.8; }
      to { opacity: 1; transform: scale(1.05); }
    }
    .election-bars-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .election-bar-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .election-bar-header {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      font-weight: 800;
    }
    .election-bar-track {
      width: 100%;
      height: 28px;
      background: rgba(255,255,255,0.06);
      border-radius: 6px;
      overflow: hidden;
      position: relative;
    }
    .election-bar-fill {
      height: 100%;
      display: flex;
      align-items: center;
      padding-left: 12px;
      font-weight: 900;
      font-size: 13px;
      color: #fff;
      transition: width 1s ease-out;
    }
    .election-winner-spotlight {
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid var(--green-accent);
      border-radius: 12px;
      padding: 14px 20px;
    }

    /* CAREER PROGRESSION DASHBOARD (EXACT MATCH TO REFERENCE IMAGE) */
    .career-hero-card {
      background: linear-gradient(135deg, rgba(15, 25, 48, 0.95), rgba(30, 58, 138, 0.4));
      border: 1.5px solid var(--gold-primary);
      border-radius: 18px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .career-hero-top {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    .career-avatar-box {
      width: 80px;
      height: 80px;
      border-radius: 16px;
      border: 2px solid var(--gold-light);
      background: rgba(245, 158, 11, 0.15);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 40px;
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    }
    .career-xp-track {
      width: 100%;
      height: 12px;
      background: rgba(255,255,255,0.08);
      border-radius: 6px;
      overflow: hidden;
    }
    .career-xp-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--gold-primary), var(--gold-light));
      border-radius: 6px;
      width: 64%;
    }
    .rep-bar-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 8px;
    }
    .rep-bar-label-line {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 700;
    }
    .rep-track {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 4px;
      overflow: hidden;
    }
    .rep-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.3s ease;
    }

    /* Graphics Quality Selector in Settings */
    .perf-options-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin: 12px 0;
    }
    .perf-chip-btn {
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.05);
      border: 1.5px solid var(--border-subtle);
      border-radius: 10px;
      color: #cbd5e1;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }
    .perf-chip-btn.active {
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
        padding: 12px 16px 54px 16px;
      }
      #screen-main-menu {
        justify-content: flex-start !important;
        align-items: flex-start;
        overflow-y: auto;
        padding: 14px 16px 60px clamp(20px, 6vw, 60px);
      }
      .crown-icon {
        font-size: 24px;
        margin-bottom: -2px;
      }
      .main-logo-text {
        font-size: clamp(20px, 3.8vw, 30px);
        line-height: 1.1;
      }
      .main-tagline {
        font-size: 9px;
        letter-spacing: 2px;
        margin-top: 3px;
      }
      .menu-brand-box {
        margin-bottom: 8px;
      }
      .menu-button-group {
        width: min(260px, 85vw);
        gap: 4px;
        margin-bottom: 8px;
      }
      .btn-menu {
        padding: 6px 12px;
        font-size: 11px;
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
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script>
    if (typeof THREE === 'undefined') {
      document.write('<script src="https://unpkg.com/three@0.128.0/build/three.min.js"><\/script>');
    }
  </script>
</head>
<body>
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
  <div id="canvas-container"></div>

  <!-- SCREEN 1: MAIN MENU (100% English) -->
  <div class="screen-view active" id="screen-main-menu">
    <div class="menu-brand-box">
      <div class="crown-icon">👑</div>
      <h1 class="main-logo-text">KINGMAKERS<br>OF INDIAN POLITICS</h1>
      <div class="main-tagline">BUILD TRUST • LEAD THE PEOPLE • SHAPE THE FUTURE</div>
    </div>

    <div class="menu-button-group">
      <button class="btn-menu primary" id="btn-continue-game">▶ Enter 3D Chennai (Play Level 1)</button>
      <button class="btn-menu" id="btn-menu-scenarios">🎬 In-Game Scenarios (6 Modes)</button>
      <button class="btn-menu" id="btn-menu-roster">👥 Character Roster & Cast</button>
      <button class="btn-menu" id="btn-open-campaign">📢 Campaign Strategy</button>
      <button class="btn-menu" id="btn-open-election">🗳️ Election Results 2027</button>
      <button class="btn-menu" id="btn-open-char">📊 Career Progression</button>
      <button class="btn-menu" id="btn-open-settings">⚙️ Settings & Performance</button>
    </div>

    <div class="menu-quote">
      "In the democracy of Tamil Nadu, water is not merely a utility—it is the crown of the people's trust."
    </div>
  </div>

  <!-- SCREEN 2: IN-GAME AAA HUD (100% English) -->
  <div id="hud-overlay" style="display: none;">
    <!-- Top Left Real-Time Minimap & Location -->
    <div class="hud-top-left">
      <div class="radar-circle">
        <canvas id="minimap-canvas" width="88" height="88"></canvas>
        <span class="radar-north-tag">N</span>
      </div>
      <div>
        <div class="radar-loc-chip">📍 Chennai Ward 12</div>
        <div style="font-size: 10px; color: var(--text-muted); margin-top: 3px; font-weight: 600;">Dr. Radhakrishnan Avenue</div>
      </div>
    </div>

    <!-- Center Mission Banner -->
    <div class="hud-mission-banner" id="mission-banner" onclick="handleCurrentTask()">
      <div class="mission-badge-icon">🎯</div>
      <div class="mission-texts">
        <span class="mission-label">Ward 12 Water Crisis Mission</span>
        <span class="mission-goal" id="mission-goal-text">Task 1: Meet Ward Member Karuppasamy</span>
      </div>
    </div>

    <!-- Active Emote Floating Banner -->
    <div id="emote-banner">
      <span id="emote-banner-icon">🙏</span>
      <span id="emote-banner-text">Emote Active: Namaste</span>
    </div>

    <!-- Top Right Stats, Emote Button, Pause & FPS -->
    <div class="hud-top-right">
      <div class="hud-stat-pill pill-btn" onclick="openEmoteMenu()" title="Open Emote System [T]">🎭 Emotes</div>
      <div class="hud-stat-pill pill-btn" onclick="openPauseMenu()" title="Pause Game [Esc]">⏸️ Pause</div>
      <div class="hud-stat-pill pill-perf" id="hud-fps-pill" title="Toggle Graphics Preset" onclick="cycleGraphicsPreset()">60 FPS [MED]</div>
      <div class="hud-stat-pill pill-cash" id="hud-cash-val">₹ 2,45,000</div>
      <div class="hud-stat-pill pill-level">Level 5</div>
    </div>

    <!-- Action Prompt Overlay -->
    <div id="action-prompt" onclick="handleInteraction()">[E] Tap to Interact</div>

    <!-- Driving Gauge Overlay -->
    <div id="driving-hud">
      <span class="speed-gauge" id="speed-gauge">🚗 0 KM/H</span>
      <span style="font-size: 12px; color: #cbd5e1;">WASD / Joystick to Drive • [H] Honk Horn</span>
      <button class="btn-action-trigger" style="background: #ef4444;" onclick="exitCar()">Exit Ambassador</button>
    </div>

    <!-- Bottom Controls & Social Chatter -->
    <div class="hud-bottom-row">
      <!-- Public City Chatter Box -->
      <div class="hud-chat-box">
        <div class="chat-row"><span class="chat-user">Selvam (Ward 12):</span><span class="chat-msg">Tanker rates surged to ₹2000! Arun please intervene!</span></div>
        <div class="chat-row"><span class="chat-user">News Tamil 24:</span><span class="chat-msg">Bye-election campaigns intensify across Chennai.</span></div>
        <div class="chat-row"><span class="chat-user" style="color: #f59e0b;">System:</span><span class="chat-msg" id="sys-event-msg">Task 1: Walk to the local party office.</span></div>
      </div>

      <!-- Virtual Joystick for Touch / Mouse Drag -->
      <div class="joystick-zone" id="joystick-zone">
        <div class="joystick-knob" id="joystick-knob"></div>
      </div>

      <!-- Action Touch Buttons -->
      <div class="hud-action-column">
        <div class="hud-action-round" id="act-talk" title="Talk / Interact [E]" onclick="handleInteraction()">🗣️</div>
        <div class="hud-action-round" id="act-emote" title="Emotes [T]" onclick="openEmoteMenu()">🎭</div>
        <div class="hud-action-round" id="act-sprint" title="Sprint [Shift]">🏃</div>
        <div class="hud-action-round" id="act-car" title="Drive Vehicle [F]" onclick="toggleCarDrive()">🚗</div>
        <div class="hud-action-round" id="act-horn" title="Honk Horn [H]" onclick="playCarHorn()">📢</div>
      </div>
    </div>
  </div>

  <!-- EMOTE MODAL (EXACT 6x3 GRID OF 18 EMOTES MATCHING REFERENCE IMAGE) -->
  <div id="emote-modal">
    <div class="emote-modal-header">
      <div class="emote-modal-title"><span>🎭</span><span>Character Emotes & Expressions (18)</span></div>
      <button class="emote-close-btn" onclick="closeEmoteMenu()">✕</button>
    </div>
    <div class="emote-grid">
      <div class="emote-card-btn" onclick="triggerEmote('smile')">
        <span class="emote-card-icon">😊</span>
        <span class="emote-card-name">Smile / Happy</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('confident')">
        <span class="emote-card-icon">🦸</span>
        <span class="emote-card-name">Confident</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('wave')">
        <span class="emote-card-icon">👋</span>
        <span class="emote-card-name">Wave</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('namaste')">
        <span class="emote-card-icon">🙏</span>
        <span class="emote-card-name">Greeting</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('thumbsup')">
        <span class="emote-card-icon">👍</span>
        <span class="emote-card-name">Thumbs Up</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('point')">
        <span class="emote-card-icon">👉</span>
        <span class="emote-card-name">Pointing</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('speech')">
        <span class="emote-card-icon">🎙️</span>
        <span class="emote-card-name">Public Speech</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('listen')">
        <span class="emote-card-icon">✋</span>
        <span class="emote-card-name">Listening</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('angry')">
        <span class="emote-card-icon">😠</span>
        <span class="emote-card-name">Angry</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('sad')">
        <span class="emote-card-icon">😔</span>
        <span class="emote-card-name">Sad</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('worried')">
        <span class="emote-card-icon">😟</span>
        <span class="emote-card-name">Worried</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('thinking')">
        <span class="emote-card-icon">🤔</span>
        <span class="emote-card-name">Thinking</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('handshake')">
        <span class="emote-card-icon">🤝</span>
        <span class="emote-card-name">Handshake</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('celebrate')">
        <span class="emote-card-icon">🎉</span>
        <span class="emote-card-name">Victory</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('defeat')">
        <span class="emote-card-icon">🤦</span>
        <span class="emote-card-name">Defeat</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('apologize')">
        <span class="emote-card-icon">🙇</span>
        <span class="emote-card-name">Apologize</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('thank')">
        <span class="emote-card-icon">💖</span>
        <span class="emote-card-name">Thank You</span>
      </div>
      <div class="emote-card-btn" onclick="triggerEmote('support')">
        <span class="emote-card-icon">🤲</span>
        <span class="emote-card-name">Ask Support</span>
      </div>
    </div>
  </div>

  <!-- SCREEN 3: IN-GAME SCENARIOS (6 MODES MATCHING REFERENCE IMAGE) -->
  <div class="screen-view" id="screen-scenarios">
    <div style="width: 100%; max-width: 1280px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>🎬 In-Game Scenarios & Political Operations</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>
      <div class="scenario-grid">
        <!-- 1. Door to Door -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #1e3a8a, #3b82f6);">🏡</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 01 • Grassroots</span>
            <h3 class="scenario-title">Door-to-Door Campaigning</h3>
            <p class="scenario-desc">Approach residential apartments, meet working families at doorsteps, listen to civic water grievances, and distribute campaign leaflets with Namaste greetings.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Target: Residential Villas</span>
              <button class="btn-action-trigger" onclick="launchScenario('doortodoor')">🚀 Launch Scenario</button>
            </div>
          </div>
        </div>

        <!-- 2. Public Rally -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #991b1b, #ef4444);">🚩</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 02 • Mass Mobilization</span>
            <h3 class="scenario-title">Public Mega Rally</h3>
            <p class="scenario-desc">Ascend the elevated wooden campaign stage, step before the microphone cluster, deliver a rousing keynote speech, and ignite an ocean of 50+ flag-waving supporters.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Target: Mega Stage (Z = -75)</span>
              <button class="btn-action-trigger" onclick="launchScenario('rally')">🚀 Launch Scenario</button>
            </div>
          </div>
        </div>

        <!-- 3. Driving Mission -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #065f46, #10b981);">🚗</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 03 • Transit & Patrol</span>
            <h3 class="scenario-title">VIP Driving Mission</h3>
            <p class="scenario-desc">Take control of the official White Ambassador VIP Car with flashing red roof beacon. Navigate Dr. Radhakrishnan Avenue, dodge auto-rickshaws and buses, and honk the dual-frequency horn.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Target: Ambassador VIP Car</span>
              <button class="btn-action-trigger" onclick="launchScenario('driving')">🚀 Launch Scenario</button>
            </div>
          </div>
        </div>

        <!-- 4. Water Crisis (Ward 12) -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #0369a1, #0284c7);">🚰</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 04 • Civic Crisis</span>
            <h3 class="scenario-title">Water Crisis (Ward 12)</h3>
            <p class="scenario-desc">Investigate the severe drinking water shortage. Confront the illegal commercial water tanker cartel driver, protect worried residents queuing with plastic pots, and restore equitable tap supply.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Target: Blue Water Tanker</span>
              <button class="btn-action-trigger" onclick="launchScenario('watercrisis')">🚀 Launch Scenario</button>
            </div>
          </div>
        </div>

        <!-- 5. Election Results -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #5b21b6, #8b5cf6);">🗳️</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 05 • Democratic Mandate</span>
            <h3 class="scenario-title">Tamil Nadu Election Results</h3>
            <p class="scenario-desc">Live television counting broadcast. Watch constituency vote returns update in real-time with dynamic bar charts, candidate vote shares, and final victory declarations.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Format: Live TV Broadcast</span>
              <button class="btn-action-trigger" onclick="switchScreen('screen-election')">📊 View Results</button>
            </div>
          </div>
        </div>

        <!-- 6. Career Progression -->
        <div class="scenario-card">
          <div class="scenario-banner" style="background: linear-gradient(135deg, #78350f, #d97706);">👑</div>
          <div class="scenario-content">
            <span class="scenario-tag">Scenario 06 • Political Ascendance</span>
            <h3 class="scenario-title">Leadership & Career Roadmap</h3>
            <p class="scenario-desc">Monitor your 5 core reputation dimensions: Public Trust, Integrity, Leadership, Party Loyalty, and Media Image. Advance from Grassroots Activist to Chief Minister of Tamil Nadu.</p>
            <div class="scenario-footer">
              <span style="font-size: 11px; color: var(--gold-light);">Office: Ward Councilor</span>
              <button class="btn-action-trigger" onclick="switchScreen('screen-profile')">👑 View Progress</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SCREEN 4: CHARACTER ROSTER (13 CHARACTERS MATCHING REFERENCE IMAGE) -->
  <div class="screen-view" id="screen-roster">
    <div style="width: 100%; max-width: 1280px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>👥 Character Roster & In-Game Cast (13)</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
        Every character from the official design reference is physically modeled and populated throughout Chennai Ward 12. Click any character to inspect details.
      </p>
      <div class="roster-grid">
        <!-- 1. Player / Politician -->
        <div class="char-card" onclick="inspectCharacter(0)">
          <div class="char-card-header">
            <div class="char-avatar-circle" style="border-color: var(--gold-primary);">👑</div>
            <div class="char-meta">
              <h3>Arun (Player)</h3>
              <span>Main Politician & Reformer</span>
            </div>
          </div>
          <p class="char-desc">Crisp white khadi shirt, tailored trousers, and a tasteful Indian tricolor scarf. Charismatic grassroots leader fighting for clean water and civic transparency.</p>
          <div class="char-stats-row">
            <span>Trust: 75%</span>
            <span>Integrity: 78%</span>
            <span>Alignment: People's Front</span>
          </div>
        </div>

        <!-- 2. Campaign Worker -->
        <div class="char-card" onclick="inspectCharacter(1)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🧢</div>
            <div class="char-meta">
              <h3>Karthik</h3>
              <span>Campaign Worker (Male)</span>
            </div>
          </div>
          <p class="char-desc">White polo shirt with campaign crest badge, blue jeans, and baseball cap. Field canvasser managing street-level voter lists and banners.</p>
          <div class="char-stats-row">
            <span>Energy: High</span>
            <span>Role: Field Organizer</span>
            <span>Loyalty: 90%</span>
          </div>
        </div>

        <!-- 3. Female Campaign Worker -->
        <div class="char-card" onclick="inspectCharacter(2)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🧣</div>
            <div class="char-meta">
              <h3>Deepa</h3>
              <span>Female Campaign Worker</span>
            </div>
          </div>
          <p class="char-desc">Elegant white salwar suit with vibrant blue dupatta scarf and accreditation badge. Leads women's welfare drives and door-to-door outreach.</p>
          <div class="char-stats-row">
            <span>Trust: 82%</span>
            <span>Role: Women's Wing Lead</span>
            <span>Influence: High</span>
          </div>
        </div>

        <!-- 4. Police Officer -->
        <div class="char-card" onclick="inspectCharacter(3)">
          <div class="char-card-header">
            <div class="char-avatar-circle">👮</div>
            <div class="char-meta">
              <h3>Inspector Pandian</h3>
              <span>Tamil Nadu Police Officer</span>
            </div>
          </div>
          <p class="char-desc">Crisp khaki uniform with shoulder badges, peaked duty cap, brown holster belt, and polished boots. Maintains order at checkpoints and rally barricades.</p>
          <div class="char-stats-row">
            <span>Stance: Strict Law</span>
            <span>Duty: Ward 12 Police</span>
            <span>Morale: Neutral</span>
          </div>
        </div>

        <!-- 5. Journalist -->
        <div class="char-card" onclick="inspectCharacter(4)">
          <div class="char-card-header">
            <div class="char-avatar-circle">📷</div>
            <div class="char-meta">
              <h3>Vikram</h3>
              <span>Press Journalist</span>
            </div>
          </div>
          <p class="char-desc">Slate blue shirt, beige chinos, press media accreditation lanyard, telephoto DSLR camera strapped across chest, and reporting microphone.</p>
          <div class="char-stats-row">
            <span>Media Reach: 50K</span>
            <span>Outlet: News Tamil 24</span>
            <span>Focus: Investigative</span>
          </div>
        </div>

        <!-- 6. Resident (Male) -->
        <div class="char-card" onclick="inspectCharacter(5)">
          <div class="char-card-header">
            <div class="char-avatar-circle">👔</div>
            <div class="char-meta">
              <h3>Murugan</h3>
              <span>Resident (Male)</span>
            </div>
          </div>
          <p class="char-desc">Checkered button-down shirt and brown trousers. Hardworking family man living in Ward 12 apartments frustrated by illegal tanker rates.</p>
          <div class="char-stats-row">
            <span>Issue: Water Rates</span>
            <span>Voter Status: Undecided</span>
            <span>Trust: 55%</span>
          </div>
        </div>

        <!-- 7. Resident (Female) -->
        <div class="char-card" onclick="inspectCharacter(6)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🥻</div>
            <div class="char-meta">
              <h3>Lakshmi</h3>
              <span>Resident (Female)</span>
            </div>
          </div>
          <p class="char-desc">Traditional royal peacock-blue silk saree with shimmering golden zari border and fragrant jasmine flowers in her hair. Vocal advocate for household tap water.</p>
          <div class="char-stats-row">
            <span>Issue: 24/7 Water</span>
            <span>Influence: Community</span>
            <span>Trust: 65%</span>
          </div>
        </div>

        <!-- 8. Elderly Person -->
        <div class="char-card" onclick="inspectCharacter(7)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🦯</div>
            <div class="char-meta">
              <h3>Periyavar Sundaram</h3>
              <span>Elderly Citizen</span>
            </div>
          </div>
          <p class="char-desc">Traditional white cotton shirt, white dhoti with golden kasavu border, silver-white beard, and a polished wooden walking cane. Respected neighborhood elder.</p>
          <div class="char-stats-row">
            <span>Wisdom: 95%</span>
            <span>Reputation: Venerable</span>
            <span>Voter: High Weight</span>
          </div>
        </div>

        <!-- 9. Student -->
        <div class="char-card" onclick="inspectCharacter(8)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🎒</div>
            <div class="char-meta">
              <h3>Anand</h3>
              <span>Student & Youth Activist</span>
            </div>
          </div>
          <p class="char-desc">Neat white collared shirt with navy school trim, shoulder backpack, and university notebooks. Passionate about democratic reforms and youth civic engagement.</p>
          <div class="char-stats-row">
            <span>Drive: Civic Reform</span>
            <span>Age: 20</span>
            <span>Support: Youth Front</span>
          </div>
        </div>

        <!-- 10. Shopkeeper -->
        <div class="char-card" onclick="inspectCharacter(9)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🏪</div>
            <div class="char-meta">
              <h3>Babu</h3>
              <span>Market Shopkeeper</span>
            </div>
          </div>
          <p class="char-desc">Comfortable shirt and printed lungi protected by a heavy blue canvas merchant apron. Operates the fresh vegetable and coconut stall on the avenue.</p>
          <div class="char-stats-row">
            <span>Business: Fresh Market</span>
            <span>Issue: Power & Water</span>
            <span>Commerce: Vital</span>
          </div>
        </div>

        <!-- 11. Political Opponent -->
        <div class="char-card" onclick="inspectCharacter(10)">
          <div class="char-card-header">
            <div class="char-avatar-circle" style="border-color: #ef4444;">⚡</div>
            <div class="char-meta">
              <h3>Karuppasamy</h3>
              <span>Political Opponent</span>
            </div>
          </div>
          <p class="char-desc">Crimson and cream silk shirt with rival political insignia and dark shades. Entrenched incumbent defending existing political patronage and tanker alliances.</p>
          <div class="char-stats-row">
            <span>Faction: Ruling Alliance</span>
            <span>Power: High</span>
            <span>Rivalry: Intense</span>
          </div>
        </div>

        <!-- 12. Rally Supporter -->
        <div class="char-card" onclick="inspectCharacter(11)">
          <div class="char-card-header">
            <div class="char-avatar-circle">🚩</div>
            <div class="char-meta">
              <h3>Shiva</h3>
              <span>Rally Supporter</span>
            </div>
          </div>
          <p class="char-desc">Crisp white shirt with dual-color party scarf draped across chest, waving a large fabric political flag on a tall bamboo pole and leading crowd chants.</p>
          <div class="char-stats-row">
            <span>Enthusiasm: Maximum</span>
            <span>Prop: Party Flag</span>
            <span>Chant: 'Vetri Nichayam!'</span>
          </div>
        </div>

        <!-- 13. Water Crisis Victim -->
        <div class="char-card" onclick="inspectCharacter(12)">
          <div class="char-card-header">
            <div class="char-avatar-circle" style="border-color: var(--blue-bright);">🚰</div>
            <div class="char-meta">
              <h3>Meenakshi</h3>
              <span>Water Crisis Victim</span>
            </div>
          </div>
          <p class="char-desc">Distressed resident in yellow and blue saree holding a traditional plastic water pot (kudam) balanced on her hip, waiting anxiously in the long municipal queue.</p>
          <div class="char-stats-row">
            <span>Wait Time: 4 Hours</span>
            <span>Prop: Plastic Kudam</span>
            <span>Urgency: Critical</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SCREEN 5: ELECTION RESULTS 2027 (MATCHING REFERENCE IMAGE) -->
  <div class="screen-view" id="screen-election">
    <div style="width: 100%; max-width: 900px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>🗳️ Tamil Nadu State Election 2027</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>

      <div class="election-broadcast-screen">
        <div class="broadcast-header">
          <div>
            <h2 style="font-size: 20px; font-weight: 900; color: #fff;">TAMIL NADU ELECTION RESULTS</h2>
            <div style="font-size: 12px; color: var(--gold-light);">CONSTITUENCY: CHENNAI WARD 12 (BYE-ELECTION)</div>
          </div>
          <div class="live-badge">🔴 OFFICIAL RESULTS</div>
        </div>

        <div class="election-bars-container">
          <!-- Your Party -->
          <div class="election-bar-row">
            <div class="election-bar-header">
              <span style="color: #38bdf8;">★ Your Party (People's Front - Arun)</span>
              <span style="color: #38bdf8;">45.2% (68,450 Votes)</span>
            </div>
            <div class="election-bar-track">
              <div class="election-bar-fill" style="width: 45.2%; background: linear-gradient(90deg, #0284c7, #38bdf8);">
                45.2% WINNER
              </div>
            </div>
          </div>

          <!-- Rival Party -->
          <div class="election-bar-row">
            <div class="election-bar-header">
              <span style="color: #ef4444;">Rival Party (Ruling Alliance - Karuppasamy)</span>
              <span style="color: #ef4444;">38.6% (58,420 Votes)</span>
            </div>
            <div class="election-bar-track">
              <div class="election-bar-fill" style="width: 38.6%; background: linear-gradient(90deg, #b91c1c, #ef4444);">
                38.6%
              </div>
            </div>
          </div>

          <!-- Others -->
          <div class="election-bar-row">
            <div class="election-bar-header">
              <span style="color: #fbbf24;">Others & Independent Candidates</span>
              <span style="color: #fbbf24;">16.2% (24,510 Votes)</span>
            </div>
            <div class="election-bar-track">
              <div class="election-bar-fill" style="width: 16.2%; background: linear-gradient(90deg, #d97706, #fbbf24);">
                16.2%
              </div>
            </div>
          </div>
        </div>

        <div class="election-winner-spotlight">
          <div style="font-size: 42px;">🏆</div>
          <div>
            <h3 style="color: var(--green-accent); font-size: 18px; font-weight: 900;">MANDATE CONFIRMED: ARUN ELECTED WARD COUNCILOR</h3>
            <p style="font-size: 13px; color: #cbd5e1; line-height: 1.45; margin-top: 4px;">
              By exposing the water tanker mafia and standing with working residents, Arun secured a decisive 6.6% margin of victory over the incumbent alliance!
            </p>
          </div>
        </div>

        <div style="display: flex; gap: 12px; justify-content: flex-end;">
          <button class="btn-action-trigger" style="background: var(--gold-primary); color: #000;" onclick="switchScreen('screen-profile')">Inspect Career Progression ▶</button>
          <button class="btn-action-trigger" onclick="start3DWorld()">Return to 3D Chennai</button>
        </div>
      </div>
    </div>
  </div>

  <!-- SCREEN 6: CAREER PROGRESSION (MATCHING REFERENCE IMAGE) -->
  <div class="screen-view" id="screen-profile">
    <div style="width: 100%; max-width: 1000px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>📊 Political Career Progression & Leadership</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>

      <div class="career-hero-card">
        <div class="career-hero-top">
          <div class="career-avatar-box">👑</div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h2 style="font-size: 24px; font-weight: 900; color: #fff;">Leadership Level 5</h2>
              <span style="font-size: 13px; font-weight: 800; color: var(--gold-light);">320 / 500 XP</span>
            </div>
            <div class="career-xp-track" style="margin: 8px 0;">
              <div class="career-xp-fill"></div>
            </div>
            <div style="font-size: 13px; color: var(--text-muted);">
              Current Office: <strong style="color: var(--blue-bright);">Ward Councilor (Ward 12, Chennai)</strong> • Next: <strong>Member of Legislative Assembly (MLA)</strong>
            </div>
          </div>
        </div>

        <div class="grid-dashboard" style="margin-top: 8px;">
          <!-- 5 Independent Dimensions -->
          <div class="dash-card">
            <div class="card-top-title"><span>Core Reputation Attributes</span><span>Status</span></div>
            <div class="rep-bar-row">
              <div class="rep-bar-label-line"><span style="color: #38bdf8;">Public Trust</span><span id="rep-val-trust">72%</span></div>
              <div class="rep-track"><div class="rep-fill" id="rep-bar-trust" style="width: 72%; background: #38bdf8;"></div></div>
            </div>
            <div class="rep-bar-row">
              <div class="rep-bar-label-line"><span style="color: #10b981;">Integrity</span><span>68%</span></div>
              <div class="rep-track"><div class="rep-fill" style="width: 68%; background: #10b981;"></div></div>
            </div>
            <div class="rep-bar-row">
              <div class="rep-bar-label-line"><span style="color: #f59e0b;">Reputation</span><span>71%</span></div>
              <div class="rep-track"><div class="rep-fill" style="width: 71%; background: #f59e0b;"></div></div>
            </div>
            <div class="rep-bar-row">
              <div class="rep-bar-label-line"><span style="color: #8b5cf6;">Leadership Authority</span><span>74%</span></div>
              <div class="rep-track"><div class="rep-fill" style="width: 74%; background: #8b5cf6;"></div></div>
            </div>
            <div class="rep-bar-row">
              <div class="rep-bar-label-line"><span style="color: #ef4444;">Media Visibility</span><span>65%</span></div>
              <div class="rep-track"><div class="rep-fill" style="width: 65%; background: #ef4444;"></div></div>
            </div>
          </div>

          <!-- Career Ladder -->
          <div class="dash-card">
            <div class="card-top-title"><span>Career Office Milestones</span></div>
            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
              <div style="color: var(--green-accent); font-weight: 700;">✓ Level 1: Grassroots Activist (Completed)</div>
              <div style="color: var(--green-accent); font-weight: 700;">✓ Level 2: Ward 12 Campaign Lead (Completed)</div>
              <div style="color: var(--gold-light); font-weight: 800; background: rgba(245, 158, 11, 0.1); padding: 6px 10px; border-radius: 6px;">
                ★ Level 3-5: Elected Ward Councilor (CURRENT)
              </div>
              <div style="color: var(--text-muted);">🔒 Level 6: Corporation Standing Committee Chairman</div>
              <div style="color: var(--text-muted);">🔒 Level 7: Member of Legislative Assembly (MLA)</div>
              <div style="color: var(--text-muted);">🔒 Level 8: Cabinet Minister (Municipal Administration & Water)</div>
              <div style="color: var(--text-muted);">🔒 Level 9: Chief Minister of Tamil Nadu</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SCREEN 7: CAMPAIGN STRATEGY -->
  <div class="screen-view" id="screen-campaign">
    <div style="width: 100%; max-width: 1280px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>📢 Campaign Strategy & Voter Mobilization</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>
      <div class="grid-dashboard">
        <div class="dash-card">
          <div class="card-top-title"><span>Campaign Actions</span><span>Budget Cost</span></div>
          <div class="action-row-item">
            <div class="action-left">
              <div class="action-icon-circle" style="color: #ef4444;">🚩</div>
              <div class="action-info"><h4>Political Mega Rally</h4><p>Keynote address on campaign stage with flags and public sound</p></div>
            </div>
            <span style="color: var(--gold-light); font-size: 12px; font-weight: 700;">₹ 50,000</span>
            <button class="btn-action-trigger" onclick="runCampaignAction('Mega Rally', 50000, 8)">Launch</button>
          </div>
          <div class="action-row-item">
            <div class="action-left">
              <div class="action-icon-circle" style="color: #38bdf8;">🤝</div>
              <div class="action-info"><h4>Door-to-Door Canvassing</h4><p>Direct meetings with resident families, listening to local issues</p></div>
            </div>
            <span style="color: var(--gold-light); font-size: 12px; font-weight: 700;">₹ 20,000</span>
            <button class="btn-action-trigger" onclick="runCampaignAction('Door-to-Door Canvassing', 20000, 5)">Launch</button>
          </div>
          <div class="action-row-item">
            <div class="action-left">
              <div class="action-icon-circle" style="color: #10b981;">🚰</div>
              <div class="action-info"><h4>Emergency Water Tanker Supply</h4><p>Deploy free clean drinking water relief to low-income streets</p></div>
            </div>
            <span style="color: var(--gold-light); font-size: 12px; font-weight: 700;">₹ 35,000</span>
            <button class="btn-action-trigger" onclick="runCampaignAction('Emergency Water Tanker Supply', 35000, 7)">Deploy</button>
          </div>
        </div>
        <div class="dash-card">
          <div class="card-top-title"><span>Campaign Momentum</span><span>Voter Confidence</span></div>
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 18px 0;">
            <div style="font-size: 44px; font-weight: 900; color: var(--blue-bright);" id="camp-support-val">72%</div>
            <div style="font-size: 12px; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Projected Vote Share</div>
          </div>
          <p style="font-size: 12px; color: var(--text-muted); text-align: center; line-height: 1.45;">
            Public rallies galvanize youth voter turnout. Direct door-to-door listening builds lasting trust among women voters and senior residents.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- SCREEN 8: SETTINGS & PERFORMANCE -->
  <div class="screen-view" id="screen-settings">
    <div style="width: 100%; max-width: 720px; margin: 0 auto;">
      <div class="screen-header-title">
        <span>⚙️ Visuals & Hardware Performance</span>
        <button class="btn-action-trigger" onclick="switchScreen('screen-main-menu')">Back to Menu</button>
      </div>
      <div class="dash-card">
        <div class="card-top-title"><span>Graphics Quality Preset</span></div>
        <p style="font-size: 13px; color: var(--text-muted); line-height: 1.45;">
          Optimized specifically for laptops with Intel Core 5 processor, integrated Intel graphics, and 16 GB RAM.
        </p>
        <div class="perf-options-grid">
          <div class="perf-chip-btn" id="preset-low" onclick="applyGraphicsPreset('low')">
            <div style="font-size: 14px; font-weight: 800;">LOW</div>
            <div style="font-size: 11px; opacity: 0.8;">No Shadows • 20 Crowd • 60+ FPS</div>
          </div>
          <div class="perf-chip-btn active" id="preset-med" onclick="applyGraphicsPreset('medium')">
            <div style="font-size: 14px; font-weight: 800;">MEDIUM</div>
            <div style="font-size: 11px; opacity: 0.8;">1024 Shadows • 45 Crowd • Balanced</div>
          </div>
          <div class="perf-chip-btn" id="preset-high" onclick="applyGraphicsPreset('high')">
            <div style="font-size: 14px; font-weight: 800;">HIGH</div>
            <div style="font-size: 11px; opacity: 0.8;">Soft Shadows • 70+ Crowd • Realistic</div>
          </div>
        </div>

        <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 13px;">
            <span>Real-Time Telemetry:</span>
            <span id="telemetry-info" style="color: var(--blue-bright); font-family: monospace;">60 FPS | 16.6 ms</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 13px;">
            <span>Hardware Target:</span>
            <span style="color: var(--gold-light);">Intel Core 5 / Intel Graphics / 16 GB RAM</span>
          </div>
        </div>

        <button class="btn-action-trigger" style="margin-top: 10px; width: 100%;" onclick="switchScreen('screen-main-menu')">Return to Menu</button>
      </div>
    </div>
  </div>

  <!-- MASTER NAVIGATION DOCK -->
  <div id="global-dock">
    <button class="dock-btn active" id="dock-btn-main" onclick="switchScreen('screen-main-menu')">🏠 Main Menu</button>
    <button class="dock-btn" id="dock-btn-game" onclick="start3DWorld()">🎮 3D Chennai</button>
    <button class="dock-btn" onclick="switchScreen('screen-scenarios')">🎬 Scenarios</button>
    <button class="dock-btn" onclick="switchScreen('screen-roster')">👥 Cast (13)</button>
    <button class="dock-btn" onclick="openEmoteMenu()">🎭 Emotes (18)</button>
    <button class="dock-btn" onclick="switchScreen('screen-campaign')">📢 Campaign</button>
    <button class="dock-btn" onclick="switchScreen('screen-election')">🗳️ Election</button>
    <button class="dock-btn" onclick="switchScreen('screen-profile')">👑 Career</button>
    <button class="dock-btn" onclick="switchScreen('screen-settings')">⚙️ Settings</button>
  </div>

  <!-- PAUSE MENU MODAL -->
  <div id="pause-modal">
    <div class="pause-title">GAME PAUSED</div>
    <div style="font-size: 13px; color: var(--text-muted);">Kingmakers of Indian Politics - Chennai Ward 12</div>
    <div class="pause-button-list">
      <button class="btn-menu primary" onclick="closePauseMenu()">▶ Resume Gameplay</button>
      <button class="btn-menu" onclick="closePauseMenu(); openEmoteMenu();">🎭 Open Emotes Menu (18)</button>
      <button class="btn-menu" onclick="closePauseMenu(); switchScreen('screen-scenarios');">🎬 In-Game Scenarios</button>
      <button class="btn-menu" onclick="closePauseMenu(); switchScreen('screen-roster');">👥 Character Cast Roster</button>
      <button class="btn-menu" onclick="closePauseMenu(); switchScreen('screen-settings');">⚙️ Graphics & Settings</button>
      <button class="btn-menu" onclick="closePauseMenu(); resetLevel1();">🔄 Restart Level 1</button>
      <button class="btn-menu" onclick="closePauseMenu(); switchScreen('screen-main-menu');">🏠 Exit to Main Menu</button>
    </div>
  </div>

  <!-- Dialogue Box Modal -->
  <div id="dialogue-modal">
    <div class="dialogue-speaker" id="dialogue-speaker"><span>👤</span><span>Ward Member Karuppasamy</span></div>
    <div class="dialogue-text" id="dialogue-text">...</div>
    <div class="dialogue-options" id="dialogue-options"></div>
  </div>

  <!-- Level Complete Victory Modal -->
  <div id="level-complete-modal">
    <div style="font-size: 36px; color: var(--gold-light);">★★★</div>
    <h2 style="color: var(--green-accent); font-size: 24px; font-weight: 900;">WARD 12 BYE-ELECTION VICTORY!</h2>
    <p style="color: #cbd5e1; font-size: 14px; line-height: 1.5;">
      You stood resolutely with the working families of Chennai Ward 12, exposed the illegal water tanker cartel, energized thousands at the campaign rally, and secured an overwhelming election victory!
    </p>
    <div style="background: rgba(18, 30, 54, 0.85); border-radius: 12px; padding: 14px 20px; width: 100%; display: flex; justify-content: space-around;">
      <div><span style="color: var(--text-muted); font-size: 11px;">PUBLIC TRUST</span><strong style="color: var(--blue-bright); font-size: 17px; display:block;">88%</strong></div>
      <div><span style="color: var(--text-muted); font-size: 11px;">VOTES SECURED</span><strong style="color: var(--green-accent); font-size: 17px; display:block;">68,450</strong></div>
      <div><span style="color: var(--text-muted); font-size: 11px;">NEXT OFFICE</span><strong style="color: var(--gold-light); font-size: 17px; display:block;">Ward Councilor</strong></div>
    </div>
    <button class="btn-menu primary" style="width: 100%; justify-content: center;" onclick="switchScreen('screen-election')">View Election Broadcast ▶</button>
  </div>
'''

print("Part 1 defined.")
