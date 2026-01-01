# 🔀 Vanilla Palette Color Mix Projections

This document shows *virtual* 50/50 mix results projected onto the closest existing palette color.

## 📊 Summary

- Palette size: **64 colors**
- Total mix combinations: **136**
- Average ΔE (CIEDE2000): **3.05**
- Worst-case ΔE: **8.09**

## Generation 0 (5 colors)

### ![White](icons/white.png) White
- **Hex:** ` #F9FFFE `
- **RGB:** ` (249, 255, 254) `
- **Lab:** ` (99.54, -2.14, -0.21) `
- **Mixed from:** _Base color_

**Definition:**
```js
global White as Color = Color('white', '#F9FFFE');
```

### ![Yellow](icons/yellow.png) Yellow
- **Hex:** ` #FED83D `
- **RGB:** ` (254, 216, 61) `
- **Lab:** ` (87.25, -1.68, 75.81) `
- **Mixed from:** _Base color_

**Definition:**
```js
global Yellow as Color = Color('yellow', '#FED83D');
```

### ![Blue](icons/blue.png) Blue
- **Hex:** ` #3C44AA `
- **RGB:** ` (60, 68, 170) `
- **Lab:** ` (33.98, 29.61, -55.84) `
- **Mixed from:** _Base color_

**Definition:**
```js
global Blue as Color = Color('blue', '#3C44AA');
```

**Projections:**
```js
// Blue
/*  7.25 */ Blue.addMix([Purple, Blue]);
```

### ![Red](icons/red.png) Red
- **Hex:** ` #B02E26 `
- **RGB:** ` (176, 46, 38) `
- **Lab:** ` (40.12, 51.64, 36.32) `
- **Mixed from:** _Base color_

**Definition:**
```js
global Red as Color = Color('red', '#B02E26');
```

**Projections:**
```js
// Red
/*  4.87 */ Red.addMix([Brown, Red]);
```

### ![Black](icons/black.png) Black
- **Hex:** ` #1D1D21 `
- **RGB:** ` (29, 29, 33) `
- **Lab:** ` (10.92, 1.06, -2.73) `
- **Mixed from:** _Base color_

**Definition:**
```js
global Black as Color = Color('black', '#1D1D21');
```

**Projections:**
```js
// Black
/*  8.09 */ Black.addMix([Gray, Black]);
```

## Generation 1 (9 colors)

### ![Orange](icons/orange.png) Orange
- **Hex:** ` #F9801D `
- **RGB:** ` (249, 128, 29) `
- **Lab:** ` (66.26, 40.82, 67.60) `
- **Mixed from:**
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)
  - ![Red](icons/red.png) Red (` #B02E26 `)

**Definition:**
```js
global Orange as Color = Color('orange', '#F9801D');
```

**Projections:**
```js
// Orange
/*  0.00 */ Orange.addMix([Yellow, Red]);
/*  5.22 */ Orange.addMix([Orange, Pink]);
```

### ![LightBlue](icons/light_blue.png) Light Blue
- **Hex:** ` #3AB3DA `
- **RGB:** ` (58, 179, 218) `
- **Lab:** ` (68.17, -20.41, -29.19) `
- **Mixed from:**
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global LightBlue as Color = Color('light_blue', '#3AB3DA');
```

**Projections:**
```js
// LightBlue
/*  0.00 */ LightBlue.addMix([White, Blue]);
```

### ![Pink](icons/pink.png) Pink
- **Hex:** ` #F38BAA `
- **RGB:** ` (243, 139, 170) `
- **Lab:** ` (69.77, 43.01, 1.14) `
- **Mixed from:**
  - ![Red](icons/red.png) Red (` #B02E26 `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global Pink as Color = Color('pink', '#F38BAA');
```

**Projections:**
```js
// Pink
/*  0.00 */ Pink.addMix([White, Red]);
/*  7.94 */ Pink.addMix([Pink, LightGray]);
```

### ![Gray](icons/gray.png) Gray
- **Hex:** ` #474F52 `
- **RGB:** ` (71, 79, 82) `
- **Lab:** ` (33.01, -2.48, -2.86) `
- **Mixed from:**
  - ![Black](icons/black.png) Black (` #1D1D21 `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global Gray as Color = Color('gray', '#474F52');
```

**Projections:**
```js
// Gray
/*  0.00 */ Gray.addMix([White, Black]);
/*  6.39 */ Gray.addMix([LightGray, Black]);
```

### ![Purple](icons/purple.png) Purple
- **Hex:** ` #8932B8 `
- **RGB:** ` (137, 50, 184) `
- **Lab:** ` (39.68, 57.93, -54.52) `
- **Mixed from:**
  - ![Red](icons/red.png) Red (` #B02E26 `)
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)

**Definition:**
```js
global Purple as Color = Color('purple', '#8932B8');
```

**Projections:**
```js
// Purple
/*  0.00 */ Purple.addMix([Blue, Red]);
/*  4.20 */ Purple.addMix([Magenta, Blue]);
/*  7.07 */ Purple.addMix([Magenta, Purple]);
```

### ![Green](icons/green.png) Green
- **Hex:** ` #5E7C16 `
- **RGB:** ` (94, 124, 22) `
- **Lab:** ` (48.07, -25.57, 47.61) `
- **Mixed from:**
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)

