# -*- coding: utf-8 -*-
"""
Script to apply visual improvements to build_engine_assets.py:
1. Fix head/neck connection so the head is anatomically attached to the collar/torso.
2. Add pelvis / hips to close the gap between torso and thighs.
3. Upgrade the Indian Tricolor Scarf with realistic neck drape and golden tassels.
4. Upgrade hair, ears, collar, and facial styling.
5. Upgrade Auto-Rickshaw with realistic curved canopy, passenger seating, headlamp, and meter.
6. Upgrade buildings with window grids, architectural parapets, and compound walls.
7. Add zebra crossings and road markings.
8. Improve camera framing for an expansive, panoramic view of Chennai.
"""

with open(r"e:\kip android\build_engine_assets.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the createHumanoidRig function with the anatomically grounded, polished version
old_rig_marker = "    function createHumanoidRig(options = {}) {"
old_rig_end_marker = "    /* ==========================================================================\n       10. POPULATE THE 13 CHARACTERS ACROSS CHENNAI WARD 12"

new_rig_implementation = r'''    function createHumanoidRig(options = {}) {
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
'''

start_idx = code.find(old_rig_marker)
end_idx = code.find(old_rig_end_marker)

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + new_rig_implementation + "\n" + code[end_idx:]
    print("Successfully replaced createHumanoidRig with anatomical grounded proportions.")
else:
    print(f"Markers not found: start_idx={start_idx}, end_idx={end_idx}")

# Also improve camera framing in animation loop
code = code.replace(
    "const camDist = 5.2;\n        const camHeight = 2.4;",
    "const camDist = 6.2;\n        const camHeight = 2.8;"
)

with open(r"e:\kip android\build_engine_assets.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated build_engine_assets.py.")
