# -*- coding: utf-8 -*-
"""
Helper module that provides the 3D Engine, Landmarks, Vehicles, Characters,
and Kinematics for Kingmakers of Indian Politics.
"""

def get_engine_code():
    return r'''
    /* ==========================================================================
       4. THREE.JS 3D ENGINE & SCENE SETUP
       ========================================================================== */
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();

    // Atmosphere: Chennai Warm Golden Afternoon
    scene.background = new THREE.Color(0xbfe0f7);
    scene.fog = new THREE.FogExp2(0xbfe0f7, 0.0075);

    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.2, 500);
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    container.appendChild(renderer.domElement);

    // Warm Chennai sunlight + soft skylight
    const hemiLight = new THREE.HemisphereLight(0xfff7ed, 0x334155, 0.95);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffbeb, 1.4);
    dirLight.position.set(45, 65, 30);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 200;
    const shadowD = 75;
    dirLight.shadow.camera.left = -shadowD;
    dirLight.shadow.camera.right = shadowD;
    dirLight.shadow.camera.top = shadowD;
    dirLight.shadow.camera.bottom = -shadowD;
    dirLight.shadow.bias = -0.0006;
    scene.add(dirLight);

    // Camera Orbit State
    let camYaw = 0;
    let camPitch = 0.25;
    let isMouseDown = false;
    let prevMousePos = { x: 0, y: 0 };

    window.addEventListener('pointerdown', (e) => {
      if (e.target.closest('#hud-overlay') || e.target.closest('.screen-view') || e.target.closest('#global-dock') || e.target.closest('#dialogue-modal') || e.target.closest('#emote-modal') || e.target.closest('#pause-modal')) return;
      isMouseDown = true;
      prevMousePos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('pointermove', (e) => {
      if (!isMouseDown) return;
      const dx = e.clientX - prevMousePos.x;
      const dy = e.clientY - prevMousePos.y;
      camYaw -= dx * 0.005;
      camPitch = Math.max(0.08, Math.min(0.85, camPitch + dy * 0.004));
      prevMousePos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('pointerup', () => isMouseDown = false);

    /* ==========================================================================
       5. CHENNAI ENVIRONMENT & ROAD INFRASTRUCTURE
       ========================================================================== */
    const roadTexture = createRoadTexture();
    const sidewalkTexture = createSidewalkTexture();

    // Road Mesh (Z from +40 to -125)
    const roadGeo = new THREE.PlaneGeometry(24, 195);
    const roadMat = new THREE.MeshStandardMaterial({
      map: roadTexture,
      roughness: 0.88,
      metalness: 0.05
    });
    const mainRoad = new THREE.Mesh(roadGeo, roadMat);
    mainRoad.rotation.x = -Math.PI / 2;
    mainRoad.position.set(0, 0.01, -42.5);
    mainRoad.receiveShadow = true;
    scene.add(mainRoad);

    // Sidewalks (West and East)
    const sidewalkGeo = new THREE.BoxGeometry(6, 0.35, 195);
    const sidewalkMat = new THREE.MeshStandardMaterial({
      map: sidewalkTexture,
      roughness: 0.8
    });

    const westWalk = new THREE.Mesh(sidewalkGeo, sidewalkMat);
    westWalk.position.set(-15, 0.175, -42.5);
    westWalk.receiveShadow = true;
    scene.add(westWalk);

    const eastWalk = new THREE.Mesh(sidewalkGeo, sidewalkMat);
    eastWalk.position.set(15, 0.175, -42.5);
    eastWalk.receiveShadow = true;
    scene.add(eastWalk);

    // Raised Curbs with safety yellow/black hazard stripes
    function createCurbTrim(xPos) {
      const cvs = document.createElement('canvas');
      cvs.width = 128; cvs.height = 32;
      const ctx = cvs.getContext('2d');
      for (let i = 0; i < 128; i += 32) {
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(i, 0, 16, 32);
        ctx.fillStyle = '#1e242d';
        ctx.fillRect(i + 16, 0, 16, 32);
      }
      const t = new THREE.CanvasTexture(cvs);
      t.wrapS = THREE.RepeatWrapping;
      t.repeat.set(26, 1);
      const curb = new THREE.Mesh(
        new THREE.BoxGeometry(0.3, 0.38, 195),
        new THREE.MeshStandardMaterial({ map: t, roughness: 0.7 })
      );
      curb.position.set(xPos, 0.19, -42.5);
      scene.add(curb);
    }
    createCurbTrim(-12.05);
    createCurbTrim(12.05);

    // Street Lamps with warm glowing LED lenses
    function createStreetLamp(x, z) {
      const lampGroup = new THREE.Group();

      const pole = new THREE.Mesh(
        new THREE.CylinderGeometry(0.12, 0.16, 8, 8),
        new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.6, roughness: 0.3 })
      );
      pole.position.y = 4;
      lampGroup.add(pole);

      const arm = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.08, 2.4, 8),
        new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.6 })
      );
      arm.rotation.z = Math.PI / 3 * (x > 0 ? -1 : 1);
      arm.position.set(x > 0 ? -1.0 : 1.0, 7.8, 0);
      lampGroup.add(arm);

      const head = new THREE.Mesh(
        new THREE.BoxGeometry(0.5, 0.25, 0.9),
        new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8 })
      );
      head.position.set(x > 0 ? -1.8 : 1.8, 8.2, 0);
      lampGroup.add(head);

      const bulb = new THREE.Mesh(
        new THREE.PlaneGeometry(0.4, 0.8),
        new THREE.MeshBasicMaterial({ color: 0xfef08a })
      );
      bulb.rotation.x = Math.PI / 2;
      bulb.position.set(x > 0 ? -1.8 : 1.8, 8.05, 0);
      lampGroup.add(bulb);

      lampGroup.position.set(x, 0, z);
      scene.add(lampGroup);
    }

    [-85, -60, -35, -10, 15].forEach(z => {
      createStreetLamp(-12.8, z);
      createStreetLamp(12.8, z);
    });

    // Chennai Avenue Trees (Gulmohar / Neem canopy)
    function createChennaiTree(x, z) {
      const tree = new THREE.Group();
      const trunkMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.9 });
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.45, 4.5, 7), trunkMat);
      trunk.position.y = 2.25;
      trunk.castShadow = true;
      tree.add(trunk);

      const leafMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.75, flatShading: true });
      const canopy1 = new THREE.Mesh(new THREE.DodecahedronGeometry(2.4, 1), leafMat);
      canopy1.position.y = 4.8;
      canopy1.castShadow = true;
      tree.add(canopy1);

      const canopy2 = new THREE.Mesh(new THREE.DodecahedronGeometry(1.8, 1), leafMat);
      canopy2.position.set(0.7, 5.8, -0.4);
      canopy2.castShadow = true;
      tree.add(canopy2);

      tree.position.set(x, 0, z);
      scene.add(tree);
    }
    [-75, -45, -15, 10, 25].forEach(z => {
      createChennaiTree(-16.8, z);
      createChennaiTree(16.8, z);
    });

    /* ==========================================================================
       6. ICONIC CHENNAI LANDMARKS (MATCHING REFERENCE IMAGE)
       ========================================================================== */

    // 1. DRAVIDIAN TEMPLE GOPURAM (Rising 28m high at North Avenue end, Z = -118)
    function buildDravidianTempleGopuram(x, z) {
      const gopuramGroup = new THREE.Group();
      const stoneMat = new THREE.MeshStandardMaterial({
        color: 0xd97706,
        roughness: 0.85,
        map: createTempleReliefTexture()
      });
      const goldMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.9, roughness: 0.2 });

      // Plinth base
      const plinth = new THREE.Mesh(new THREE.BoxGeometry(22, 4.0, 14), stoneMat);
      plinth.position.y = 2.0;
      plinth.castShadow = true;
      plinth.receiveShadow = true;
      gopuramGroup.add(plinth);

      // Grand Entrance Archway (Thoranam)
      const archHole = new THREE.Mesh(
        new THREE.BoxGeometry(5.0, 3.8, 14.5),
        new THREE.MeshStandardMaterial({ color: 0x1c1917, roughness: 0.9 })
      );
      archHole.position.y = 1.9;
      gopuramGroup.add(archHole);

      // 5 Stepped Pyramidal Tiers
      const tierHeights = [3.6, 3.2, 2.8, 2.5, 2.2];
      const tierWidths = [19, 16.5, 14, 11.5, 9.0];
      const tierDepths = [12, 10.5, 9.0, 7.5, 6.0];
      let currentY = 4.0;

      for (let t = 0; t < 5; t++) {
        const h = tierHeights[t];
        const w = tierWidths[t];
        const d = tierDepths[t];

        const tierMesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), stoneMat);
        tierMesh.position.y = currentY + h / 2;
        tierMesh.castShadow = true;
        gopuramGroup.add(tierMesh);

        // Ornamental Cornice Ledge
        const cornice = new THREE.Mesh(new THREE.BoxGeometry(w + 1.2, 0.45, d + 1.2), stoneMat);
        cornice.position.y = currentY + h + 0.22;
        gopuramGroup.add(cornice);

        currentY += h + 0.45;
      }

      // Vaulted Barrel Roof (Shikara)
      const shikara = new THREE.Mesh(
        new THREE.CylinderGeometry(2.4, 3.8, 3.5, 12),
        stoneMat
      );
      shikara.rotation.z = Math.PI / 2;
      shikara.scale.set(0.8, 1.4, 1.0);
      shikara.position.y = currentY + 1.6;
      gopuramGroup.add(shikara);

      // 5 Golden Kalasam Finials on Crest
      for (let k = -3.2; k <= 3.2; k += 1.6) {
        const kalasam = new THREE.Group();
        const basePot = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), goldMat);
        basePot.position.y = 0.35;
        kalasam.add(basePot);

        const spire = new THREE.Mesh(new THREE.ConeGeometry(0.18, 1.1, 10), goldMat);
        spire.position.y = 1.05;
        kalasam.add(spire);

        kalasam.position.set(k, currentY + 3.2, 0);
        gopuramGroup.add(kalasam);
      }

      gopuramGroup.position.set(x, 0, z);
      scene.add(gopuramGroup);
    }
    buildDravidianTempleGopuram(0, -118);

    // 2. RIPON BUILDING / GOVERNMENT PALACE (East Avenue, X = 32, Z = -35)
    function buildRiponBuilding(x, z) {
      const bGroup = new THREE.Group();
      const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.6 });
      const archMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
      const hedgeMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.9 });

      // Ground & 1st Floor Wings (Length: 38m, Height: 12m)
      const mainBody = new THREE.Mesh(new THREE.BoxGeometry(38, 12, 14), whiteMat);
      mainBody.position.y = 6;
      mainBody.castShadow = true;
      mainBody.receiveShadow = true;
      bGroup.add(mainBody);

      // Classical Arched Colonnade on Front Facade
      for (let cX = -16; cX <= 16; cX += 4) {
        // Lower Column
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.35, 11.5, 10), whiteMat);
        col.position.set(cX, 6, -7.3);
        bGroup.add(col);

        // Lower Arch Recess
        const arch = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.2, 0.4), archMat);
        arch.position.set(cX, 3.2, -6.9);
        bGroup.add(arch);

        // Upper Arch Recess
        const arch2 = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.0, 0.4), archMat);
        arch2.position.set(cX, 8.4, -6.9);
        bGroup.add(arch2);
      }

      // Grand Central Clock Tower (Height: 25m)
      const tower = new THREE.Mesh(new THREE.BoxGeometry(8.5, 18, 9), whiteMat);
      tower.position.set(0, 15, -1);
      tower.castShadow = true;
      bGroup.add(tower);

      // Working Clock Face on Front Tower Wall
      const clockTex = createClockFaceTexture();
      const clockMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(3.6, 3.6),
        new THREE.MeshStandardMaterial({ map: clockTex, roughness: 0.3 })
      );
      clockMesh.position.set(0, 19.5, -5.55);
      bGroup.add(clockMesh);

      // Central Dome (Colonial Indo-Saracenic Cupola)
      const domeBase = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 3.4, 1.8, 16), whiteMat);
      domeBase.position.set(0, 24.8, -1);
      bGroup.add(domeBase);

      const dome = new THREE.Mesh(new THREE.SphereGeometry(3.1, 16, 16, 0, Math.PI * 2, 0, Math.PI / 2), whiteMat);
      dome.position.set(0, 25.7, -1);
      bGroup.add(dome);

      // Tall 12m Flagpole with fluttering Indian National Flag
      const flagPole = new THREE.Mesh(
        new THREE.CylinderGeometry(0.06, 0.08, 10, 8),
        new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9 })
      );
      flagPole.position.set(0, 31, -1);
      bGroup.add(flagPole);

      const flagMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(3.2, 2.1),
        new THREE.MeshStandardMaterial({ map: createIndianFlagTexture(), side: THREE.DoubleSide })
      );
      flagMesh.position.set(1.65, 33.5, -1);
      bGroup.add(flagMesh);

      // Front Manicured Garden Lawn and Hedges
      const lawn = new THREE.Mesh(
        new THREE.BoxGeometry(36, 0.2, 8),
        new THREE.MeshStandardMaterial({ color: 0x16a34a, roughness: 0.85 })
      );
      lawn.position.set(0, 0.1, -11.5);
      lawn.receiveShadow = true;
      bGroup.add(lawn);

      for (let hX = -16; hX <= 16; hX += 4) {
        const hedge = new THREE.Mesh(new THREE.BoxGeometry(3.2, 1.1, 1.2), hedgeMat);
        hedge.position.set(hX, 0.65, -15);
        bGroup.add(hedge);
      }

      bGroup.position.set(x, 0, z);
      scene.add(bGroup);
    }
    buildRiponBuilding(33, -35);

    // 3. CHENNAI STREET VEGETABLE MARKET & FRUIT STALL (West Avenue, X = -15, Z = -12)
    function buildStreetVegetableMarket(x, z) {
      const marketGroup = new THREE.Group();
      const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 });

      // Wooden Table Counters
      const table = new THREE.Mesh(new THREE.BoxGeometry(7.5, 0.9, 2.4), woodMat);
      table.position.set(0, 0.45, 0);
      table.castShadow = true;
      marketGroup.add(table);

      // Multi-Colored Produce Crates & Baskets
      const crateConfigs = [
        { col: 0xef4444, x: -2.8, name: 'Tomatoes' },
        { col: 0xf97316, x: -1.4, name: 'Carrots' },
        { col: 0x22c55e, x: 0.0, name: 'Greens' },
        { col: 0xeab308, x: 1.4, name: 'Bananas' },
        { col: 0x78350f, x: 2.8, name: 'Coconuts' }
      ];

      crateConfigs.forEach(cr => {
        // Wooden Crate
        const crate = new THREE.Mesh(
          new THREE.BoxGeometry(1.1, 0.35, 1.6),
          new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.8 })
        );
        crate.position.set(cr.x, 1.05, 0);
        marketGroup.add(crate);

        // Vegetable / Fruit mound inside
        const produce = new THREE.Mesh(
          new THREE.SphereGeometry(0.48, 10, 8),
          new THREE.MeshStandardMaterial({ color: cr.col, roughness: 0.5 })
        );
        produce.scale.set(1.1, 0.6, 1.4);
        produce.position.set(cr.x, 1.28, 0);
        marketGroup.add(produce);
      });

      // Striped Tarpaulin Awning Roof
      const awnTexCv = document.createElement('canvas');
      awnTexCv.width = 128; awnTexCv.height = 64;
      const ac = awnTexCv.getContext('2d');
      for (let i = 0; i < 128; i += 32) {
        ac.fillStyle = '#dc2626'; ac.fillRect(i, 0, 16, 64);
        ac.fillStyle = '#fde047'; ac.fillRect(i + 16, 0, 16, 64);
      }
      const awnTex = new THREE.CanvasTexture(awnTexCv);
      awnTex.wrapS = THREE.RepeatWrapping;
      awnTex.repeat.set(4, 1);

      const awning = new THREE.Mesh(
        new THREE.PlaneGeometry(8.2, 3.2),
        new THREE.MeshStandardMaterial({ map: awnTex, side: THREE.DoubleSide })
      );
      awning.rotation.x = Math.PI / 3;
      awning.position.set(0, 2.6, 0.4);
      marketGroup.add(awning);

      // 4 Bamboo Support Poles
      [[-3.8, -1.0], [3.8, -1.0], [-3.8, 1.2], [3.8, 1.2]].forEach(p => {
        const pole = new THREE.Mesh(
          new THREE.CylinderGeometry(0.04, 0.05, 2.8, 8),
          new THREE.MeshStandardMaterial({ color: 0x78350f })
        );
        pole.position.set(p[0], 1.4, p[1]);
        marketGroup.add(pole);
      });

      // Blackboard Price List Signboard
      const signMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(2.2, 1.1),
        new THREE.MeshStandardMaterial({
          map: createShopSignTexture('FRESH VEGETABLES', 'DAILY CHENNAI WHOLESALE', '#15803d', '#ffffff', '🥕')
        })
      );
      signMesh.position.set(0, 3.2, 0.4);
      marketGroup.add(signMesh);

      marketGroup.position.set(x, 0, z);
      scene.add(marketGroup);
    }
    buildStreetVegetableMarket(-14.5, -12);

    // 4. CHENNAI MTC BUS STOP SHELTER (East Avenue, X = 14.5, Z = -58)
    function buildChennaiMTCBusStop(x, z) {
      const busStopGroup = new THREE.Group();
      const steelMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8, roughness: 0.2 });
      const blueMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.4 });

      // Curved Blue Metal Canopy Roof
      const roof = new THREE.Mesh(
        new THREE.CylinderGeometry(2.8, 2.8, 6.5, 16, 1, false, 0, Math.PI / 1.5),
        blueMat
      );
      roof.rotation.z = Math.PI / 2;
      roof.position.set(0, 3.0, 0);
      busStopGroup.add(roof);

      // Stainless Steel Support Pillars
      [-2.8, 2.8].forEach(pX => {
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 3.2, 8), steelMat);
        pillar.position.set(pX, 1.6, -1.0);
        busStopGroup.add(pillar);
      });

      // Passenger Seating Bench
      const bench = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.45, 0.6), steelMat);
      bench.position.set(0, 0.45, -0.8);
      busStopGroup.add(bench);

      // English MTC Route Board Sign
      const signTex = createShopSignTexture('MTC BUS STOP', 'WARD 12 - ROUTE 29C', '#0284c7', '#ffffff', '🚏');
      const signMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(3.4, 0.9),
        new THREE.MeshStandardMaterial({ map: signTex })
      );
      signMesh.position.set(0, 3.4, 0.8);
      busStopGroup.add(signMesh);

      busStopGroup.position.set(x, 0, z);
      scene.add(busStopGroup);
    }
    buildChennaiMTCBusStop(14.5, -58);

    // 5. PUBLIC WATER CRISIS SETUP & ORDERLY ROWS OF PLASTIC POTS (KUDAM)
    function buildWaterSupplySetup(x, z) {
      const point = new THREE.Group();

      // Standpost concrete base
      const base = new THREE.Mesh(
        new THREE.BoxGeometry(3.0, 0.35, 3.0),
        new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.9 })
      );
      base.position.y = 0.175;
      point.add(base);

      // Iron water pipe and manifold bibcock
      const pipe = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.08, 1.4, 8),
        new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.7 })
      );
      pipe.position.set(0, 0.85, 0);
      point.add(pipe);

      for (let a = 0; a < Math.PI * 2; a += Math.PI / 2) {
        const tap = new THREE.Mesh(
          new THREE.BoxGeometry(0.12, 0.15, 0.3),
          new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.9 })
        );
        tap.position.set(Math.sin(a) * 0.25, 1.4, Math.cos(a) * 0.25);
        point.add(tap);
      }

      // Orderly rows of colorful plastic water pots (Kudam)
      const potColors = [0x0284c7, 0xf59e0b, 0xef4444, 0x10b981, 0xec4899, 0x8b5cf6];
      for (let r = 0; r < 3; r++) {
        for (let c = -3; c <= 3; c++) {
          const colIdx = Math.abs((r * 3 + c) % potColors.length);
          const potMat = new THREE.MeshStandardMaterial({ color: potColors[colIdx], roughness: 0.4 });

          const potBottom = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), potMat);
          potBottom.position.set(c * 0.65, 0.38, 2.0 + r * 0.65);
          potBottom.scale.set(1.0, 0.85, 1.0);
          point.add(potBottom);

          const potNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.14, 0.16, 12), potMat);
          potNeck.position.set(c * 0.65, 0.58, 2.0 + r * 0.65);
          point.add(potNeck);
        }
      }

      // Protest / Grievance Signboard in English
      const signMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(2.4, 1.0),
        new THREE.MeshStandardMaterial({
          map: createShopSignTexture('WATER CRISIS - WARD 12', 'CITIZENS DEMAND 24/7 PIPED WATER', '#dc2626', '#ffffff', '🚰')
        })
      );
      signMesh.position.set(0, 2.2, -1.2);
      point.add(signMesh);

      point.position.set(x, 0, z);
      scene.add(point);
    }
    buildWaterSupplySetup(-14.5, -24);

    // 6. CHENNAI RESIDENTIAL APARTMENTS & COMMERCIAL SHOPS
    const buildingColors = [0xfef3c7, 0xfce7f3, 0xe0e7ff, 0xdcfce7, 0xffedd5, 0xf1f5f9];
    const shopDefinitions = [
      { z: -5, side: 1, main: 'Ward 12 Welfare Office', sub: 'Citizens Council & Campaign Secretariat', bg: '#0369a1', icon: '🏛️' },
      { z: -5, side: -1, main: 'Amudham Tea Stall', sub: 'Traditional Filter Coffee & Hot Snacks', bg: '#92400e', icon: '☕' },
      { z: -28, side: -1, main: 'Saravana 24H Pharmacy', sub: 'Healthcare & Essential Medicines', bg: '#047857', icon: '⚕️' },
      { z: -28, side: 1, main: 'Annai Digital Xerox', sub: 'Government Citizen Portal & Printing', bg: '#1e3a8a', icon: '📄' },
      { z: -65, side: 1, main: 'Balaji Tiffin Centre', sub: 'Authentic South Indian Meals & Idly', bg: '#b45309', icon: '🍲' },
      { z: -65, side: -1, main: 'Vasanth Electricals', sub: 'Hardware, Cables & Water Pumps', bg: '#4338ca', icon: '💡' }
    ];

    function createChennaiBuilding(x, z, width, height, depth, colorHex, shopData = null) {
      const bGroup = new THREE.Group();
      const mainMat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.85 });
      const mainBox = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth), mainMat);
      mainBox.position.y = height / 2;
      mainBox.castShadow = true;
      mainBox.receiveShadow = true;
      bGroup.add(mainBox);

      // Balconies & architectural overhangs
      const balconyMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.4 });
      for (let floorY = 4.5; floorY < height - 1.5; floorY += 3.4) {
        const balc = new THREE.Mesh(new THREE.BoxGeometry(width * 0.7, 0.2, 1.2), mainMat);
        balc.position.set(0, floorY, (depth / 2 + 0.6) * (x < 0 ? 1 : -1));
        bGroup.add(balc);

        const railing = new THREE.Mesh(new THREE.BoxGeometry(width * 0.7, 0.9, 0.08), balconyMat);
        railing.position.set(0, floorY + 0.45, (depth / 2 + 1.15) * (x < 0 ? 1 : -1));
        bGroup.add(railing);
      }

      // Rooftop Sintex Water Tank (Black/Blue cylindrical tank)
      const tankMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 });
      const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 1.6, 16), tankMat);
      tank.position.set(width * 0.25, height + 0.8, depth * 0.2);
      bGroup.add(tank);

      // AC Outdoor Condenser Unit on wall
      const acUnit = new THREE.Mesh(
        new THREE.BoxGeometry(1.2, 0.9, 0.6),
        new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.3 })
      );
      acUnit.position.set(-width * 0.3, 5.5, (depth / 2 + 0.35) * (x < 0 ? 1 : -1));
      bGroup.add(acUnit);

      // Ground Floor Shopfront Signboard in English
      if (shopData) {
        const signTex = createShopSignTexture(shopData.main, shopData.sub, shopData.bg, '#ffffff', shopData.icon);
        const signMat = new THREE.MeshStandardMaterial({ map: signTex, roughness: 0.3 });
        const signMesh = new THREE.Mesh(new THREE.PlaneGeometry(width * 0.85, 2.2), signMat);
        signMesh.position.set(0, 3.8, (depth / 2 + 0.05) * (x < 0 ? 1 : -1));
        if (x > 0) signMesh.rotation.y = Math.PI;
        bGroup.add(signMesh);

        // Striped Awning
        const awningCv = document.createElement('canvas');
        awningCv.width = 128; awningCv.height = 64;
        const ac = awningCv.getContext('2d');
        for (let i = 0; i < 128; i += 32) {
          ac.fillStyle = '#ef4444'; ac.fillRect(i, 0, 16, 64);
          ac.fillStyle = '#ffffff'; ac.fillRect(i + 16, 0, 16, 64);
        }
        const awnTex = new THREE.CanvasTexture(awningCv);
        awnTex.wrapS = THREE.RepeatWrapping;
        awnTex.repeat.set(4, 1);
        const awning = new THREE.Mesh(
          new THREE.PlaneGeometry(width * 0.88, 1.6),
          new THREE.MeshStandardMaterial({ map: awnTex, side: THREE.DoubleSide })
        );
        awning.rotation.x = Math.PI / 4 * (x < 0 ? 1 : -1);
        if (x > 0) awning.rotation.y = Math.PI;
        awning.position.set(0, 2.7, (depth / 2 + 0.8) * (x < 0 ? 1 : -1));
        bGroup.add(awning);
      }

      bGroup.position.set(x, 0, z);
      scene.add(bGroup);
      return bGroup;
    }

    // Spawn Buildings along street
    for (let z = -90; z <= 30; z += 24) {
      const h1 = 12 + (Math.abs(z) % 7);
      const h2 = 14 + ((z + 10) % 5);
      const c1 = buildingColors[Math.abs(z) % buildingColors.length];
      const c2 = buildingColors[(Math.abs(z) + 2) % buildingColors.length];

      const s1 = shopDefinitions.find(s => Math.abs(s.z - z) < 12 && s.side === -1);
      const s2 = shopDefinitions.find(s => Math.abs(s.z - z) < 12 && s.side === 1);

      createChennaiBuilding(-24, z, 14, h1, 16, c1, s1);
      if (z > -20 || z < -50) {
        createChennaiBuilding(24, z, 14, h2, 16, c2, s2);
      }
    }

    // Election Flex Banners on roadside in English
    function createRoadsideBanner(x, z, rotY) {
      const bannerTex = createElectionBannerTexture();
      const bannerMat = new THREE.MeshStandardMaterial({ map: bannerTex, roughness: 0.4 });
      const banner = new THREE.Mesh(new THREE.PlaneGeometry(7, 3.8), bannerMat);
      banner.position.set(x, 2.8, z);
      banner.rotation.y = rotY;
      banner.castShadow = true;
      scene.add(banner);

      const frameMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 });
      const pole1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 5, 8), frameMat);
      pole1.position.set(x - 3.4, 2.5, z);
      scene.add(pole1);
      const pole2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 5, 8), frameMat);
      pole2.position.set(x + 3.4, 2.5, z);
      scene.add(pole2);
    }
    createRoadsideBanner(-11.5, -15, Math.PI / 2);
    createRoadsideBanner(11.5, -42, -Math.PI / 2);

    /* ==========================================================================
       7. DETAILED INDIAN VEHICLES (MATCHING REFERENCE IMAGE FLEET)
       ========================================================================== */

    // 1. WHITE AMBASSADOR VIP CAR (Player Driven)
    const carGroup = new THREE.Group();
    let carFrontWheels = [];
    let carAllWheels = [];
    let carBeaconLight = null;

    function buildAmbassadorCar() {
      const bodyMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.25, metalness: 0.2 });
      const chromeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.95, roughness: 0.1 });
      const glassMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.1, metalness: 0.8, transparent: true, opacity: 0.85 });

      // Lower Body
      const lowerBody = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.75, 4.6), bodyMat);
      lowerBody.position.y = 0.65;
      lowerBody.castShadow = true;
      carGroup.add(lowerBody);

      // Curved Hood
      const hood = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.45, 1.5), bodyMat);
      hood.position.set(0, 0.85, -1.45);
      carGroup.add(hood);

      // Rounded Cabin Top
      const cabin = new THREE.Mesh(new THREE.BoxGeometry(2.05, 0.75, 2.3), bodyMat);
      cabin.position.set(0, 1.35, 0.2);
      carGroup.add(cabin);

      // Windshields
      const windshield = new THREE.Mesh(new THREE.PlaneGeometry(1.85, 0.65), glassMat);
      windshield.rotation.x = -Math.PI / 5;
      windshield.position.set(0, 1.35, -0.96);
      carGroup.add(windshield);

      const rearGlass = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 0.65), glassMat);
      rearGlass.rotation.x = Math.PI / 5;
      rearGlass.rotation.y = Math.PI;
      rearGlass.position.set(0, 1.35, 1.36);
      carGroup.add(rearGlass);

      // Chrome Front Grille
      const grille = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.4, 0.1), chromeMat);
      grille.position.set(0, 0.72, -2.31);
      carGroup.add(grille);

      // Chrome Bumpers
      const frontBumper = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.22, 0.25), chromeMat);
      frontBumper.position.set(0, 0.45, -2.36);
      carGroup.add(frontBumper);

      const rearBumper = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.22, 0.25), chromeMat);
      rearBumper.position.set(0, 0.45, 2.36);
      carGroup.add(rearBumper);

      // Headlamps
      [-0.8, 0.8].forEach(xSide => {
        const lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.15, 16), chromeMat);
        lamp.rotation.x = Math.PI / 2;
        lamp.position.set(xSide, 0.8, -2.3);
        carGroup.add(lamp);

        const bulb = new THREE.Mesh(new THREE.CircleGeometry(0.14, 16), new THREE.MeshBasicMaterial({ color: 0xffedd5 }));
        bulb.position.set(xSide, 0.8, -2.38);
        carGroup.add(bulb);
      });

      // Red VIP Beacon on Roof
      const beaconBase = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.12, 12), chromeMat);
      beaconBase.position.set(0, 1.78, 0.2);
      carGroup.add(beaconBase);

      const beaconLens = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.14, 0.22, 12),
        new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 })
      );
      beaconLens.position.set(0, 1.9, 0.2);
      carGroup.add(beaconLens);

      carBeaconLight = new THREE.PointLight(0xef4444, 1.2, 12);
      carBeaconLight.position.set(0, 2.2, 0.2);
      carGroup.add(carBeaconLight);

      // Party flags on front fenders
      [-1.05, 1.05].forEach(xSide => {
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.8, 8), chromeMat);
        pole.position.set(xSide, 1.2, -2.0);
        carGroup.add(pole);

        const flag = new THREE.Mesh(
          new THREE.PlaneGeometry(0.35, 0.22),
          new THREE.MeshStandardMaterial({ color: 0xb91c1c, side: THREE.DoubleSide })
        );
        flag.position.set(xSide + (xSide > 0 ? 0.18 : -0.18), 1.45, -2.0);
        carGroup.add(flag);
      });

      // Wheels
      const wheelGeo = new THREE.CylinderGeometry(0.36, 0.36, 0.28, 16);
      const tireMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.9 });
      const capMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.2 });

      function makeWheel(x, z, isFront) {
        const wGroup = new THREE.Group();
        const tire = new THREE.Mesh(wheelGeo, tireMat);
        tire.rotation.z = Math.PI / 2;
        tire.castShadow = true;
        wGroup.add(tire);

        const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.29, 12), capMat);
        cap.rotation.z = Math.PI / 2;
        wGroup.add(cap);

        wGroup.position.set(x, 0.36, z);
        carGroup.add(wGroup);
        carAllWheels.push(wGroup);
        if (isFront) carFrontWheels.push(wGroup);
      }

      makeWheel(-1.12, -1.4, true);
      makeWheel(1.12, -1.4, true);
      makeWheel(-1.12, 1.4, false);
      makeWheel(1.12, 1.4, false);

      carGroup.position.set(4, 0, -45);
      scene.add(carGroup);
    }
    buildAmbassadorCar();

    // 2. CHENNAI METRO WATER TANKER (Blue Tanker at Z = -28)
    const tankerGroup = new THREE.Group();
    function buildWaterTanker() {
      const yellowCabMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.5 });
      const tankMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.6, roughness: 0.25 });
      const steelMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.8, roughness: 0.3 });

      // Truck Driver Cabin
      const cab = new THREE.Mesh(new THREE.BoxGeometry(2.7, 2.6, 2.4), yellowCabMat);
      cab.position.set(0, 1.8, -3.2);
      cab.castShadow = true;
      tankerGroup.add(cab);

      // Cabin Front Windscreen
      const wind = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 1.0), new THREE.MeshBasicMaterial({ color: 0x0f172a }));
      wind.position.set(0, 2.1, -4.41);
      tankerGroup.add(wind);

      // Bumper
      const bumper = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.45, 0.35), steelMat);
      bumper.position.set(0, 0.65, -4.4);
      tankerGroup.add(bumper);

      // Massive Cylindrical Water Tank
      const tank = new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 6.4, 24), tankMat);
      tank.rotation.x = Math.PI / 2;
      tank.position.set(0, 2.2, 1.0);
      tank.castShadow = true;
      tankerGroup.add(tank);

      // Stencil Plate: "CHENNAI WATER SUPPLY"
      const stencilCv = document.createElement('canvas');
      stencilCv.width = 512; stencilCv.height = 128;
      const sCtx = stencilCv.getContext('2d');
      sCtx.fillStyle = '#0284c7'; sCtx.fillRect(0, 0, 512, 128);
      sCtx.fillStyle = '#ffffff'; sCtx.font = '900 32px sans-serif'; sCtx.textAlign = 'center';
      sCtx.fillText('CHENNAI WATER SUPPLY', 256, 50);
      sCtx.fillStyle = '#fde047'; sCtx.font = 'bold 22px sans-serif';
      sCtx.fillText('WARD 12 EMERGENCY DRINKING WATER', 256, 92);
      const stencilTex = new THREE.CanvasTexture(stencilCv);
      const stencilMesh = new THREE.Mesh(new THREE.PlaneGeometry(4.8, 1.2), new THREE.MeshStandardMaterial({ map: stencilTex }));
      stencilMesh.position.set(1.48, 2.2, 1.0);
      stencilMesh.rotation.y = Math.PI / 2;
      tankerGroup.add(stencilMesh);

      // Rear Dispensing Manifold (Taps & Valves)
      const manifold = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.5, 0.4), steelMat);
      manifold.position.set(0, 1.0, 4.3);
      tankerGroup.add(manifold);

      for (let i = -0.8; i <= 0.8; i += 0.4) {
        const tap = new THREE.Mesh(
          new THREE.CylinderGeometry(0.06, 0.06, 0.35, 8),
          new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.9 })
        );
        tap.position.set(i, 0.8, 4.5);
        tankerGroup.add(tap);
      }

      // Wheels
      const tGeo = new THREE.CylinderGeometry(0.48, 0.48, 0.38, 16);
      const tMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 });
      [
        [-1.3, -3.0], [1.3, -3.0],
        [-1.3, 1.2], [1.3, 1.2],
        [-1.3, 2.6], [1.3, 2.6]
      ].forEach(pos => {
        const w = new THREE.Mesh(tGeo, tMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(pos[0], 0.48, pos[1]);
        tankerGroup.add(w);
      });

      tankerGroup.position.set(-6, 0, -28);
      scene.add(tankerGroup);
    }
    buildWaterTanker();

    // 3. CHENNAI AUTO-RICKSHAW (Bajaj style 3-wheeler)
    function buildAutoRickshaw(x, z, rotY) {
      const auto = new THREE.Group();
      const yellowTopMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.35 });
      const greenBaseMat = new THREE.MeshStandardMaterial({ color: 0x166534, roughness: 0.4 });
      const blackMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });

      // Lower chassis
      const base = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.6, 2.5), greenBaseMat);
      base.position.y = 0.55;
      auto.add(base);

      // Yellow canopy roof
      const roof = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.15, 2.2), yellowTopMat);
      roof.position.set(0, 1.75, 0.1);
      auto.add(roof);

      // Support pillars
      [[-0.65, -0.9], [0.65, -0.9], [-0.65, 1.1], [0.65, 1.1]].forEach(p => {
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.1, 8), blackMat);
        pillar.position.set(p[0], 1.2, p[1]);
        auto.add(pillar);
      });

      // Front windscreen
      const ws = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 0.7), new THREE.MeshBasicMaterial({ color: 0x1e293b }));
      ws.rotation.x = -Math.PI / 10;
      ws.position.set(0, 1.25, -1.0);
      auto.add(ws);

      // Headlamp
      const light = new THREE.Mesh(new THREE.CircleGeometry(0.12, 12), new THREE.MeshBasicMaterial({ color: 0xfef08a }));
      light.position.set(0, 0.75, -1.26);
      auto.add(light);

      // 3 Wheels
      const wGeo = new THREE.CylinderGeometry(0.28, 0.28, 0.2, 14);
      const fw = new THREE.Mesh(wGeo, blackMat);
      fw.rotation.z = Math.PI / 2;
      fw.position.set(0, 0.28, -1.1);
      auto.add(fw);

      [-0.75, 0.75].forEach(rwX => {
        const rw = new THREE.Mesh(wGeo, blackMat);
        rw.rotation.z = Math.PI / 2;
        rw.position.set(rwX, 0.28, 0.85);
        auto.add(rw);
      });

      auto.position.set(x, 0, z);
      auto.rotation.y = rotY;
      scene.add(auto);
      return auto;
    }
    buildAutoRickshaw(6.5, 8, -Math.PI / 2);
    buildAutoRickshaw(-6.8, -12, Math.PI / 4);

    // 4. CHENNAI MTC CITY TRANSIT BUS
    function buildChennaiMTCBus(x, z, rotY) {
      const bus = new THREE.Group();
      const blueMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.4 });
      const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.5 });
      const glassMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.2 });

      // Lower Blue Body
      const lower = new THREE.Mesh(new THREE.BoxGeometry(2.8, 1.6, 10.5), blueMat);
      lower.position.y = 1.2;
      lower.castShadow = true;
      bus.add(lower);

      // Upper White Top
      const upper = new THREE.Mesh(new THREE.BoxGeometry(2.78, 1.4, 10.45), whiteMat);
      upper.position.y = 2.65;
      bus.add(upper);

      // Front Destination Board in English ("MTC 29C: BESANT NAGAR")
      const cvs = document.createElement('canvas');
      cvs.width = 256; cvs.height = 64;
      const c = cvs.getContext('2d');
      c.fillStyle = '#0f172a'; c.fillRect(0, 0, 256, 64);
      c.fillStyle = '#fde047'; c.font = 'bold 22px sans-serif'; c.textAlign = 'center';
      c.fillText('MTC 29C: BESANT NAGAR', 128, 42);
      const destTex = new THREE.CanvasTexture(cvs);
      const destMesh = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 0.6), new THREE.MeshBasicMaterial({ map: destTex }));
      destMesh.position.set(0, 3.0, -5.26);
      bus.add(destMesh);

      // Large Front Windscreen
      const wind = new THREE.Mesh(new THREE.PlaneGeometry(2.5, 1.1), glassMat);
      wind.position.set(0, 2.1, -5.26);
      bus.add(wind);

      // Wheels
      const bwGeo = new THREE.CylinderGeometry(0.5, 0.5, 0.4, 16);
      const bwMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.9 });
      [
        [-1.38, -3.6], [1.38, -3.6],
        [-1.38, 2.8], [1.38, 2.8],
        [-1.38, 4.1], [1.38, 4.1]
      ].forEach(pos => {
        const w = new THREE.Mesh(bwGeo, bwMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(pos[0], 0.5, pos[1]);
        bus.add(w);
      });

      bus.position.set(x, 0, z);
      bus.rotation.y = rotY;
      scene.add(bus);
      return bus;
    }
    buildChennaiMTCBus(17.5, -60, Math.PI);

    // 5. INDIAN COMMUTER MOTORCYCLE (Hero Splendor / Pulsar style)
    function buildMotorcycle(x, z, rotY) {
      const bike = new THREE.Group();
      const tankMat = new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.3 });
      const chromeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.95, roughness: 0.1 });
      const blackMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.8 });

      // Chassis & Engine Block
      const engine = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.4, 0.6), chromeMat);
      engine.position.y = 0.5;
      bike.add(engine);

      // Fuel Tank
      const tank = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.32, 0.75), tankMat);
      tank.position.set(0, 0.88, -0.15);
      bike.add(tank);

      // Seat
      const seat = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.18, 0.85), blackMat);
      seat.position.set(0, 0.88, 0.45);
      bike.add(seat);

      // Chrome Exhaust Pipe
      const exhaust = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 1.2, 8), chromeMat);
      exhaust.rotation.x = Math.PI / 2;
      exhaust.position.set(0.24, 0.35, 0.3);
      bike.add(exhaust);

      // Handlebars & Headlamp
      const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.85, 8), chromeMat);
      handle.rotation.z = Math.PI / 2;
      handle.position.set(0, 1.15, -0.55);
      bike.add(handle);

      const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 10), chromeMat);
      lamp.position.set(0, 1.05, -0.68);
      bike.add(lamp);

      // Spoked Wheels
      const wGeo = new THREE.CylinderGeometry(0.34, 0.34, 0.12, 14);
      [-0.9, 0.9].forEach(zPos => {
        const w = new THREE.Mesh(wGeo, blackMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(0, 0.34, zPos);
        bike.add(w);
      });

      bike.position.set(x, 0, z);
      bike.rotation.y = rotY;
      scene.add(bike);
      return bike;
    }
    buildMotorcycle(6.8, -18, -Math.PI / 3);
    buildMotorcycle(-7.2, 2, Math.PI / 6);

    // 6. TAMIL NADU POLICE CAR / SUV (White with blue decals & flashing roof beacon)
    function buildPoliceCar(x, z, rotY) {
      const suv = new THREE.Group();
      const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 });
      const blueStripeMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.4 });
      const blackMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });

      // SUV Main Body
      const body = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.1, 4.8), whiteMat);
      body.position.y = 0.9;
      body.castShadow = true;
      suv.add(body);

      // Cabin Top
      const cabin = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.9, 2.8), whiteMat);
      cabin.position.set(0, 1.85, 0.2);
      suv.add(cabin);

      // Blue Police Side Stripes
      [-1.21, 1.21].forEach(xSide => {
        const stripe = new THREE.Mesh(new THREE.PlaneGeometry(4.5, 0.3), blueStripeMat);
        stripe.position.set(xSide, 0.9, 0);
        stripe.rotation.y = xSide > 0 ? Math.PI / 2 : -Math.PI / 2;
        suv.add(stripe);
      });

      // Front Bull-Bar
      const bullBar = new THREE.Mesh(
        new THREE.BoxGeometry(2.3, 0.5, 0.15),
        new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.8 })
      );
      bullBar.position.set(0, 0.65, -2.45);
      suv.add(bullBar);

      // Dual Red/Blue Flashing Roof Lightbar
      const redLight = new THREE.Mesh(
        new THREE.BoxGeometry(0.4, 0.18, 0.25),
        new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 })
      );
      redLight.position.set(-0.35, 2.38, 0.2);
      suv.add(redLight);

      const blueLight = new THREE.Mesh(
        new THREE.BoxGeometry(0.4, 0.18, 0.25),
        new THREE.MeshStandardMaterial({ color: 0x0284c7, emissive: 0x0284c7, emissiveIntensity: 0.9 })
      );
      blueLight.position.set(0.35, 2.38, 0.2);
      suv.add(blueLight);

      // 4 SUV Wheels
      const wGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.32, 16);
      [[-1.15, -1.4], [1.15, -1.4], [-1.15, 1.4], [1.15, 1.4]].forEach(pos => {
        const w = new THREE.Mesh(wGeo, blackMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(pos[0], 0.42, pos[1]);
        suv.add(w);
      });

      suv.position.set(x, 0, z);
      suv.rotation.y = rotY;
      scene.add(suv);
      return suv;
    }
    buildPoliceCar(-7.5, -48, Math.PI / 2);

    // 7. AMBULANCE (White with Red Cross & Siren)
    function buildAmbulance(x, z, rotY) {
      const amb = new THREE.Group();
      const whiteMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
      const redCrossMat = new THREE.MeshStandardMaterial({ color: 0xdc2626 });
      const blackMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });

      const body = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.6, 5.0), whiteMat);
      body.position.y = 1.25;
      body.castShadow = true;
      amb.add(body);

      // Red Cross on side
      [-1.21, 1.21].forEach(xSide => {
        const crossH = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.3), redCrossMat);
        crossH.position.set(xSide, 1.4, 0.2);
        crossH.rotation.y = xSide > 0 ? Math.PI / 2 : -Math.PI / 2;
        amb.add(crossH);

        const crossV = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.9), redCrossMat);
        crossV.position.set(xSide, 1.4, 0.2);
        crossV.rotation.y = xSide > 0 ? Math.PI / 2 : -Math.PI / 2;
        amb.add(crossV);
      });

      // Roof Beacon
      const beacon = new THREE.Mesh(
        new THREE.CylinderGeometry(0.18, 0.18, 0.25, 12),
        new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 })
      );
      beacon.position.set(0, 2.15, -0.6);
      amb.add(beacon);

      const wGeo = new THREE.CylinderGeometry(0.4, 0.4, 0.3, 14);
      [[-1.15, -1.5], [1.15, -1.5], [-1.15, 1.5], [1.15, 1.5]].forEach(pos => {
        const w = new THREE.Mesh(wGeo, blackMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(pos[0], 0.4, pos[1]);
        amb.add(w);
      });

      amb.position.set(x, 0, z);
      amb.rotation.y = rotY;
      scene.add(amb);
      return amb;
    }
    buildAmbulance(17.0, -10, Math.PI / 3);

    // 8. HEAVY COMMERCIAL TIPPER TRUCK
    function buildHeavyTruck(x, z, rotY) {
      const truck = new THREE.Group();
      const cabMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.4 });
      const bedMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7 });
      const blackMat = new THREE.MeshStandardMaterial({ color: 0x111827 });

      // Cabin
      const cab = new THREE.Mesh(new THREE.BoxGeometry(2.6, 2.2, 2.2), cabMat);
      cab.position.set(0, 1.6, -2.6);
      cab.castShadow = true;
      truck.add(cab);

      // Heavy Cargo Tipper Bed
      const bed = new THREE.Mesh(new THREE.BoxGeometry(2.8, 1.8, 5.2), bedMat);
      bed.position.set(0, 1.6, 1.4);
      bed.castShadow = true;
      truck.add(bed);

      // 6 Heavy Wheels
      const wGeo = new THREE.CylinderGeometry(0.5, 0.5, 0.35, 16);
      [
        [-1.35, -2.4], [1.35, -2.4],
        [-1.35, 1.2], [1.35, 1.2],
        [-1.35, 2.6], [1.35, 2.6]
      ].forEach(pos => {
        const w = new THREE.Mesh(wGeo, blackMat);
        w.rotation.z = Math.PI / 2;
        w.position.set(pos[0], 0.5, pos[1]);
        truck.add(w);
      });

      truck.position.set(x, 0, z);
      truck.rotation.y = rotY;
      scene.add(truck);
      return truck;
    }
    buildHeavyTruck(6.5, -95, 0);

    /* ==========================================================================
       8. MEGA RALLY CAMPAIGN STAGE & RIGGING (At Z = -75)
       ========================================================================== */
    const rallyStageGroup = new THREE.Group();
    function buildMegaRallyStage() {
      // Stage platform with red carpet
      const woodMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8 });
      const stageBase = new THREE.Mesh(new THREE.BoxGeometry(18, 1.8, 11), woodMat);
      stageBase.position.y = 0.9;
      stageBase.receiveShadow = true;
      rallyStageGroup.add(stageBase);

      const redCarpet = new THREE.Mesh(
        new THREE.PlaneGeometry(17.6, 10.6),
        new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.95 })
      );
      redCarpet.rotation.x = -Math.PI / 2;
      redCarpet.position.set(0, 1.81, 0);
      rallyStageGroup.add(redCarpet);

      // Giant Campaign Backdrop in English
      const backdropTex = createRallyBackdropTexture();
      const backdrop = new THREE.Mesh(
        new THREE.PlaneGeometry(16.5, 6.2),
        new THREE.MeshStandardMaterial({ map: backdropTex, roughness: 0.4 })
      );
      backdrop.position.set(0, 4.9, -5.2);
      rallyStageGroup.add(backdrop);

      // Aluminum Overhead Truss Arch
      const trussMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 });
      [-8.2, 8.2].forEach(trussX => {
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 7.5, 8), trussMat);
        pillar.position.set(trussX, 4.5, -4.8);
        rallyStageGroup.add(pillar);
      });

      const topBar = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 16.8, 8), trussMat);
      topBar.rotation.z = Math.PI / 2;
      topBar.position.set(0, 8.2, -4.8);
      rallyStageGroup.add(topBar);

      // Colored Stage Spotlights (Saffron, White, Green, Blue)
      const spotColors = [0xf59e0b, 0xffffff, 0x10b981, 0x38bdf8];
      spotColors.forEach((col, idx) => {
        const spotMesh = new THREE.Mesh(
          new THREE.ConeGeometry(0.3, 0.6, 12),
          new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: 0.8 })
        );
        const xPos = -6 + idx * 4;
        spotMesh.rotation.x = Math.PI / 3;
        spotMesh.position.set(xPos, 8.0, -4.6);
        rallyStageGroup.add(spotMesh);
      });

      // Speaker Podium with Microphones
      const podium = new THREE.Mesh(
        new THREE.BoxGeometry(1.2, 1.3, 0.9),
        new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 })
      );
      podium.position.set(0, 2.45, 2.5);
      podium.castShadow = true;
      rallyStageGroup.add(podium);

      for (let m = -0.3; m <= 0.3; m += 0.2) {
        const mic = new THREE.Mesh(
          new THREE.CylinderGeometry(0.02, 0.02, 0.4, 8),
          new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9 })
        );
        mic.position.set(m, 3.25, 2.3);
        rallyStageGroup.add(mic);
      }

      // Traditional Indian Funnel Horn Loudspeakers
      [-9.8, 9.8].forEach(sideX => {
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 10, 8), woodMat);
        pole.position.set(sideX, 5.0, 4.0);
        rallyStageGroup.add(pole);

        for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 2) {
          const horn = new THREE.Mesh(
            new THREE.ConeGeometry(0.4, 0.8, 12, 1, true),
            new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.7, side: THREE.DoubleSide })
          );
          horn.rotation.x = Math.PI / 2;
          horn.rotation.y = angle;
          horn.position.set(sideX + Math.sin(angle) * 0.4, 9.2, 4.0 + Math.cos(angle) * 0.4);
          rallyStageGroup.add(horn);
        }
      });

      rallyStageGroup.position.set(0, 0, -75);
      scene.add(rallyStageGroup);
    }
    buildMegaRallyStage();

    /* ==========================================================================
       9. ADVANCED 3D HUMANOID RIGS & CHARACTER ARTIST PIPELINE
       ========================================================================== */
    function createHumanoidRig(options = {}) {
      const {
        shirtColor = 0xffffff,
        lowerColor = 0xf8fafc,
        skinColor = 0xa16207,
        hairColor = 0x09090b,
        hasMustache = true,
        hasBeard = false,
        hasGoggles = false,
        hasCap = false,
        capColor = 0x1e3a8a,
        hasSash = false,
        sashColor = 0xb91c1c,
        isTricolorScarf = false,
        hasDupatta = false,
        dupattaColor = 0x0284c7,
        isSaree = false,
        palluColor = 0xf59e0b,
        hasFlowers = false,
        hasKhakiPolice = false,
        hasDSLR = false,
        hasCane = false,
        hasBackpack = false,
        hasApron = false,
        hasPot = false,
        potColor = 0x0284c7
      } = options;

      const rig = new THREE.Group();

      const skinMat = new THREE.MeshStandardMaterial({ color: skinColor, roughness: 0.7 });
      const shirtMat = new THREE.MeshStandardMaterial({ color: shirtColor, roughness: 0.6 });
      const lowerMat = new THREE.MeshStandardMaterial({ color: lowerColor, roughness: 0.7 });
      const hairMat = new THREE.MeshStandardMaterial({ color: hairColor, roughness: 0.85 });
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0x271711, roughness: 0.8 });

      // Torso / Chest (Height: 0.80, Center: 1.35)
      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.80, 0.40), shirtMat);
      torso.position.y = 1.35;
      torso.castShadow = true;
      rig.add(torso);

      // Pelvis / Hips (Grounds torso to legs)
      const pelvis = new THREE.Mesh(new THREE.BoxGeometry(0.70, 0.24, 0.38), lowerMat);
      pelvis.position.y = 0.93;
      pelvis.castShadow = true;
      rig.add(pelvis);

      // Shirt Collar
      const collar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.18, 0.22, 0.08, 12),
        shirtMat
      );
      collar.position.set(0, 0.42, 0);
      torso.add(collar);

      // Neck & Head (Anatomically anchored to top of collar)
      const headGroup = new THREE.Group();
      
      const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.13, 0.18, 10), skinMat);
      neck.position.y = 0.09;
      headGroup.add(neck);

      const head = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 16), skinMat);
      head.position.y = 0.28;
      head.scale.set(1.0, 1.15, 1.05);
      headGroup.add(head);

      // Ears
      [-0.24, 0.24].forEach(earX => {
        const ear = new THREE.Mesh(new THREE.SphereGeometry(0.055, 8, 8), skinMat);
        ear.scale.set(0.6, 1.2, 0.8);
        ear.position.set(earX, 0.28, 0.02);
        headGroup.add(ear);
      });

      // Layered Hair
      const hair = new THREE.Mesh(new THREE.SphereGeometry(0.255, 16, 16, 0, Math.PI * 2, 0, Math.PI / 1.7), hairMat);
      hair.position.set(0, 0.33, -0.02);
      headGroup.add(hair);

      const hairSides = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.22, 0.42), hairMat);
      hairSides.position.set(0, 0.32, -0.06);
      headGroup.add(hairSides);

      // Jasmine Flowers in Hair (Malli Poo)
      if (hasFlowers) {
        const flowerMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
        const garland = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.045, 8, 16), flowerMat);
        garland.position.set(0, 0.32, -0.16);
        headGroup.add(garland);
      }

      // Facial Features (Mustache & Beard)
      if (hasMustache) {
        const mustache = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.06), hairMat);
        mustache.position.set(0, 0.22, 0.24);
        headGroup.add(mustache);
      }
      if (hasBeard) {
        const beard = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.12, 0.16), hairMat);
        beard.position.set(0, 0.14, 0.17);
        headGroup.add(beard);
      }

      // Eyeglasses
      if (hasGoggles) {
        const specMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.9, roughness: 0.1 });
        const spec = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.08, 0.08), specMat);
        spec.position.set(0, 0.30, 0.24);
        headGroup.add(spec);
      }

      // Cap
      if (hasCap) {
        const capMat = new THREE.MeshStandardMaterial({ color: capColor, roughness: 0.5 });
        const capCrown = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.27, 0.14, 16), capMat);
        capCrown.position.set(0, 0.46, -0.02);
        headGroup.add(capCrown);
        const capVisor = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.2), capMat);
        capVisor.rotation.x = -Math.PI / 6;
        capVisor.position.set(0, 0.43, 0.22);
        headGroup.add(capVisor);
      }

      headGroup.position.set(0, 0.40, 0);
      torso.add(headGroup);

      // AUTHENTIC INDIAN TRICOLOR SCARF FOR POLITICIAN ARUN (MATCHING REFERENCE IMAGE)
      if (isTricolorScarf) {
        const saffronMat = new THREE.MeshStandardMaterial({ color: 0xff9933, roughness: 0.5 });
        const whiteScarfMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.5 });
        const greenScarfMat = new THREE.MeshStandardMaterial({ color: 0x138808, roughness: 0.5 });
        const goldFringeMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.8, roughness: 0.3 });

        // Scarf Loop behind neck
        const neckLoop = new THREE.Mesh(
          new THREE.TorusGeometry(0.24, 0.065, 8, 16, Math.PI),
          saffronMat
        );
        neckLoop.rotation.x = -Math.PI / 2;
        neckLoop.position.set(0, 0.42, -0.06);
        torso.add(neckLoop);

        // Left draping angavastram
        const leftGroup = new THREE.Group();
        const sL1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), saffronMat);
        sL1.position.x = -0.06;
        const sL2 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), whiteScarfMat);
        const sL3 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), greenScarfMat);
        sL3.position.x = 0.06;
        leftGroup.add(sL1, sL2, sL3);

        const tasselL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.04), goldFringeMat);
        tasselL.position.y = -0.47;
        leftGroup.add(tasselL);

        leftGroup.position.set(-0.20, -0.02, 0.21);
        torso.add(leftGroup);

        // Right draping angavastram
        const rightGroup = new THREE.Group();
        const sR1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), greenScarfMat);
        sR1.position.x = -0.06;
        const sR2 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), whiteScarfMat);
        const sR3 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.90, 0.03), saffronMat);
        sR3.position.x = 0.06;
        rightGroup.add(sR1, sR2, sR3);

        const tasselR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.04), goldFringeMat);
        tasselR.position.y = -0.47;
        rightGroup.add(tasselR);

        rightGroup.position.set(0.20, -0.02, 0.21);
        torso.add(rightGroup);

      } else if (hasSash) {
        const sashMat = new THREE.MeshStandardMaterial({ color: sashColor, roughness: 0.5 });
        const sash = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.95, 0.44), sashMat);
        sash.position.set(-0.22, 0.0, 0.0);
        torso.add(sash);
      }

      // Dupatta drape
      if (hasDupatta) {
        const dupMat = new THREE.MeshStandardMaterial({ color: dupattaColor, roughness: 0.6 });
        const dup = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.95, 0.44), dupMat);
        dup.position.set(-0.18, -0.02, 0.01);
        torso.add(dup);
      }

      // Saree Pallu drape
      if (isSaree) {
        const palluMat = new THREE.MeshStandardMaterial({ color: palluColor, roughness: 0.6 });
        const pallu = new THREE.Mesh(new THREE.BoxGeometry(0.30, 1.0, 0.44), palluMat);
        pallu.position.set(0.18, 0.0, 0.02);
        torso.add(pallu);

        const goldBorder = new THREE.Mesh(
          new THREE.BoxGeometry(0.05, 1.02, 0.45),
          new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.8, roughness: 0.3 })
        );
        goldBorder.position.set(0.31, 0.0, 0.02);
        torso.add(goldBorder);
      }

      // Shopkeeper Apron
      if (hasApron) {
        const apronMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.7 });
        const apron = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.75, 0.42), apronMat);
        apron.position.set(0, -0.1, 0.02);
        torso.add(apron);
      }

      // Student Backpack
      if (hasBackpack) {
        const packMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
        const pack = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.65, 0.28), packMat);
        pack.position.set(0, 0.05, -0.30);
        torso.add(pack);
      }

      // Police Duty Belt & Holster
      if (hasKhakiPolice) {
        const beltMat = new THREE.MeshStandardMaterial({ color: 0x3e2723, roughness: 0.4 });
        const belt = new THREE.Mesh(new THREE.BoxGeometry(0.74, 0.14, 0.42), beltMat);
        belt.position.set(0, -0.38, 0);
        torso.add(belt);

        const holster = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.26, 0.14), beltMat);
        holster.position.set(0.38, -0.45, 0);
        torso.add(holster);
      }

      // Arms & Hands Rigging
      function makeArm(isRight) {
        const armGroup = new THREE.Group();
        const upper = new THREE.Mesh(new THREE.CylinderGeometry(0.10, 0.09, 0.45, 10), shirtMat);
        upper.position.y = -0.22;
        armGroup.add(upper);

        const forearmGroup = new THREE.Group();
        // Kurta sleeve covers upper half of forearm
        const forearmCloth = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.085, 0.25, 10), shirtMat);
        forearmCloth.position.y = -0.125;
        forearmGroup.add(forearmCloth);

        const forearmSkin = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.075, 0.20, 10), skinMat);
        forearmSkin.position.y = -0.32;
        forearmGroup.add(forearmSkin);

        const hand = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), skinMat);
        hand.position.y = -0.44;
        forearmGroup.add(hand);

        // Wristwatch on left wrist for Arun
        if (!isRight && isTricolorScarf) {
          const watch = new THREE.Mesh(
            new THREE.CylinderGeometry(0.09, 0.09, 0.05, 12),
            new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.9, roughness: 0.2 })
          );
          watch.position.y = -0.38;
          forearmGroup.add(watch);
        }

        forearmGroup.position.y = -0.42;
        armGroup.add(forearmGroup);

        armGroup.position.set(isRight ? 0.46 : -0.46, 0.32, 0);
        torso.add(armGroup);
        return { armGroup, forearmGroup, hand };
      }

      const leftArm = makeArm(false);
      const rightArm = makeArm(true);

      // Pelvis & Legs Rigging
      function makeLeg(isRight) {
        const legGroup = new THREE.Group();
        const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.12, 0.52, 10), lowerMat);
        thigh.position.y = -0.26;
        thigh.castShadow = true;
        legGroup.add(thigh);

        const calfGroup = new THREE.Group();
        const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.50, 10), lowerMat);
        calf.position.y = -0.24;
        calfGroup.add(calf);

        // Leather Chappal / Shoe
        const foot = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.09, 0.30), shoeMat);
        foot.position.set(0, -0.48, 0.07);
        calfGroup.add(foot);

        calfGroup.position.y = -0.50;
        legGroup.add(calfGroup);

        legGroup.position.set(isRight ? 0.19 : -0.19, 0.90, 0);
        rig.add(legGroup);
        return { legGroup, calfGroup, foot };
      }

      const leftLeg = makeLeg(false);
      const rightLeg = makeLeg(true);

      // Handheld Props
      if (hasDSLR) {
        const camBody = new THREE.Mesh(
          new THREE.BoxGeometry(0.24, 0.18, 0.18),
          new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.4 })
        );
        camBody.position.set(0, -0.52, 0.12);
        const lens = new THREE.Mesh(
          new THREE.CylinderGeometry(0.08, 0.09, 0.22, 12),
          new THREE.MeshStandardMaterial({ color: 0x1f2937, metalness: 0.8 })
        );
        lens.rotation.x = Math.PI / 2;
        lens.position.set(0, 0, 0.16);
        camBody.add(lens);
        rightArm.forearmGroup.add(camBody);
      }

      if (hasCane) {
        const cane = new THREE.Mesh(
          new THREE.CylinderGeometry(0.02, 0.025, 1.0, 8),
          new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8 })
        );
        cane.position.set(0.1, -0.50, 0.1);
        rightArm.forearmGroup.add(cane);
      }

      if (hasPot) {
        const potMat = new THREE.MeshStandardMaterial({ color: potColor, roughness: 0.4 });
        const potBottom = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 12), potMat);
        potBottom.scale.set(1.0, 0.85, 1.0);
        potBottom.position.set(0.25, -0.38, 0.1);
        rightArm.forearmGroup.add(potBottom);
      }

      return {
        root: rig,
        torso,
        headGroup,
        leftArm,
        rightArm,
        leftLeg,
        rightLeg
      };
    }

    /* ==========================================================================
       10. POPULATE THE 13 CHARACTERS ACROSS CHENNAI WARD 12 (MATCHING REFERENCE IMAGE)
       ========================================================================== */

    // 1. ARUN (Main Playable Politician)
    // White Khadi Shirt, Tailored White Trousers, Draped Indian Tricolor Scarf, Gold Watch
    const arunRig = createHumanoidRig({
      shirtColor: 0xffffff,
      lowerColor: 0xf8fafc,
      skinColor: 0xa16207,
      hairColor: 0x09090b,
      hasMustache: true,
      hasBeard: true,
      isTricolorScarf: true
    });
    const playerGroup = arunRig.root;
    playerGroup.position.set(0, 0, 10);
    scene.add(playerGroup);

    // 2. KARTHIK (Campaign Worker Male at Z = 2, X = 4.5)
    // White polo shirt, blue jeans, cap
    const karthikRig = createHumanoidRig({
      shirtColor: 0xffffff,
      lowerColor: 0x1d4ed8,
      skinColor: 0x854d0e,
      hasCap: true,
      capColor: 0x1e3a8a
    });
    karthikRig.root.position.set(4.5, 0, 2);
    karthikRig.root.rotation.y = -Math.PI / 2;
    scene.add(karthikRig.root);

    // 3. DEEPA (Female Campaign Worker at Z = 6, X = -4.5)
    // White salwar suit, vibrant blue dupatta
    const deepaRig = createHumanoidRig({
      shirtColor: 0xffffff,
      lowerColor: 0xffffff,
      skinColor: 0x9a3412,
      hasMustache: false,
      hasDupatta: true,
      dupattaColor: 0x0284c7
    });
    deepaRig.root.position.set(-4.5, 0, 6);
    deepaRig.root.rotation.y = Math.PI / 2;
    scene.add(deepaRig.root);

    // 4. INSPECTOR PANDIAN (Police Officer at Z = -48, X = -9.5)
    // Khaki uniform with peaked cap, holster belt, boots
    const policeRig = createHumanoidRig({
      shirtColor: 0xb45309,
      lowerColor: 0x92400e,
      skinColor: 0x854d0e,
      hasCap: true,
      capColor: 0x78350f,
      hasKhakiPolice: true
    });
    policeRig.root.position.set(-9.5, 0, -48);
    policeRig.root.rotation.y = Math.PI / 3;
    scene.add(policeRig.root);

    // 5. VIKRAM (Press Journalist at Z = -25, X = -2.5)
    // Blue shirt, chinos, telephoto DSLR camera, microphone
    const pressRig = createHumanoidRig({
      shirtColor: 0x3b82f6,
      lowerColor: 0xd97706,
      skinColor: 0x9a3412,
      hasDSLR: true
    });
    pressRig.root.position.set(-2.5, 0, -25);
    pressRig.root.rotation.y = -Math.PI / 4;
    scene.add(pressRig.root);

    // 6. MURUGAN (Resident Male at Z = 14, X = -14.0)
    // Checkered shirt, grey trousers
    const muruganRig = createHumanoidRig({
      shirtColor: 0x0284c7,
      lowerColor: 0x475569,
      skinColor: 0x78350f
    });
    muruganRig.root.position.set(-14.0, 0, 14);
    muruganRig.root.rotation.y = Math.PI / 2;
    scene.add(muruganRig.root);

    // 7. LAKSHMI (Resident Female at Z = 5, X = -14.2)
    // Royal peacock-blue silk saree with gold border & jasmine flowers
    const lakshmiRig = createHumanoidRig({
      shirtColor: 0x0369a1,
      lowerColor: 0x0369a1,
      skinColor: 0x9a3412,
      hasMustache: false,
      isSaree: true,
      palluColor: 0x0369a1,
      hasFlowers: true
    });
    lakshmiRig.root.position.set(-14.2, 0, 5);
    lakshmiRig.root.rotation.y = Math.PI / 2;
    scene.add(lakshmiRig.root);

    // 8. PERIYAVAR SUNDARAM (Elderly Person at Z = -3, X = -14.5)
    // White cotton shirt, kasavu dhoti, white beard, wooden cane
    const elderRig = createHumanoidRig({
      shirtColor: 0xffffff,
      lowerColor: 0xfef08a,
      skinColor: 0xa16207,
      hairColor: 0xe2e8f0,
      hasBeard: true,
      hasCane: true
    });
    elderRig.root.position.set(-14.5, 0, -3);
    elderRig.root.rotation.y = Math.PI / 2;
    scene.add(elderRig.root);

    // 9. ANAND (Student at Z = -55, X = 14.5)
    // School uniform, shoulder backpack
    const studentRig = createHumanoidRig({
      shirtColor: 0xffffff,
      lowerColor: 0x1e3a8a,
      skinColor: 0x854d0e,
      hasMustache: false,
      hasBackpack: true
    });
    studentRig.root.position.set(14.5, 0, -55);
    studentRig.root.rotation.y = -Math.PI / 2;
    scene.add(studentRig.root);

    // 10. BABU (Market Shopkeeper at Z = -12, X = -14.5)
    // Printed shirt, merchant apron
    const shopkeeperRig = createHumanoidRig({
      shirtColor: 0xd97706,
      lowerColor: 0x64748b,
      skinColor: 0x78350f,
      hasApron: true
    });
    shopkeeperRig.root.position.set(-14.5, 0, -12);
    shopkeeperRig.root.rotation.y = Math.PI / 2;
    scene.add(shopkeeperRig.root);

    // 11. KARUPPASAMY (Political Opponent at Z = -5, X = 7.5)
    // Rich cream/crimson shirt, party stole, dark sunglasses
    const karuppasamyRig = createHumanoidRig({
      shirtColor: 0xb91c1c,
      lowerColor: 0xfde68a,
      skinColor: 0x854d0e,
      hasSash: true,
      sashColor: 0x0f172a,
      hasGoggles: true
    });
    const karuppasamy = karuppasamyRig.root;
    karuppasamy.position.set(7.5, 0, -5);
    karuppasamy.rotation.y = -Math.PI / 2;
    scene.add(karuppasamy);

    // 12. TANKER MAFIA DRIVER (Task 2 Target at Z = -28, X = -3.8)
    const driverRig = createHumanoidRig({
      shirtColor: 0x2563eb,
      lowerColor: 0x78716c,
      skinColor: 0x713f12,
      hasCap: true,
      capColor: 0x1e3a8a
    });
    const tankerDriver = driverRig.root;
    tankerDriver.position.set(-3.8, 0, -28);
    tankerDriver.rotation.y = Math.PI / 2;
    scene.add(tankerDriver);

    // 13. MEENAKSHI & DIVERSE CITIZENS / RALLY SUPPORTERS CROWD
    const crowdList = [];
    const sareeColors = [0xdb2777, 0x7c3aed, 0x059669, 0xd97706, 0xdc2626, 0x0284c7];
    const lungiColors = [0x3b82f6, 0x10b981, 0xf97316, 0x64748b, 0xffffff];

    function spawnCrowdMember(x, z, rotY, isRallyCheerer = false, isWaterQueue = false) {
      const isWoman = Math.random() > 0.52;
      const topCol = isWoman ? sareeColors[Math.floor(Math.random() * sareeColors.length)] : (Math.random() > 0.5 ? 0xffffff : 0x3b82f6);
      const botCol = isWoman ? topCol : lungiColors[Math.floor(Math.random() * lungiColors.length)];
      const skinCol = 0x854d0e + Math.floor(Math.random() * 0x1a1205);

      const rig = createHumanoidRig({
        shirtColor: topCol,
        lowerColor: botCol,
        skinColor: skinCol,
        hasSash: isRallyCheerer && Math.random() > 0.45,
        isSaree: isWoman,
        palluColor: topCol,
        hasPot: isWaterQueue,
        potColor: isWoman ? 0xef4444 : 0x0284c7
      });
      rig.root.position.set(x, 0, z);
      rig.root.rotation.y = rotY;

      // Add fluttering political flag for rally cheerers
      if (isRallyCheerer && Math.random() > 0.35) {
        const flagPole = new THREE.Mesh(
          new THREE.CylinderGeometry(0.02, 0.02, 1.8, 8),
          new THREE.MeshStandardMaterial({ color: 0x78350f })
        );
        flagPole.position.set(0.1, 0.7, 0.2);
        const flagCloth = new THREE.Mesh(
          new THREE.PlaneGeometry(0.65, 0.4),
          new THREE.MeshStandardMaterial({
            color: Math.random() > 0.5 ? 0xb91c1c : 0xf59e0b,
            side: THREE.DoubleSide
          })
        );
        flagCloth.position.set(0.35, 1.3, 0.2);
        rig.rightArm.forearmGroup.add(flagPole);
        rig.rightArm.forearmGroup.add(flagCloth);
      }

      scene.add(rig.root);
      crowdList.push({
        rig,
        isRallyCheerer,
        isWaterQueue,
        animOffset: Math.random() * 10,
        basePos: new THREE.Vector3(x, 0, z),
        reactingEmote: null,
        reactionTimer: 0
      });
    }

    // Spawn 50 rally supporters around mega stage (Z = -68 to -84)
    for (let i = 0; i < 50; i++) {
      const angle = (Math.random() - 0.5) * Math.PI * 0.85;
      const dist = 5 + Math.random() * 14;
      const x = Math.sin(angle) * dist;
      const z = -75 + Math.cos(angle) * dist;
      const rotY = Math.atan2(-x, -75 - z);
      spawnCrowdMember(x, z, rotY, true, false);
    }

    // Spawn 7 distressed residents in the Water Queue (Z = -22 to -26, X = -14.5)
    for (let i = 0; i < 7; i++) {
      spawnCrowdMember(-14.2 + (Math.random() - 0.5) * 1.0, -20 - i * 1.2, Math.PI / 2, false, true);
    }

    // Spawn 12 pedestrians along sidewalks
    [-65, -45, -12, 12, 22].forEach(zPos => {
      spawnCrowdMember(-14.5 + (Math.random() - 0.5) * 1.5, zPos, Math.random() * Math.PI * 2);
      spawnCrowdMember(14.5 + (Math.random() - 0.5) * 1.5, zPos, Math.random() * Math.PI * 2);
    });

    /* ==========================================================================
       11. CONTROLS, INTERACTION & MISSION PROGRESSION
       ========================================================================== */
    const keys = {};
    window.addEventListener('keydown', e => {
      keys[e.key.toLowerCase()] = true;
      if (e.key.toLowerCase() === 'e') handleInteraction();
      if (e.key.toLowerCase() === 'f') toggleCarDrive();
      if (e.key.toLowerCase() === 'h') playCarHorn();
      if (e.key.toLowerCase() === 't' || e.key.toLowerCase() === 'b') openEmoteMenu();
      if (e.key === 'Escape') togglePauseMenu();
    });
    window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

    // Virtual Joystick Touch Controls
    let joystickVec = { x: 0, y: 0 };
    const joyZone = document.getElementById('joystick-zone');
    const joyKnob = document.getElementById('joystick-knob');
    let joyActive = false;

    joyZone.addEventListener('pointerdown', e => {
      joyActive = true;
      joyZone.setPointerCapture(e.pointerId);
      updateJoyKnob(e);
    });

    joyZone.addEventListener('pointermove', e => {
      if (joyActive) updateJoyKnob(e);
    });

    joyZone.addEventListener('pointerup', () => {
      joyActive = false;
      joystickVec = { x: 0, y: 0 };
      joyKnob.style.transform = 'translate(-50%, -50%)';
    });

    function updateJoyKnob(e) {
      const rect = joyZone.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      let dx = e.clientX - cx;
      let dy = e.clientY - cy;
      const maxR = rect.width / 2 - 10;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > maxR) {
        dx = (dx / dist) * maxR;
        dy = (dy / dist) * maxR;
      }
      joyKnob.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
      joystickVec = { x: dx / maxR, y: -dy / maxR };
    }

    function togglePauseMenu() {
      const modal = document.getElementById('pause-modal');
      if (modal.style.display === 'flex') closePauseMenu();
      else openPauseMenu();
    }

    function toggleCarDrive() {
      if (isDriving) exitCar();
      else enterCar();
    }

    function enterCar() {
      const d = playerGroup.position.distanceTo(carGroup.position);
      if (d > 7.0 && currentTask !== 3) {
        document.getElementById('sys-event-msg').innerText = "Approach the Ambassador car first to enter.";
        return;
      }
      isDriving = true;
      playBeep(260, 'sawtooth', 0.25);
      startEngineSound();
      playerGroup.visible = false;
      document.getElementById('driving-hud').style.display = 'flex';
      document.getElementById('action-prompt').style.display = 'none';
      document.getElementById('sys-event-msg').innerText = "Driving Ambassador VIP Car. Head North to the Mega Rally Stage (Z = -75).";
    }

    function exitCar() {
      isDriving = false;
      stopEngineSound();
      playerGroup.visible = true;
      playerGroup.position.set(carGroup.position.x + 2.2, 0, carGroup.position.z);
      document.getElementById('driving-hud').style.display = 'none';
      playBeep(320, 'sine', 0.15);

      if (currentTask === 3 && carGroup.position.z < -60) {
        advanceToTask(4, 5, 0);
      }
    }

    // Context Proximity Checking
    function checkProximity() {
      const prompt = document.getElementById('action-prompt');

      if (isDriving) {
        prompt.style.display = 'none';
        return;
      }

      if (currentTask === 1) {
        const d = playerGroup.position.distanceTo(karuppasamy.position);
        if (d < 5.5 && document.getElementById('dialogue-modal').style.display !== 'flex') {
          prompt.innerText = "Press [E] or Tap: Speak with Ward Member Karuppasamy";
          prompt.style.display = 'block';
          return;
        }
      } else if (currentTask === 2) {
        const d = playerGroup.position.distanceTo(new THREE.Vector3(-6, 0, -28));
        if (d < 6.5 && document.getElementById('dialogue-modal').style.display !== 'flex') {
          prompt.innerText = "Press [E] or Tap: Intercept Illegal Water Tanker";
          prompt.style.display = 'block';
          return;
        }
      } else if (currentTask === 3) {
        const d = playerGroup.position.distanceTo(carGroup.position);
        if (d < 5.5) {
          prompt.innerText = "Press [E] / [F] or Tap: Enter White Ambassador Car";
          prompt.style.display = 'block';
          return;
        }
      } else if (currentTask === 4) {
        const d = playerGroup.position.distanceTo(new THREE.Vector3(0, 0, -75));
        if (d < 7.5 && document.getElementById('dialogue-modal').style.display !== 'flex') {
          prompt.innerText = "Press [E] or Tap: Address Mega Rally & Win Election!";
          prompt.style.display = 'block';
          return;
        }
      }

      prompt.style.display = 'none';
    }

    function handleInteraction() {
      if (currentTask === 1) {
        openDialogue(
          "Ward Member Karuppasamy",
          "Arun! Why are you inciting the residents against the administration? The water shortage is due to a main distribution breakdown. Take this ₹50,000 community donation and pacify the youth.",
          [
            { text: "Refuse the bribe! 'We have evidence you diverted municipal borewells to private tankers!' (+10% Public Trust)", act: () => advanceToTask(2, 10, 0) },
            { text: "Accept donation for ward relief. (+₹50,000, -8% Integrity)", act: () => advanceToTask(2, -8, 50000) }
          ]
        );
      } else if (currentTask === 2) {
        openDialogue(
          "Tanker Mafia Driver",
          "Listen brother, put down your camera! Counselor Karuppasamy authorized these 10 tankers for luxury commercial complexes. Do not get involved.",
          [
            { text: "Expose the illegal distribution valves live to press journalists! (+12% Public Trust)", act: () => advanceToTask(3, 12, 0) },
            { text: "Order the tanker to redirect water to Ward 12 families immediately! (+15% Public Trust)", act: () => advanceToTask(3, 15, 0) }
          ]
        );
      } else if (currentTask === 3) {
        toggleCarDrive();
      } else if (currentTask === 4) {
        openDialogue(
          "Mega Election Rally - Stage Coordinator",
          "Thousands of Ward 12 residents have assembled before the stage! Are you prepared to deliver the keynote address and announce your candidacy for the Bye-Election?",
          [
            { text: "Ascend the podium, deliver the keynote speech, and pledge clean drinking water for all!", act: () => completeLevel1() }
          ]
        );
      }
    }

    function handleCurrentTask() {
      if (currentTask === 1) {
        playerGroup.position.set(6, 0, -3.5);
        handleInteraction();
      } else if (currentTask === 2) {
        playerGroup.position.set(-4, 0, -26);
        handleInteraction();
      } else if (currentTask === 3) {
        playerGroup.position.set(4, 0, -42);
        toggleCarDrive();
      } else if (currentTask === 4) {
        playerGroup.position.set(0, 0, -71);
        handleInteraction();
      }
    }

    function openDialogue(speaker, text, options) {
      playBeep(580, 'sine', 0.15);
      const modal = document.getElementById('dialogue-modal');
      document.getElementById('dialogue-speaker').innerHTML = `<span>👤</span><span>${speaker}</span>`;
      document.getElementById('dialogue-text').innerText = text;

      const optsContainer = document.getElementById('dialogue-options');
      optsContainer.innerHTML = '';
      options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'dialogue-opt';
        btn.innerText = opt.text;
        btn.onclick = () => {
          modal.style.display = 'none';
          playBeep(720, 'triangle', 0.12);
          opt.act();
        };
        optsContainer.appendChild(btn);
      });
      modal.style.display = 'flex';
    }

    function advanceToTask(nextTask, trustDelta = 0, cashDelta = 0) {
      currentTask = nextTask;
      trust = Math.max(0, Math.min(100, trust + trustDelta));
      cash += cashDelta;
      updateTaskHUD();
      playBeep(880, 'sine', 0.25);
      document.getElementById('sys-event-msg').innerText = `Objective Complete! New Goal: ${taskTitles[currentTask]}`;
    }

    function completeLevel1() {
      playBeep(980, 'triangle', 0.35);
      triggerEmote('celebrate');
      setTimeout(() => {
        document.getElementById('level-complete-modal').style.display = 'flex';
      }, 1500);
    }

    function resetLevel1() {
      currentTask = 1;
      isDriving = false;
      carSpeed = 0;
      trust = 75;
      cash = 245000;
      stopEngineSound();
      playerGroup.visible = true;
      playerGroup.position.set(0, 0, 10);
      carGroup.position.set(4, 0, -45);
      carGroup.rotation.y = 0;
      document.getElementById('level-complete-modal').style.display = 'none';
      document.getElementById('driving-hud').style.display = 'none';
      updateTaskHUD();
      start3DWorld();
    }

    /* ==========================================================================
       12. GRAPHICS PRESETS & HARDWARE TELEMETRY (Intel Core 5 Friendly)
       ========================================================================== */
    function applyGraphicsPreset(preset) {
      graphicsPreset = preset;
      document.querySelectorAll('.perf-chip-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(`preset-${preset.substring(0,3)}`);
      if (activeBtn) activeBtn.classList.add('active');

      if (preset === 'low') {
        renderer.setPixelRatio(0.85);
        renderer.shadowMap.enabled = false;
        dirLight.castShadow = false;
        crowdList.forEach((c, idx) => c.rig.root.visible = (idx % 2 === 0));
        document.getElementById('hud-fps-pill').innerText = '60+ FPS [LOW]';
      } else if (preset === 'medium') {
        renderer.setPixelRatio(1.0);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.BasicShadowMap;
        dirLight.castShadow = true;
        crowdList.forEach(c => c.rig.root.visible = true);
        document.getElementById('hud-fps-pill').innerText = '60 FPS [MED]';
      } else if (preset === 'high') {
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        dirLight.castShadow = true;
        crowdList.forEach(c => c.rig.root.visible = true);
        document.getElementById('hud-fps-pill').innerText = '60 FPS [HIGH]';
      }
      playBeep(450, 'sine', 0.08);
    }

    function cycleGraphicsPreset() {
      if (graphicsPreset === 'low') applyGraphicsPreset('medium');
      else if (graphicsPreset === 'medium') applyGraphicsPreset('high');
      else applyGraphicsPreset('low');
    }

    /* ==========================================================================
       13. REAL-TIME 2D CANVAS MINIMAP RADAR
       ========================================================================== */
    const minimapCanvas = document.getElementById('minimap-canvas');
    const mmCtx = minimapCanvas.getContext('2d');

    function renderMinimap() {
      mmCtx.clearRect(0, 0, 88, 88);

      // Radar background with circular grid rings
      mmCtx.fillStyle = 'rgba(7, 13, 24, 0.95)';
      mmCtx.fillRect(0, 0, 88, 88);

      mmCtx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
      mmCtx.lineWidth = 1;
      mmCtx.beginPath(); mmCtx.arc(44, 44, 20, 0, Math.PI * 2); mmCtx.stroke();
      mmCtx.beginPath(); mmCtx.arc(44, 44, 38, 0, Math.PI * 2); mmCtx.stroke();

      // Road boundary
      mmCtx.fillStyle = '#1e293b';
      mmCtx.fillRect(36, 0, 16, 88);

      // Player / Active Actor position
      const pPos = isDriving ? carGroup.position : playerGroup.position;
      const scale = 0.5;

      function mapCoords(x, z) {
        const mx = 44 + (x - pPos.x) * scale;
        const my = 44 + (z - pPos.z) * scale;
        return [mx, my];
      }

      // Objective Markers
      // Karuppasamy (Task 1)
      const [kX, kZ] = mapCoords(7.5, -5);
      mmCtx.fillStyle = currentTask === 1 ? '#f59e0b' : '#64748b';
      mmCtx.beginPath();
      mmCtx.arc(kX, kZ, 3.5, 0, Math.PI * 2);
      mmCtx.fill();

      // Tanker (Task 2)
      const [tX, tZ] = mapCoords(-6, -28);
      mmCtx.fillStyle = currentTask === 2 ? '#38bdf8' : '#0369a1';
      mmCtx.beginPath();
      mmCtx.arc(tX, tZ, 3.5, 0, Math.PI * 2);
      mmCtx.fill();

      // Ambassador Car (Task 3)
      const [cX, cZ] = mapCoords(carGroup.position.x, carGroup.position.z);
      mmCtx.fillStyle = currentTask === 3 ? '#ef4444' : '#e2e8f0';
      mmCtx.fillRect(cX - 2, cZ - 3, 4, 6);

      // Mega Rally Stage (Task 4)
      const [rX, rZ] = mapCoords(0, -75);
      mmCtx.fillStyle = currentTask === 4 ? '#22c55e' : '#b91c1c';
      mmCtx.fillRect(rX - 4, rZ - 2.5, 8, 5);

      // Center Player Icon
      mmCtx.fillStyle = '#f8fafc';
      mmCtx.beginPath();
      mmCtx.arc(44, 44, 3.5, 0, Math.PI * 2);
      mmCtx.fill();
      mmCtx.strokeStyle = '#38bdf8';
      mmCtx.lineWidth = 2;
      mmCtx.stroke();
    }

    /* ==========================================================================
       14. ANIMATION LOOP & CHARACTER EMOTES KINEMATICS (18 EMOTES)
       ========================================================================== */
    const clock = new THREE.Clock();
    let walkCycleTime = 0;

    function animate() {
      requestAnimationFrame(animate);
      const dt = clock.getDelta();
      const now = performance.now();

      // 1. VIP AMBASSADOR DRIVING MODE
      if (isDriving) {
        let throttle = 0;
        let steer = 0;

        if (keys['w'] || keys['arrowup']) throttle += 1;
        if (keys['s'] || keys['arrowdown']) throttle -= 0.6;
        if (keys['a'] || keys['arrowleft']) steer += 1;
        if (keys['d'] || keys['arrowright']) steer -= 1;

        if (joyActive) {
          throttle += joystickVec.y;
          steer -= joystickVec.x;
        }

        const maxForward = 24.0;
        const maxReverse = -8.0;
        carSpeed = THREE.MathUtils.lerp(carSpeed, throttle > 0 ? throttle * maxForward : throttle * Math.abs(maxReverse), dt * 2.5);

        if (Math.abs(carSpeed) > 0.1) {
          const forwardVec = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), carGroup.rotation.y);
          carGroup.position.addScaledVector(forwardVec, carSpeed * dt);
          carGroup.rotation.y += steer * dt * 1.4 * Math.sign(carSpeed);

          carAllWheels.forEach(w => w.children[0].rotation.x += carSpeed * dt * 3.0);
          carFrontWheels.forEach(w => w.rotation.y = steer * 0.45);
          updateEngineSound(Math.abs(carSpeed) / maxForward);
        } else {
          updateEngineSound(0);
        }

        if (carBeaconLight) {
          carBeaconLight.intensity = 0.8 + Math.sin(now * 0.015) * 0.8;
        }

        document.getElementById('speed-gauge').innerText = `🚗 ${Math.abs(Math.round(carSpeed * 2.5))} KM/H`;

        if (currentTask === 3 && carGroup.position.z < -60) {
          advanceToTask(4, 5, 0);
        }

        // Camera Follows Car Smoothly
        const camDist = 9.0;
        const camHeight = 4.2;
        const targetCamPos = new THREE.Vector3(
          carGroup.position.x + Math.sin(carGroup.rotation.y) * camDist,
          carGroup.position.y + camHeight,
          carGroup.position.z + Math.cos(carGroup.rotation.y) * camDist
        );
        camera.position.lerp(targetCamPos, 0.12);
        camera.lookAt(carGroup.position.x, carGroup.position.y + 1.2, carGroup.position.z);

      } else {
        // 2. THIRD-PERSON CHARACTER EXPLORATION MODE (ARUN)
        let moveX = 0;
        let moveZ = 0;

        if (keys['w'] || keys['arrowup']) moveZ -= 1;
        if (keys['s'] || keys['arrowdown']) moveZ += 1;
        if (keys['a'] || keys['arrowleft']) moveX -= 1;
        if (keys['d'] || keys['arrowright']) moveX += 1;

        if (joyActive) {
          moveX += joystickVec.x;
          moveZ -= joystickVec.y;
        }

        const isMoving = Math.abs(moveX) > 0.05 || Math.abs(moveZ) > 0.05;
        const isSprinting = keys['shift'];
        const moveSpeed = isSprinting ? 7.5 : 4.5;

        if (isMoving) {
          const moveDir = new THREE.Vector3(moveX, 0, moveZ).normalize();
          moveDir.applyAxisAngle(new THREE.Vector3(0, 1, 0), camYaw);

          playerGroup.position.addScaledVector(moveDir, moveSpeed * dt);
          const targetRot = Math.atan2(moveDir.x, moveDir.z);
          playerGroup.rotation.y = THREE.MathUtils.lerp(playerGroup.rotation.y, targetRot, 0.2);

          walkCycleTime += dt * (isSprinting ? 14 : 9);
          const swing = Math.sin(walkCycleTime) * (isSprinting ? 0.75 : 0.5);

          arunRig.leftLeg.legGroup.rotation.x = swing;
          arunRig.rightLeg.legGroup.rotation.x = -swing;
          arunRig.leftArm.armGroup.rotation.x = -swing * 0.8;
          arunRig.rightArm.armGroup.rotation.x = swing * 0.8;
          arunRig.torso.position.y = 1.35 + Math.abs(Math.cos(walkCycleTime)) * 0.06;
          arunRig.torso.rotation.x = 0.05;
          arunRig.headGroup.rotation.x = 0;

          if (activeEmote) {
            activeEmote = null;
            document.getElementById('emote-banner').style.display = 'none';
          }
        } else {
          // Idle breathing
          const breath = Math.sin(now * 0.003) * 0.02;
          arunRig.leftLeg.legGroup.rotation.x = THREE.MathUtils.lerp(arunRig.leftLeg.legGroup.rotation.x, 0, 0.1);
          arunRig.rightLeg.legGroup.rotation.x = THREE.MathUtils.lerp(arunRig.rightLeg.legGroup.rotation.x, 0, 0.1);

          if (activeEmote) {
            applyEmotePose(arunRig, activeEmote, now);
            emoteTimer -= dt;
            if (emoteTimer <= 0) {
              activeEmote = null;
              document.getElementById('emote-banner').style.display = 'none';
            }
          } else {
            // Normal Idle Stance
            arunRig.torso.position.y = 1.35 + breath;
            arunRig.torso.rotation.x = 0;
            arunRig.headGroup.rotation.x = 0;
            arunRig.leftArm.armGroup.rotation.set(0, 0, 0.05);
            arunRig.rightArm.armGroup.rotation.set(0, 0, -0.05);
            arunRig.leftArm.forearmGroup.rotation.set(0, 0, 0);
            arunRig.rightArm.forearmGroup.rotation.set(0, 0, 0);
          }
        }

        // Camera Follows Arun Smoothly
        const camDist = 6.2;
        const camHeight = 2.8;
        const cx = playerGroup.position.x + Math.sin(camYaw) * (camDist * Math.cos(camPitch));
        const cy = playerGroup.position.y + camHeight + Math.sin(camPitch) * camDist;
        const cz = playerGroup.position.z + Math.cos(camYaw) * (camDist * Math.cos(camPitch));

        camera.position.lerp(new THREE.Vector3(cx, cy, cz), 0.18);
        camera.lookAt(playerGroup.position.x, playerGroup.position.y + 1.45, playerGroup.position.z);
      }

      // 3. ANIMATE CROWD & SUPPORTERS (Cheering, flag waving, water waiting, reactive emotes)
      crowdList.forEach(c => {
        if (!c.rig.root.visible) return;

        if (c.reactionTimer > 0) {
          c.reactionTimer -= dt;
          applyEmotePose(c.rig, c.reactingEmote || 'namaste', now);
        } else if (c.isRallyCheerer) {
          // Rally Supporters Enthusiastic Cheering
          const cheerPhase = Math.sin(now * 0.007 + c.animOffset);
          c.rig.rightArm.armGroup.rotation.set(-2.4 + cheerPhase * 0.4, 0, -0.3);
          c.rig.leftArm.armGroup.rotation.set(-2.0 - cheerPhase * 0.3, 0, 0.3);
          c.rig.torso.position.y = 1.35 + Math.abs(cheerPhase) * 0.08;
          c.rig.headGroup.rotation.x = -0.2;
        } else if (c.isWaterQueue) {
          // Distressed Residents Waiting for Water (Anxious stance)
          const waitSway = Math.sin(now * 0.002 + c.animOffset) * 0.05;
          c.rig.torso.rotation.x = 0.08 + waitSway;
          c.rig.headGroup.rotation.x = 0.12;
          c.rig.leftArm.armGroup.rotation.set(0.1, 0, 0.1);
        }
      });

      // 4. ANIMATE KARUPPASAMY NPC (Turning to look at Arun)
      const distToKaruppasamy = playerGroup.position.distanceTo(karuppasamy.position);
      if (distToKaruppasamy < 12.0) {
        const lookAngle = Math.atan2(playerGroup.position.x - karuppasamy.position.x, playerGroup.position.z - karuppasamy.position.z);
        karuppasamy.rotation.y = THREE.MathUtils.lerp(karuppasamy.rotation.y, lookAngle, 0.05);
      }

      checkProximity();
      renderMinimap();
      renderer.render(scene, camera);
    }

    // PROCEDURAL EMOTE KINEMATICS SYSTEM (FULL 18 EMOTES MATCHING REFERENCE IMAGE)
    function applyEmotePose(rig, emoteId, now) {
      const p = Math.sin(now * 0.008);

      switch (emoteId) {
        case 'smile':
          // Open cheerful greeting, gentle head tilt
          rig.leftArm.armGroup.rotation.set(-0.6, 0, 0.5);
          rig.rightArm.armGroup.rotation.set(-0.6, 0, -0.5);
          rig.torso.position.y = 1.35 + Math.abs(p) * 0.03;
          rig.headGroup.rotation.x = -0.08;
          break;

        case 'confident':
          // Hands on hips, chest puffed
          rig.leftArm.armGroup.rotation.set(-0.3, 0, 0.7);
          rig.rightArm.armGroup.rotation.set(-0.3, 0, -0.7);
          rig.leftArm.forearmGroup.rotation.set(-1.4, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-1.4, 0, 0);
          rig.torso.rotation.x = -0.08;
          rig.headGroup.rotation.x = -0.12;
          break;

        case 'wave':
          // Right arm raised and waving
          rig.rightArm.armGroup.rotation.set(-2.2, 0, -0.3);
          rig.rightArm.forearmGroup.rotation.set(0, 0, p * 0.45);
          rig.leftArm.armGroup.rotation.set(0, 0, 0);
          rig.torso.rotation.x = 0;
          rig.headGroup.rotation.x = -0.05;
          break;

        case 'namaste':
          // Hands joined at chest, slight bow (Vanakkam)
          rig.leftArm.armGroup.rotation.set(-1.1, 0, 0.65);
          rig.rightArm.armGroup.rotation.set(-1.1, 0, -0.65);
          rig.leftArm.forearmGroup.rotation.set(-0.9, 0.4, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.9, -0.4, 0);
          rig.torso.rotation.x = 0.18 + p * 0.03;
          rig.headGroup.rotation.x = 0.15;
          break;

        case 'thumbsup':
          // Right arm forward thumbs up
          rig.rightArm.armGroup.rotation.set(-1.4, 0, -0.2);
          rig.rightArm.forearmGroup.rotation.set(-0.7, 0, 0);
          rig.leftArm.armGroup.rotation.set(0, 0, 0);
          rig.headGroup.rotation.x = p * 0.05;
          break;

        case 'point':
          // Right arm firmly pointing forward
          rig.rightArm.armGroup.rotation.set(-1.6, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.1, 0, 0);
          rig.leftArm.armGroup.rotation.set(-0.2, 0, 0.2);
          rig.torso.rotation.x = 0.05;
          break;

        case 'speech':
          // Expressive bilateral orator gestures
          rig.leftArm.armGroup.rotation.set(-1.3 + p * 0.25, 0, 0.45);
          rig.rightArm.armGroup.rotation.set(-1.3 - p * 0.25, 0, -0.45);
          rig.leftArm.forearmGroup.rotation.set(-0.6, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.6, 0, 0);
          rig.torso.rotation.x = 0.06;
          rig.headGroup.rotation.x = p * 0.08;
          break;

        case 'listen':
          // Hands raised gently calming audience
          rig.leftArm.armGroup.rotation.set(-1.2, 0, 0.3);
          rig.rightArm.armGroup.rotation.set(-1.2, 0, -0.3);
          rig.leftArm.forearmGroup.rotation.set(-0.3 + p * 0.1, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.3 + p * 0.1, 0, 0);
          rig.torso.rotation.x = 0;
          break;

        case 'angry':
          // Clenched fists, aggressive posture
          rig.leftArm.armGroup.rotation.set(-0.5, 0, 0.3);
          rig.rightArm.armGroup.rotation.set(-0.5, 0, -0.3);
          rig.leftArm.forearmGroup.rotation.set(-1.5, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-1.5, 0, 0);
          rig.torso.rotation.x = 0.15;
          rig.headGroup.rotation.x = 0.12;
          break;

        case 'sad':
          // Slumped shoulders, head down
          rig.leftArm.armGroup.rotation.set(0.1, 0, 0.1);
          rig.rightArm.armGroup.rotation.set(0.1, 0, -0.1);
          rig.torso.rotation.x = 0.22;
          rig.headGroup.rotation.x = 0.35;
          break;

        case 'worried':
          // Hand to temple, troubled stance
          rig.rightArm.armGroup.rotation.set(-1.8, 0, -0.5);
          rig.rightArm.forearmGroup.rotation.set(-1.4, 0, 0);
          rig.leftArm.armGroup.rotation.set(-0.2, 0, 0.2);
          rig.torso.rotation.x = 0.12;
          rig.headGroup.rotation.x = 0.2;
          break;

        case 'thinking':
          // Hand on chin, elbow supported
          rig.rightArm.armGroup.rotation.set(-1.6, 0, -0.3);
          rig.rightArm.forearmGroup.rotation.set(-1.3, 0, 0);
          rig.leftArm.armGroup.rotation.set(-0.8, 0, 0.5);
          rig.leftArm.forearmGroup.rotation.set(-0.9, 0, 0);
          rig.torso.rotation.x = 0.05;
          rig.headGroup.rotation.x = -0.06;
          break;

        case 'handshake':
          // Right arm extended forward
          rig.rightArm.armGroup.rotation.set(-1.2, 0, -0.1);
          rig.rightArm.forearmGroup.rotation.set(-0.4, 0, 0);
          rig.leftArm.armGroup.rotation.set(0, 0, 0);
          rig.torso.rotation.x = 0.08;
          break;

        case 'celebrate':
          // Both arms high in the air victory celebration
          rig.leftArm.armGroup.rotation.set(-2.6 + p * 0.2, 0, 0.4);
          rig.rightArm.armGroup.rotation.set(-2.6 - p * 0.2, 0, -0.4);
          rig.torso.position.y = 1.35 + Math.abs(p) * 0.08;
          rig.headGroup.rotation.x = -0.25;
          break;

        case 'defeat':
          // Hands covering face in regret
          rig.leftArm.armGroup.rotation.set(-1.8, 0, 0.4);
          rig.rightArm.armGroup.rotation.set(-1.8, 0, -0.4);
          rig.leftArm.forearmGroup.rotation.set(-1.6, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-1.6, 0, 0);
          rig.torso.rotation.x = 0.25;
          rig.headGroup.rotation.x = 0.35;
          break;

        case 'apologize':
          // Clasped hands, deep bowing apology
          rig.leftArm.armGroup.rotation.set(-1.1, 0, 0.55);
          rig.rightArm.armGroup.rotation.set(-1.1, 0, -0.55);
          rig.leftArm.forearmGroup.rotation.set(-0.8, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.8, 0, 0);
          rig.torso.rotation.x = 0.32;
          rig.headGroup.rotation.x = 0.25;
          break;

        case 'thank':
          // Right hand over heart, bowing gratefully
          rig.rightArm.armGroup.rotation.set(-1.2, 0, -0.5);
          rig.rightArm.forearmGroup.rotation.set(-1.1, 0, 0);
          rig.leftArm.armGroup.rotation.set(0, 0, 0.1);
          rig.torso.rotation.x = 0.12 + p * 0.04;
          rig.headGroup.rotation.x = 0.15;
          break;

        case 'support':
          // Open cupped palms pleading for voter support
          rig.leftArm.armGroup.rotation.set(-1.2, 0, 0.25);
          rig.rightArm.armGroup.rotation.set(-1.2, 0, -0.25);
          rig.leftArm.forearmGroup.rotation.set(-0.5 + p * 0.1, 0, 0);
          rig.rightArm.forearmGroup.rotation.set(-0.5 + p * 0.1, 0, 0);
          rig.torso.rotation.x = 0.1;
          break;

        default:
          break;
      }
    }

    // Landscape Mode Request & Fullscreen API
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
    animate();
  </script>
</body>
</html>
'''

print("Part 3 (Engine & Assets) defined.")