**Definition:**
```js
global Green as Color = Color('green', '#5E7C16');
```

**Projections:**
```js
// Green
/*  0.00 */ Green.addMix([Yellow, Blue]);
/*  5.80 */ Green.addMix([Yellow, Black]);
```

### ![ArcaneRed](icons/red+black.png) Arcane Red
- **Hex:** ` #612925 `
- **RGB:** ` (97, 41, 37) `
- **Lab:** ` (24.52, 25.08, 14.95) `
- **Mixed from:**
  - ![Red](icons/red.png) Red (` #B02E26 `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global ArcaneRed as Color = Color('arcane_red', '#612925');
```

**Projections:**
```js
// ArcaneRed
/*  0.00 */ ArcaneRed.addMix([Red, Black]);
/*  7.19 */ ArcaneRed.addMix([Gray, Red]);
```

### ![Galaxea](icons/blue+black.png) Galaxea
- **Hex:** ` #32355E `
- **RGB:** ` (50, 53, 94) `
- **Lab:** ` (23.78, 10.87, -24.91) `
- **Mixed from:**
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global Galaxea as Color = Color('galaxea', '#32355E');
```

**Projections:**
```js
// Galaxea
/*  0.00 */ Galaxea.addMix([Blue, Black]);
/*  7.91 */ Galaxea.addMix([Gray, Blue]);
```

### ![SpaetzleYellow](icons/white+yellow.png) Spätzle Yellow
- **Hex:** ` #FBEC89 `
- **RGB:** ` (251, 236, 137) `
- **Lab:** ` (92.71, -7.99, 49.61) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)

**Definition:**
```js
global SpaetzleYellow as Color = Color('spaetzle_yellow', '#FBEC89');
```

**Projections:**
```js
// SpaetzleYellow
/*  0.00 */ SpaetzleYellow.addMix([White, Yellow]);
```

## Generation 2 (23 colors)

### ![Magenta](icons/magenta.png) Magenta
- **Hex:** ` #C74EBD `
- **RGB:** ` (199, 78, 189) `
- **Lab:** ` (53.24, 61.52, -35.30) `
- **Mixed from:**
  - ![Purple](icons/purple.png) Purple (` #8932B8 `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global Magenta as Color = Color('magenta', '#C74EBD');
```

**Projections:**
```js
// Magenta
/*  0.00 */ Magenta.addMix([White, Purple]);
/*  3.92 */ Magenta.addMix([Pink, Purple]);
```

### ![Lime](icons/lime.png) Lime
- **Hex:** ` #80C71F `
- **RGB:** ` (128, 199, 31) `
- **Lab:** ` (73.24, -45.86, 68.31) `
- **Mixed from:**
  - ![Green](icons/green.png) Green (` #5E7C16 `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global Lime as Color = Color('lime', '#80C71F');
```

**Projections:**
```js
// Lime
/*  0.00 */ Lime.addMix([White, Green]);
/*  5.21 */ Lime.addMix([Lime, LightGray]);
```

### ![LightGray](icons/light_gray.png) Light Gray
- **Hex:** ` #9D9D97 `
- **RGB:** ` (157, 157, 151) `
- **Lab:** ` (64.58, -1.12, 3.14) `
- **Mixed from:**
  - ![Gray](icons/gray.png) Gray (` #474F52 `)
  - ![White](icons/white.png) White (` #F9FFFE `)

**Definition:**
```js
global LightGray as Color = Color('light_gray', '#9D9D97');
```

**Projections:**
```js
// LightGray
/*  0.00 */ LightGray.addMix([White, Gray]);
```

### ![Cyan](icons/cyan.png) Cyan
- **Hex:** ` #169C9C `
- **RGB:** ` (22, 156, 156) `
- **Lab:** ` (58.37, -32.24, -9.53) `
- **Mixed from:**
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)
  - ![Green](icons/green.png) Green (` #5E7C16 `)

**Definition:**
```js
global Cyan as Color = Color('cyan', '#169C9C');
```

**Projections:**
```js
// Cyan
/*  0.00 */ Cyan.addMix([Blue, Green]);
/*  4.66 */ Cyan.addMix([LightGray, Cyan]);
```

### ![Brown](icons/brown.png) Brown
- **Hex:** ` #835432 `
- **RGB:** ` (131, 84, 50) `
- **Lab:** ` (40.24, 15.90, 27.69) `
- **Mixed from:**
  - ![Black](icons/black.png) Black (` #1D1D21 `)
  - ![Orange](icons/orange.png) Orange (` #F9801D `)

**Definition:**
```js
global Brown as Color = Color('brown', '#835432');
```

**Projections:**
```js
// Brown
/*  0.00 */ Brown.addMix([Orange, Black]);
/*  6.49 */ Brown.addMix([Green, Red]);
```

### ![WizardsBrew](icons/light_blue+pink.png) Wizard’s Brew
- **Hex:** ` #9890B9 `
- **RGB:** ` (152, 144, 185) `
- **Lab:** ` (61.76, 11.49, -20.26) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)

**Definition:**
```js
global WizardsBrew as Color = Color('wizards_brew', '#9890B9');
```

**Projections:**
```js
// WizardsBrew
/*  0.00 */ WizardsBrew.addMix([LightBlue, Pink]);
```

### ![IndianSilk](icons/pink+black.png) Indian Silk
- **Hex:** ` #845468 `
- **RGB:** ` (132, 84, 104) `
- **Lab:** ` (41.60, 23.01, -3.18) `
- **Mixed from:**
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global IndianSilk as Color = Color('indian_silk', '#845468');
```

**Projections:**
```js
// IndianSilk
/*  0.00 */ IndianSilk.addMix([Pink, Black]);
/*  2.90 */ IndianSilk.addMix([Purple, Brown]);
/*  3.26 */ IndianSilk.addMix([LightBlue, Red]);
```

### ![RichGold](icons/orange+green.png) Rich Gold
- **Hex:** ` #A38019 `
- **RGB:** ` (163, 128, 25) `
- **Lab:** ` (55.37, 3.92, 55.47) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Green](icons/green.png) Green (` #5E7C16 `)

**Definition:**
```js
global RichGold as Color = Color('rich_gold', '#A38019');
```

**Projections:**
```js
// RichGold
/*  0.00 */ RichGold.addMix([Orange, Green]);
```

### ![FadingNight](icons/light_blue+blue.png) Fading Night
- **Hex:** ` #3B78C3 `
- **RGB:** ` (59, 120, 195) `
- **Lab:** ` (49.86, 5.20, -44.93) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)

**Definition:**
```js
global FadingNight as Color = Color('fading_night', '#3B78C3');
```

**Projections:**
```js
// FadingNight
/*  0.00 */ FadingNight.addMix([LightBlue, Blue]);
/*  6.12 */ FadingNight.addMix([Cyan, Blue]);
```

### ![TreetopCathedral](icons/green+black.png) Treetop Cathedral
- **Hex:** ` #334B18 `
- **RGB:** ` (51, 75, 24) `
- **Lab:** ` (28.91, -18.98, 26.76) `
- **Mixed from:**
  - ![Green](icons/green.png) Green (` #5E7C16 `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global TreetopCathedral as Color = Color('treetop_cathedral', '#334B18');
```

**Projections:**
```js
// TreetopCathedral
/*  0.00 */ TreetopCathedral.addMix([Green, Black]);
```

### ![PurpleProtege](icons/purple+black.png) Purple Protégé
- **Hex:** ` #55316C `
- **RGB:** ` (85, 49, 108) `
- **Lab:** ` (27.33, 28.20, -28.11) `
- **Mixed from:**
  - ![Purple](icons/purple.png) Purple (` #8932B8 `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global PurpleProtege as Color = Color('purple_protege', '#55316C');
```

**Projections:**
```js
// PurpleProtege
/*  0.00 */ PurpleProtege.addMix([Purple, Black]);
/*  7.02 */ PurpleProtege.addMix([Magenta, Black]);
/*  7.15 */ PurpleProtege.addMix([Gray, Purple]);
```

### ![Beer](icons/orange+yellow.png) Beer
- **Hex:** ` #FCAB29 `
- **RGB:** ` (252, 171, 41) `
- **Lab:** ` (76.06, 20.13, 72.12) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)

**Definition:**
```js
global Beer as Color = Color('beer', '#FCAB29');
```

**Projections:**
```js
// Beer
/*  0.00 */ Beer.addMix([Orange, Yellow]);
/*  6.70 */ Beer.addMix([White, Orange]);
```

### ![Lizard](icons/purple+green.png) Lizard
- **Hex:** ` #7D6E49 `
- **RGB:** ` (125, 110, 73) `
- **Lab:** ` (46.97, 0.21, 22.80) `
- **Mixed from:**
  - ![Purple](icons/purple.png) Purple (` #8932B8 `)
  - ![Green](icons/green.png) Green (` #5E7C16 `)

**Definition:**
```js
global Lizard as Color = Color('lizard', '#7D6E49');
```

**Projections:**
```js
// Lizard
/*  0.00 */ Lizard.addMix([Purple, Green]);
/*  6.17 */ Lizard.addMix([Orange, Gray]);
/*  7.38 */ Lizard.addMix([Orange, Blue]);
/*  7.97 */ Lizard.addMix([Brown, Green]);
```

### ![TotallyBroccoli](icons/yellow+gray.png) Totally Broccoli
- **Hex:** ` #8C9C4D `
- **RGB:** ` (140, 156, 77) `
- **Lab:** ` (61.56, -18.08, 39.13) `
- **Mixed from:**
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)
  - ![Gray](icons/gray.png) Gray (` #474F52 `)

**Definition:**
```js
global TotallyBroccoli as Color = Color('totally_broccoli', '#8C9C4D');
```

**Projections:**
```js
// TotallyBroccoli
/*  0.00 */ TotallyBroccoli.addMix([Yellow, Gray]);
/*  1.98 */ TotallyBroccoli.addMix([LightGray, Green]);
/*  4.00 */ TotallyBroccoli.addMix([Orange, LightBlue]);
/*  5.88 */ TotallyBroccoli.addMix([Lime, Purple]);
/*  7.86 */ TotallyBroccoli.addMix([Lime, Brown]);
/*  7.96 */ TotallyBroccoli.addMix([Lime, Green]);
```

### ![MysteriousBlue](icons/light_blue+gray.png) Mysterious Blue
- **Hex:** ` #487E8E `
- **RGB:** ` (72, 126, 142) `
- **Lab:** ` (49.80, -13.33, -14.21) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![Gray](icons/gray.png) Gray (` #474F52 `)

**Definition:**
```js
global MysteriousBlue as Color = Color('mysterious_blue', '#487E8E');
```

**Projections:**
```js
// MysteriousBlue
/*  0.00 */ MysteriousBlue.addMix([LightBlue, Gray]);
```

### ![Langoustine](icons/orange+red.png) Langoustine
- **Hex:** ` #D44E22 `
- **RGB:** ` (212, 78, 34) `
- **Lab:** ` (51.34, 50.81, 51.33) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Red](icons/red.png) Red (` #B02E26 `)

**Definition:**
```js
global Langoustine as Color = Color('langoustine', '#D44E22');
```

**Projections:**
```js
// Langoustine
/*  0.00 */ Langoustine.addMix([Orange, Red]);
```

### ![BerriesNCream](icons/white+pink.png) Berries N’ Cream
- **Hex:** ` #F7BECF `
- **RGB:** ` (247, 190, 207) `
- **Lab:** ` (82.44, 22.98, -0.59) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)

**Definition:**
```js
global BerriesNCream as Color = Color('berries_n_cream', '#F7BECF');
```

**Projections:**
```js
// BerriesNCream
/*  0.00 */ BerriesNCream.addMix([White, Pink]);
```

### ![StrawberryMoon](icons/pink+red.png) Strawberry Moon
- **Hex:** ` #D7536D `
- **RGB:** ` (215, 83, 109) `
- **Lab:** ` (53.75, 53.88, 12.83) `
- **Mixed from:**
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)
  - ![Red](icons/red.png) Red (` #B02E26 `)

**Definition:**
```js
global StrawberryMoon as Color = Color('strawberry_moon', '#D7536D');
```

**Projections:**
```js
// StrawberryMoon
/*  0.00 */ StrawberryMoon.addMix([Pink, Red]);
/*  7.97 */ StrawberryMoon.addMix([LightGray, Red]);
```

### ![Apricot](icons/yellow+pink.png) Apricot
- **Hex:** ` #FAB06F `
- **RGB:** ` (250, 176, 111) `
- **Lab:** ` (77.59, 20.24, 43.79) `
- **Mixed from:**
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)

**Definition:**
```js
global Apricot as Color = Color('apricot', '#FAB06F');
```

**Projections:**
```js
// Apricot
/*  0.00 */ Apricot.addMix([Yellow, Pink]);
```

### ![Fluorescence](icons/light_blue+yellow.png) Fluorescence
- **Hex:** ` #8CD873 `
- **RGB:** ` (140, 216, 115) `
- **Lab:** ` (79.57, -42.10, 42.34) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)

**Definition:**
```js
global Fluorescence as Color = Color('fluorescence', '#8CD873');
```

**Projections:**
```js
// Fluorescence
/*  0.00 */ Fluorescence.addMix([LightBlue, Yellow]);
/*  4.36 */ Fluorescence.addMix([Yellow, Cyan]);
/*  5.27 */ Fluorescence.addMix([LightBlue, Lime]);
```

### ![BimiGreen](icons/gray+green.png) Bimi Green
- **Hex:** ` #4E692C `
- **RGB:** ` (78, 105, 44) `
- **Lab:** ` (41.06, -21.08, 30.68) `
- **Mixed from:**
  - ![Gray](icons/gray.png) Gray (` #474F52 `)
  - ![Green](icons/green.png) Green (` #5E7C16 `)

**Definition:**
```js
global BimiGreen as Color = Color('bimi_green', '#4E692C');
```

**Projections:**
```js
// BimiGreen
/*  0.00 */ BimiGreen.addMix([Gray, Green]);
/*  4.23 */ BimiGreen.addMix([Lime, Black]);
```

### ![Atlantis](icons/light_blue+black.png) Atlantis
- **Hex:** ` #346576 `
- **RGB:** ` (52, 101, 118) `
- **Lab:** ` (40.16, -11.32, -14.61) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global Atlantis as Color = Color('atlantis', '#346576');
```

**Projections:**
```js
// Atlantis
/*  0.00 */ Atlantis.addMix([LightBlue, Black]);
```

### ![NeverForget](icons/pink+gray.png) Never Forget
- **Hex:** ` #9B6A7D `
- **RGB:** ` (155, 106, 125) `
- **Lab:** ` (50.40, 22.51, -2.59) `
- **Mixed from:**
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)
  - ![Gray](icons/gray.png) Gray (` #474F52 `)

