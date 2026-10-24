# -*- coding: utf-8 -*-
"""
Helper module that provides the complete JavaScript section for Kingmakers of Indian Politics.
"""

def get_js_code():
    return r'''  <script>
    /* ==========================================================================
       1. SYNTHESIZED SOUND SYSTEM (Web Audio API)
       ========================================================================== */
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playBeep(freq = 440, type = 'sine', duration = 0.1, gainVal = 0.12) {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    // Realistic Indian Ambassador car horn (dual-frequency harmonic honk: 370Hz + 440Hz)
    function playCarHorn() {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const t = audioCtx.currentTime;
      [370, 440].forEach(f => {
        try {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(f, t);
          gain.gain.setValueAtTime(0.18, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(t + 0.35);
        } catch (e) {}
      });
      document.getElementById('sys-event-msg').innerText = "Ambassador horn sounded! Clearing avenue traffic.";
    }

    // Procedural Ambient Engine Rumble
    let engineOsc = null;
    let engineGain = null;

    function startEngineSound() {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      if (!engineOsc) {
        try {
          engineOsc = audioCtx.createOscillator();
          engineGain = audioCtx.createGain();
          engineOsc.type = 'sawtooth';
          engineOsc.frequency.setValueAtTime(55, audioCtx.currentTime);
          engineGain.gain.setValueAtTime(0.06, audioCtx.currentTime);
          engineOsc.connect(engineGain);
          engineGain.connect(audioCtx.destination);
          engineOsc.start();
        } catch (e) {}
      }
    }

    function updateEngineSound(speedRatio) {
      if (engineOsc && audioCtx.state !== 'suspended') {
        const targetFreq = 50 + speedRatio * 130;
        engineOsc.frequency.setTargetAtTime(targetFreq, audioCtx.currentTime, 0.08);
      }
    }

    function stopEngineSound() {
      if (engineGain) {
        try {
          engineGain.gain.setTargetAtTime(0, audioCtx.currentTime, 0.1);
          setTimeout(() => {
            if (engineOsc) {
              engineOsc.stop();
              engineOsc.disconnect();
              engineOsc = null;
              engineGain = null;
            }
          }, 150);
        } catch (e) {}
      }
    }

    /* ==========================================================================
       2. PROCEDURAL HIGH-RESOLUTION TEXTURE GENERATORS
       ========================================================================== */
    function createRoadTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 512; cvs.height = 512;
      const ctx = cvs.getContext('2d');

      // Asphalt base with grit
      ctx.fillStyle = '#1e242d';
      ctx.fillRect(0, 0, 512, 512);

      // Fine asphalt grit noise
      for (let i = 0; i < 18000; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        const c = 20 + Math.random() * 25;
        ctx.fillStyle = `rgb(${c},${c+2},${c+5})`;
        ctx.fillRect(x, y, 1.5, 1.5);
      }

      // Yellow double center divider line
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(250, 0); ctx.lineTo(250, 512);
      ctx.moveTo(262, 0); ctx.lineTo(262, 512);
      ctx.stroke();

      // White dashed lane markers
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 5;
      ctx.setLineDash([28, 28]);
      ctx.beginPath();
      ctx.moveTo(130, 0); ctx.lineTo(130, 512);
      ctx.moveTo(382, 0); ctx.lineTo(382, 512);
      ctx.stroke();

      // White solid boundary lines
      ctx.setLineDash([]);
      ctx.lineWidth = 4;
      ctx.strokeStyle = '#cbd5e1';
      ctx.beginPath();
      ctx.moveTo(18, 0); ctx.lineTo(18, 512);
      ctx.moveTo(494, 0); ctx.lineTo(494, 512);
      ctx.stroke();

      const tex = new THREE.CanvasTexture(cvs);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(1, 14);
      return tex;
    }

    function createSidewalkTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 256; cvs.height = 256;
      const ctx = cvs.getContext('2d');

      ctx.fillStyle = '#64748b';
      ctx.fillRect(0, 0, 256, 256);

      // Interlocking paver blocks pattern
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 32) {
        for (let x = 0; x < 256; x += 32) {
          ctx.strokeRect(x, y, 32, 32);
          ctx.fillStyle = ((x + y) % 64 === 0) ? '#94a3b8' : '#78889b';
          ctx.fillRect(x + 2, y + 2, 28, 28);
        }
      }

      const tex = new THREE.CanvasTexture(cvs);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(2, 24);
      return tex;
    }

    // 100% English Commercial Shop Signboard
    function createShopSignTexture(mainTitle, subTitle, bgColor, textColor = '#ffffff', subIcon = '★') {
      const cvs = document.createElement('canvas');
      cvs.width = 512; cvs.height = 128;
      const ctx = cvs.getContext('2d');

      ctx.fillStyle = bgColor;
      ctx.fillRect(0, 0, 512, 128);

      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 6;
      ctx.strokeRect(4, 4, 504, 120);

      ctx.fillStyle = textColor;
      ctx.font = '900 32px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${subIcon} ${mainTitle.toUpperCase()} ${subIcon}`, 256, 54);

      ctx.fillStyle = '#fde047';
      ctx.font = 'bold 18px sans-serif';
      ctx.fillText(subTitle, 256, 94);

      return new THREE.CanvasTexture(cvs);
    }

    // 100% English Political Election Flex Banner
    function createElectionBannerTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 512; cvs.height = 256;
      const ctx = cvs.getContext('2d');

      // Vibrant tricolor & royal gradient background
      const grad = ctx.createLinearGradient(0, 0, 512, 256);
      grad.addColorStop(0, '#0f172a');
      grad.addColorStop(0.5, '#1e3a8a');
      grad.addColorStop(1, '#0284c7');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 512, 256);

      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 10;
      ctx.strokeRect(6, 6, 500, 244);

      ctx.fillStyle = '#fbbf24';
      ctx.font = '900 22px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('👑 PUBLIC SERVICE • PEOPLE\'S DEMOCRACY 👑', 256, 42);

      ctx.fillStyle = '#ffffff';
      ctx.font = '900 32px sans-serif';
      ctx.fillText('WARD 12 BYE-ELECTION 2027', 256, 92);

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 26px sans-serif';
      ctx.fillText('CANDIDATE: ARUN (PEOPLE\'S FRONT)', 256, 140);

      ctx.fillStyle = '#fde047';
      ctx.font = 'bold 19px sans-serif';
      ctx.fillText('CLEAN WATER IS OUR FUNDAMENTAL RIGHT!', 256, 188);

      ctx.fillStyle = '#10b981';
      ctx.font = 'bold 15px sans-serif';
      ctx.fillText('★ VOTE FOR HONESTY & PROGRESS ★', 256, 226);

      return new THREE.CanvasTexture(cvs);
    }

    // 100% English Mega Rally Stage Backdrop
    function createRallyBackdropTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 1024; cvs.height = 384;
      const ctx = cvs.getContext('2d');

      ctx.fillStyle = '#7f1d1d';
      ctx.fillRect(0, 0, 1024, 384);

      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 14;
      ctx.strokeRect(10, 10, 1004, 364);

      ctx.fillStyle = '#fef08a';
      ctx.font = '900 44px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('WARD 12 SPECIAL BYE-ELECTION CONVENTION', 512, 90);

      ctx.fillStyle = '#ffffff';
      ctx.font = '900 60px sans-serif';
      ctx.fillText('MEGA CAMPAIGN RALLY 2027', 512, 175);

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 36px sans-serif';
      ctx.fillText('KEYNOTE ADDRESS BY CANDIDATE ARUN', 512, 245);

      ctx.fillStyle = '#4ade80';
      ctx.font = 'bold 28px sans-serif';
      ctx.fillText('RESTORING 24/7 WATER SUPPLY • END TANKER CORRUPTION!', 512, 315);

      return new THREE.CanvasTexture(cvs);
    }

    // Indian National Tricolor Flag Texture with Ashoka Chakra
    function createIndianFlagTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 300; cvs.height = 200;
      const ctx = cvs.getContext('2d');

      // Saffron (Top)
      ctx.fillStyle = '#ff9933';
      ctx.fillRect(0, 0, 300, 66.6);

      // White (Middle)
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 66.6, 300, 66.6);

      // India Green (Bottom)
      ctx.fillStyle = '#138808';
      ctx.fillRect(0, 133.2, 300, 66.8);

      // Navy Blue Ashoka Chakra (24 spokes)
      ctx.strokeStyle = '#000080';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(150, 100, 22, 0, Math.PI * 2);
      ctx.stroke();

      for (let i = 0; i < 24; i++) {
        const angle = (i * Math.PI) / 12;
        ctx.beginPath();
        ctx.moveTo(150, 100);
        ctx.lineTo(150 + Math.cos(angle) * 22, 100 + Math.sin(angle) * 22);
        ctx.stroke();
      }

      return new THREE.CanvasTexture(cvs);
    }

    // Temple Gopuram Sandstone Relief Texture
    function createTempleReliefTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 256; cvs.height = 256;
      const ctx = cvs.getContext('2d');

      ctx.fillStyle = '#d97706';
      ctx.fillRect(0, 0, 256, 256);

      // Carved stone horizontal pilasters and niche reliefs
      ctx.strokeStyle = '#92400e';
      ctx.lineWidth = 3;
      for (let y = 0; y < 256; y += 32) {
        ctx.beginPath();
        ctx.moveTo(0, y); ctx.lineTo(256, y);
        ctx.stroke();

        for (let x = 16; x < 256; x += 32) {
          ctx.strokeRect(x, y + 4, 16, 24);
          ctx.fillStyle = '#b45309';
          ctx.fillRect(x + 2, y + 6, 12, 20);
        }
      }

      const tex = new THREE.CanvasTexture(cvs);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(4, 6);
      return tex;
    }

    // Working Ripon Building Clock Face
    function createClockFaceTexture() {
      const cvs = document.createElement('canvas');
      cvs.width = 256; cvs.height = 256;
      const ctx = cvs.getContext('2d');

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(128, 128, 120, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 8;
      ctx.stroke();

      // Roman Numerals
      ctx.fillStyle = '#0f172a';
      ctx.font = '900 24px serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('XII', 128, 30);
      ctx.fillText('III', 226, 128);
      ctx.fillText('VI', 128, 226);
      ctx.fillText('IX', 30, 128);

      // Hands (set to 4:30 PM Chennai Golden Afternoon)
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(128, 128); ctx.lineTo(180, 175); // Hour
      ctx.stroke();

      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(128, 128); ctx.lineTo(128, 210); // Minute
      ctx.stroke();

      return new THREE.CanvasTexture(cvs);
    }

    /* ==========================================================================
       3. GAME STATE, CHARACTERS DATA & SCREEN NAVIGATION
       ========================================================================== */
    let currentTask = 1; // 1: Karuppasamy, 2: Water Tanker, 3: Ambassador Car, 4: Rally Stage
    let isDriving = false;
    let carSpeed = 0;
    let cash = 245000;
    let trust = 75;
    let graphicsPreset = 'medium'; // 'low', 'medium', 'high'

    // Active Emote state
    let activeEmote = null;
    let emoteTimer = 0;

    const taskTitles = [
      "",
      "Task 1: Meet Ward Member Karuppasamy at the local office",
      "Task 2: Intercept the illegal Water Tanker truck",
      "Task 3: Enter the White Ambassador VIP Car and mobilize voters",
      "Task 4: Address the Mega Rally and win the Ward 12 Election!"
    ];

    function updateTaskHUD() {
      document.getElementById('mission-goal-text').innerText = taskTitles[currentTask];
      document.getElementById('hud-cash-val').innerText = `₹ ${cash.toLocaleString('en-IN')}`;
      document.getElementById('rep-val-trust').innerText = `${trust}%`;
      document.getElementById('rep-bar-trust').style.width = `${trust}%`;
    }

    function switchScreen(screenId) {
      document.querySelectorAll('.screen-view').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(screenId);
      if (target) target.classList.add('active');
      document.getElementById('hud-overlay').style.display = 'none';

      document.querySelectorAll('.dock-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(screenId));
      });
      playBeep(480, 'sine', 0.08);
    }

    function start3DWorld() {
      document.querySelectorAll('.screen-view').forEach(s => s.classList.remove('active'));
      document.getElementById('hud-overlay').style.display = 'flex';
      document.querySelectorAll('.dock-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('dock-btn-game').classList.add('active');
      playBeep(520, 'sine', 0.15);
    }

    function openPauseMenu() {
      document.getElementById('pause-modal').style.display = 'flex';
      playBeep(400, 'sine', 0.12);
    }

    function closePauseMenu() {
      document.getElementById('pause-modal').style.display = 'none';
      playBeep(520, 'sine', 0.1);
    }

    function openEmoteMenu() {
      document.getElementById('emote-modal').style.display = 'flex';
      playBeep(540, 'triangle', 0.1);
    }

    function closeEmoteMenu() {
      document.getElementById('emote-modal').style.display = 'none';
      playBeep(420, 'sine', 0.08);
    }

    // Trigger an Emote from the 18-Emote Grid
    const emoteNames = {
      smile: 'Smile / Happy',
      confident: 'Confident Pose',
      wave: 'Wave Hello',
      namaste: 'Namaste Greeting',
      thumbsup: 'Thumbs Up',
      point: 'Pointing Direction',
      speech: 'Public Speech',
      listen: 'Listening Attentively',
      angry: 'Angry / Indignant',
      sad: 'Disappointed / Sad',
      worried: 'Water Crisis Worry',
      thinking: 'Thinking Pose',
      handshake: 'Handshake Gesture',
      celebrate: 'Election Victory',
      defeat: 'Defeat Reaction',
      apologize: 'Deep Apology',
      thank: 'Thank You Grateful',
      support: 'Ask for Public Support'
    };

    const emoteIcons = {
      smile: '😊', confident: '🦸', wave: '👋', namaste: '🙏',
      thumbsup: '👍', point: '👉', speech: '🎙️', listen: '✋',
      angry: '😠', sad: '😔', worried: '😟', thinking: '🤔',
      handshake: '🤝', celebrate: '🎉', defeat: '🤦', apologize: '🙇',
      thank: '💖', support: '🤲'
    };

    function triggerEmote(emoteId) {
      activeEmote = emoteId;
      emoteTimer = 3.5;
      closeEmoteMenu();

      const banner = document.getElementById('emote-banner');
      document.getElementById('emote-banner-icon').innerText = emoteIcons[emoteId] || '🎭';
      document.getElementById('emote-banner-text').innerText = `Emote Active: ${emoteNames[emoteId] || emoteId}`;
      banner.style.display = 'flex';

      playBeep(640, 'sine', 0.18);
      document.getElementById('sys-event-msg').innerText = `Arun performs: ${emoteNames[emoteId]}. Nearby citizens react!`;

      // Trigger dynamic NPC reactions in vicinity
      crowdList.forEach(c => {
        const dist = c.basePos.distanceTo(playerGroup.position);
        if (dist < 14.0) {
          c.reactingEmote = emoteId;
          c.reactionTimer = 4.0;
        }
      });
    }

    // Scenario Launchers (Direct In-Game Teleport & Scenario Configuration)
    function launchScenario(key) {
      start3DWorld();
      if (key === 'doortodoor') {
        playerGroup.position.set(-14.0, 0, 5.0);
        playerGroup.rotation.y = -Math.PI / 2;
        camYaw = Math.PI / 2;
        triggerEmote('namaste');
        openDialogue(
          "Door-to-Door Campaigning (Ward 12)",
          "Vanakkam Arun! We are deeply appreciative of your door-to-door visit. The illegal water tankers are demanding ₹2000 per load, and municipal taps have been dry for 5 days. What will your front do?",
          [
            { text: "Assure 24/7 piped municipal water and end the private tanker cartel! (+10% Public Trust)", act: () => { trust += 10; updateTaskHUD(); } },
            { text: "Hand out emergency campaign water coupons for free tanker relief. (+5% Trust, -₹5,000)", act: () => { trust += 5; cash -= 5000; updateTaskHUD(); } }
          ]
        );
      } else if (key === 'rally') {
        playerGroup.position.set(0, 1.8, -73.5);
        playerGroup.rotation.y = 0;
        camYaw = Math.PI;
        triggerEmote('speech');
        currentTask = 4;
        updateTaskHUD();
      } else if (key === 'driving') {
        playerGroup.position.set(carGroup.position.x + 2, 0, carGroup.position.z);
        enterCar();
      } else if (key === 'watercrisis') {
        playerGroup.position.set(-6, 0, -26);
        currentTask = 2;
        updateTaskHUD();
        handleInteraction();
      }
    }

    function inspectCharacter(idx) {
      const charCards = document.querySelectorAll('.char-card');
      if (charCards[idx]) {
        charCards[idx].scrollIntoView({ behavior: 'smooth', block: 'center' });
        playBeep(580, 'sine', 0.12);
      }
    }

    function runCampaignAction(actionName, cost, trustGain) {
      if (cash < cost) {
        alert("Insufficient campaign funds! Win elections or collect donations.");
        return;
      }
      cash -= cost;
      trust = Math.min(100, trust + trustGain);
      updateTaskHUD();
      document.getElementById('camp-support-val').innerText = `${trust}%`;
      playBeep(700, 'triangle', 0.2);
      alert(`Success: "${actionName}" executed!\nInvested: ₹${cost.toLocaleString('en-IN')}\nPublic Trust gained: +${trustGain}%`);
    }

    document.getElementById('btn-continue-game').addEventListener('click', start3DWorld);
    document.getElementById('btn-menu-scenarios').addEventListener('click', () => switchScreen('screen-scenarios'));
    document.getElementById('btn-menu-roster').addEventListener('click', () => switchScreen('screen-roster'));
    document.getElementById('btn-open-campaign').addEventListener('click', () => switchScreen('screen-campaign'));
    document.getElementById('btn-open-election').addEventListener('click', () => switchScreen('screen-election'));
    document.getElementById('btn-open-char').addEventListener('click', () => switchScreen('screen-profile'));
    document.getElementById('btn-open-settings').addEventListener('click', () => switchScreen('screen-settings'));
'''

print("Part 2 (JS Code Provider) defined.")