**Definition:**
```js
global NeverForget as Color = Color('never_forget', '#9B6A7D');
```

**Projections:**
```js
// NeverForget
/*  0.00 */ NeverForget.addMix([Pink, Gray]);
```

## Generation 3 (27 colors)

### ![Morocco](icons/pink+brown.png) Morocco
- **Hex:** ` #C26E65 `
- **RGB:** ` (194, 110, 101) `
- **Lab:** ` (55.65, 32.27, 19.63) `
- **Mixed from:**
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global Morocco as Color = Color('morocco', '#C26E65');
```

**Projections:**
```js
// Morocco
/*  0.00 */ Morocco.addMix([Pink, Brown]);
```

### ![ToadKing](icons/cyan+brown.png) Toad King
- **Hex:** ` #4D715B `
- **RGB:** ` (77, 113, 91) `
- **Lab:** ` (44.44, -17.93, 8.17) `
- **Mixed from:**
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global ToadKing as Color = Color('toad_king', '#4D715B');
```

**Projections:**
```js
// ToadKing
/*  0.00 */ ToadKing.addMix([Cyan, Brown]);
/*  7.86 */ ToadKing.addMix([LightBlue, Brown]);
```

### ![Frappe](icons/white+brown.png) Frappé
- **Hex:** ` #C5A188 `
- **RGB:** ` (197, 161, 136) `
- **Lab:** ` (68.85, 9.63, 18.03) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global Frappe as Color = Color('frappe', '#C5A188');
```

**Projections:**
```js
// Frappe
/*  0.00 */ Frappe.addMix([White, Brown]);
/*  6.40 */ Frappe.addMix([Yellow, Purple]);
/*  7.45 */ Frappe.addMix([Magenta, Yellow]);
```

### ![DarkRum](icons/brown+black.png) Dark Rum
- **Hex:** ` #483B2A `
- **RGB:** ` (72, 59, 42) `
- **Lab:** ` (25.78, 2.84, 12.68) `
- **Mixed from:**
  - ![Brown](icons/brown.png) Brown (` #835432 `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global DarkRum as Color = Color('dark_rum', '#483B2A');
```

**Projections:**
```js
// DarkRum
/*  0.00 */ DarkRum.addMix([Brown, Black]);
/*  7.90 */ DarkRum.addMix([Gray, Brown]);
```

### ![VolcanicAsh](icons/gray+light_gray.png) Volcanic Ash
- **Hex:** ` #717777 `
- **RGB:** ` (113, 119, 119) `
- **Lab:** ` (49.54, -2.25, -0.78) `
- **Mixed from:**
  - ![Gray](icons/gray.png) Gray (` #474F52 `)
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)

**Definition:**
```js
global VolcanicAsh as Color = Color('volcanic_ash', '#717777');
```

**Projections:**
```js
// VolcanicAsh
/*  0.00 */ VolcanicAsh.addMix([Gray, LightGray]);
```

### ![CandyFloss](icons/white+magenta.png) Candy Floss
- **Hex:** ` #DE9FDC `
- **RGB:** ` (222, 159, 220) `
- **Lab:** ` (73.22, 33.22, -21.67) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)

**Definition:**
```js
global CandyFloss as Color = Color('candy_floss', '#DE9FDC');
```

**Projections:**
```js
// CandyFloss
/*  0.00 */ CandyFloss.addMix([White, Magenta]);
```

### ![SpicyPurple](icons/magenta+red.png) Spicy Purple
- **Hex:** ` #C03B71 `
- **RGB:** ` (192, 59, 113) `
- **Lab:** ` (46.35, 57.01, -0.68) `
- **Mixed from:**
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)
  - ![Red](icons/red.png) Red (` #B02E26 `)

**Definition:**
```js
global SpicyPurple as Color = Color('spicy_purple', '#C03B71');
```

**Projections:**
```js
// SpicyPurple
/*  0.00 */ SpicyPurple.addMix([Magenta, Red]);
/*  7.06 */ SpicyPurple.addMix([Magenta, Brown]);
/*  7.88 */ SpicyPurple.addMix([Purple, Red]);
```

### ![LightBrown](icons/orange+brown.png) Light Brown
- **Hex:** ` #B16927 `
- **RGB:** ` (177, 105, 39) `
- **Lab:** ` (51.38, 23.62, 47.23) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global LightBrown as Color = Color('light_brown', '#B16927');
```

**Projections:**
```js
// LightBrown
/*  0.00 */ LightBrown.addMix([Orange, Brown]);
/*  1.71 */ LightBrown.addMix([Lime, Red]);
/*  5.93 */ LightBrown.addMix([Orange, Purple]);
```

### ![SalsaVerde](icons/yellow+light_gray.png) Salsa Verde
- **Hex:** ` #C5C462 `
- **RGB:** ` (197, 196, 98) `
- **Lab:** ` (77.42, -13.06, 48.79) `
- **Mixed from:**
  - ![Yellow](icons/yellow.png) Yellow (` #FED83D `)
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)

**Definition:**
```js
global SalsaVerde as Color = Color('salsa_verde', '#C5C462');
```

**Projections:**
```js
// SalsaVerde
/*  0.00 */ SalsaVerde.addMix([Yellow, LightGray]);
/*  6.74 */ SalsaVerde.addMix([Yellow, Green]);
```

### ![TwinkleNight](icons/magenta+cyan.png) Twinkle Night
- **Hex:** ` #6D6DB0 `
- **RGB:** ` (109, 109, 176) `
- **Lab:** ` (48.66, 16.73, -35.67) `
- **Mixed from:**
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)

**Definition:**
```js
global TwinkleNight as Color = Color('twinkle_night', '#6D6DB0');
```

**Projections:**
```js
// TwinkleNight
/*  0.00 */ TwinkleNight.addMix([Magenta, Cyan]);
/*  3.91 */ TwinkleNight.addMix([LightGray, Blue]);
/*  4.77 */ TwinkleNight.addMix([LightBlue, Purple]);
/*  6.02 */ TwinkleNight.addMix([Magenta, LightBlue]);
/*  6.52 */ TwinkleNight.addMix([Cyan, Purple]);
```

### ![DeepSeaDiver](icons/cyan+black.png) Deep Sea Diver
- **Hex:** ` #20565A `
- **RGB:** ` (32, 86, 90) `
- **Lab:** ` (33.35, -16.23, -7.64) `
- **Mixed from:**
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)
  - ![Black](icons/black.png) Black (` #1D1D21 `)

**Definition:**
```js
global DeepSeaDiver as Color = Color('deep_sea_diver', '#20565A');
```

**Projections:**
```js
// DeepSeaDiver
/*  0.00 */ DeepSeaDiver.addMix([Cyan, Black]);
```

### ![PinotNoir](icons/blue+brown.png) Pinot Noir
- **Hex:** ` #5E525C `
- **RGB:** ` (94, 82, 92) `
- **Lab:** ` (36.34, 6.96, -4.00) `
- **Mixed from:**
  - ![Blue](icons/blue.png) Blue (` #3C44AA `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global PinotNoir as Color = Color('pinot_noir', '#5E525C');
```

**Projections:**
```js
// PinotNoir
/*  0.00 */ PinotNoir.addMix([Blue, Brown]);
/*  6.38 */ PinotNoir.addMix([Cyan, Red]);
```

### ![KryptoniteGreen](icons/cyan+green.png) Kryptonite Green
- **Hex:** ` #37933E `
- **RGB:** ` (55, 147, 62) `
- **Lab:** ` (54.06, -45.15, 36.57) `
- **Mixed from:**
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)
  - ![Green](icons/green.png) Green (` #5E7C16 `)

**Definition:**
```js
global KryptoniteGreen as Color = Color('kryptonite_green', '#37933E');
```

**Projections:**
```js
// KryptoniteGreen
/*  0.00 */ KryptoniteGreen.addMix([Cyan, Green]);
/*  3.61 */ KryptoniteGreen.addMix([Lime, Blue]);
/*  5.64 */ KryptoniteGreen.addMix([Lime, Gray]);
/*  6.75 */ KryptoniteGreen.addMix([Orange, Cyan]);
```

### ![SummerOf82](icons/white+cyan.png) Summer of ’82
- **Hex:** ` #76CED7 `
- **RGB:** ` (118, 206, 215) `
- **Lab:** ` (77.82, -24.12, -12.72) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)

**Definition:**
```js
global SummerOf82 as Color = Color('summer_of82', '#76CED7');
```

**Projections:**
```js
// SummerOf82
/*  0.00 */ SummerOf82.addMix([White, Cyan]);
/*  7.45 */ SummerOf82.addMix([White, LightBlue]);
```

### ![IronFist](icons/white+light_gray.png) Iron Fist
- **Hex:** ` #C8CAC9 `
- **RGB:** ` (200, 202, 201) `
- **Lab:** ` (81.15, -0.86, 0.26) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)

**Definition:**
```js
global IronFist as Color = Color('iron_fist', '#C8CAC9');
```

**Projections:**
```js
// IronFist
/*  0.00 */ IronFist.addMix([White, LightGray]);
```

### ![Greenfinch](icons/orange+lime.png) Greenfinch
- **Hex:** ` #B9A11D `
- **RGB:** ` (185, 161, 29) `
- **Lab:** ` (66.44, -4.00, 64.57) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Lime](icons/lime.png) Lime (` #80C71F `)

**Definition:**
```js
global Greenfinch as Color = Color('greenfinch', '#B9A11D');
```

**Projections:**
```js
// Greenfinch
/*  0.00 */ Greenfinch.addMix([Orange, Lime]);
/*  6.27 */ Greenfinch.addMix([Lime, Pink]);
```

### ![VenomousSting](icons/white+lime.png) Venomous Sting
- **Hex:** ` #CBED6B `
- **RGB:** ` (203, 237, 107) `
- **Lab:** ` (89.08, -29.87, 58.34) `
- **Mixed from:**
  - ![White](icons/white.png) White (` #F9FFFE `)
  - ![Lime](icons/lime.png) Lime (` #80C71F `)

**Definition:**
```js
global VenomousSting as Color = Color('venomous_sting', '#CBED6B');
```

**Projections:**
```js
// VenomousSting
/*  0.00 */ VenomousSting.addMix([White, Lime]);
/*  7.36 */ VenomousSting.addMix([Yellow, Lime]);
```

### ![CrownJewels](icons/light_gray+purple.png) Crown Jewels
- **Hex:** ` #9367A7 `
- **RGB:** ` (147, 103, 167) `
- **Lab:** ` (50.33, 29.52, -27.56) `
- **Mixed from:**
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)
  - ![Purple](icons/purple.png) Purple (` #8932B8 `)

**Definition:**
```js
global CrownJewels as Color = Color('crown_jewels', '#9367A7');
```

**Projections:**
```js
// CrownJewels
/*  0.00 */ CrownJewels.addMix([LightGray, Purple]);
/*  3.05 */ CrownJewels.addMix([Pink, Blue]);
```

### ![GreenWithEnvy](icons/lime+cyan.png) Green With Envy
- **Hex:** ` #3FBA4A `
- **RGB:** ` (63, 186, 74) `
- **Lab:** ` (67.03, -56.35, 46.06) `
- **Mixed from:**
  - ![Lime](icons/lime.png) Lime (` #80C71F `)
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)

**Definition:**
```js
global GreenWithEnvy as Color = Color('green_with_envy', '#3FBA4A');
```

**Projections:**
```js
// GreenWithEnvy
/*  0.00 */ GreenWithEnvy.addMix([Lime, Cyan]);
/*  5.35 */ GreenWithEnvy.addMix([LightBlue, Green]);
```

### ![WhiskyBarrel](icons/light_gray+brown.png) Whisky Barrel
- **Hex:** ` #95775D `
- **RGB:** ` (149, 119, 93) `
- **Lab:** ` (52.26, 7.90, 18.75) `
- **Mixed from:**
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)
  - ![Brown](icons/brown.png) Brown (` #835432 `)

**Definition:**
```js
global WhiskyBarrel as Color = Color('whisky_barrel', '#95775D');
```

**Projections:**
```js
// WhiskyBarrel
/*  0.00 */ WhiskyBarrel.addMix([LightGray, Brown]);
/*  5.33 */ WhiskyBarrel.addMix([Magenta, Green]);
```

### ![SuperPink](icons/magenta+pink.png) Super Pink
- **Hex:** ` #DD6CB2 `
- **RGB:** ` (221, 108, 178) `
- **Lab:** ` (61.06, 52.35, -16.66) `
- **Mixed from:**
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)

**Definition:**
```js
global SuperPink as Color = Color('super_pink', '#DD6CB2');
```

**Projections:**
```js
// SuperPink
/*  0.00 */ SuperPink.addMix([Magenta, Pink]);
/*  7.72 */ SuperPink.addMix([Magenta, LightGray]);
```

### ![Jaffa](icons/orange+magenta.png) Jaffa
- **Hex:** ` #D9764E `
- **RGB:** ` (217, 118, 78) `
- **Lab:** ` (60.12, 35.22, 38.84) `
- **Mixed from:**
  - ![Orange](icons/orange.png) Orange (` #F9801D `)
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)

**Definition:**
```js
global Jaffa as Color = Color('jaffa', '#D9764E');
```

**Projections:**
```js
// Jaffa
/*  0.00 */ Jaffa.addMix([Orange, Magenta]);
```

### ![Kathmandu](icons/magenta+lime.png) Kathmandu
- **Hex:** ` #B0975A `
- **RGB:** ` (176, 151, 90) `
- **Lab:** ` (63.43, 1.14, 35.42) `
- **Mixed from:**
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)
  - ![Lime](icons/lime.png) Lime (` #80C71F `)

**Definition:**
```js
global Kathmandu as Color = Color('kathmandu', '#B0975A');
```

**Projections:**
```js
// Kathmandu
/*  0.00 */ Kathmandu.addMix([Magenta, Lime]);
/*  5.45 */ Kathmandu.addMix([Yellow, Brown]);
/*  6.09 */ Kathmandu.addMix([Orange, LightGray]);
/*  6.21 */ Kathmandu.addMix([Pink, Green]);
```

### ![Ming](icons/gray+cyan.png) Ming
- **Hex:** ` #327173 `
- **RGB:** ` (50, 113, 115) `
- **Lab:** ` (43.84, -19.42, -7.25) `
- **Mixed from:**
  - ![Gray](icons/gray.png) Gray (` #474F52 `)
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)

**Definition:**
```js
global Ming as Color = Color('ming', '#327173');
```

**Projections:**
```js
// Ming
/*  0.00 */ Ming.addMix([Gray, Cyan]);
```

### ![Tempest](icons/pink+cyan.png) Tempest
- **Hex:** ` #8088A2 `
- **RGB:** ` (128, 136, 162) `
- **Lab:** ` (56.89, 2.86, -14.76) `
- **Mixed from:**
  - ![Pink](icons/pink.png) Pink (` #F38BAA `)
  - ![Cyan](icons/cyan.png) Cyan (` #169C9C `)

**Definition:**
```js
global Tempest as Color = Color('tempest', '#8088A2');
```

**Projections:**
```js
// Tempest
/*  0.00 */ Tempest.addMix([Pink, Cyan]);
```

### ![GrapeCandy](icons/magenta+gray.png) Grape Candy
- **Hex:** ` #885187 `
- **RGB:** ` (136, 81, 135) `
- **Lab:** ` (42.56, 31.85, -20.64) `
- **Mixed from:**
  - ![Magenta](icons/magenta.png) Magenta (` #C74EBD `)
  - ![Gray](icons/gray.png) Gray (` #474F52 `)

**Definition:**
```js
global GrapeCandy as Color = Color('grape_candy', '#885187');
```

**Projections:**
```js
// GrapeCandy
/*  0.00 */ GrapeCandy.addMix([Magenta, Gray]);
```

### ![Seaside](icons/light_blue+light_gray.png) Seaside
- **Hex:** ` #6BA7B5 `
- **RGB:** ` (107, 167, 181) `
- **Lab:** ` (65.04, -15.74, -13.33) `
- **Mixed from:**
  - ![LightBlue](icons/light_blue.png) LightBlue (` #3AB3DA `)
  - ![LightGray](icons/light_gray.png) LightGray (` #9D9D97 `)

**Definition:**
```js
global Seaside as Color = Color('seaside', '#6BA7B5');
```

**Projections:**
```js
// Seaside
/*  0.00 */ Seaside.addMix([LightBlue, LightGray]);
/*  6.21 */ Seaside.addMix([LightBlue, Cyan]);
```
