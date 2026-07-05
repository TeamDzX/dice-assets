# Dice — In-App Purchase Metadata (App Store Connect)

Five products, all **Non-Consumable**, under app `TeamDZX.dice`.
Base price territory: **United Kingdom** — let Apple auto-generate all other
territories from the GBP base. Decided 2026-07-05.

Every product needs a **review screenshot** (any Pack Gallery screenshot
works, same one can be reused) before first submission. The app's Restore
Purchases button (gallery footer) satisfies the restore requirement.

Character limits: Display Name ≤ 30, Description ≤ 45.

---

## 1. All Dice Styles — £1.99

- **Product ID:** `TeamDZX.dice.pack.dicestyles`
- **Reference name:** Dice — All Dice Styles
- Covers: Metal Works, Gemstones, Neon Glow + every future dice pack stamped
  with this id.

| Locale | Display name | Description |
|---|---|---|
| en-GB / en-US | All Dice Styles | Every dice style pack, now and future. |
| ja | サイコロスタイル全部 | すべてのサイコロスタイルパックを解放。 |
| zh-Hans | 全部骰子样式 | 解锁所有骰子样式包（含未来新增）。 |
| ar | كل أنماط النرد | افتح كل حزم أنماط النرد الحالية والقادمة. |
| he | כל סגנונות הקוביות | פותח את כל חבילות הסגנונות, כולל עתידיות. |
| fr-FR | Tous les styles de dés | Tous les packs de styles, actuels et futurs. |
| de-DE | Alle Würfel-Stile | Alle Stil-Packs, jetzt und in Zukunft. |
| es-ES / es-MX | Todos los estilos | Todos los packs de estilos, y los futuros. |
| pt-BR | Todos os estilos | Todos os pacotes de estilos, e os futuros. |

## 2. All Table Surfaces — £0.99

- **Product ID:** `TeamDZX.dice.pack.tables`
- **Reference name:** Dice — All Table Surfaces
- Covers: Casino Night + every future table pack.

| Locale | Display name | Description |
|---|---|---|
| en-GB / en-US | All Table Surfaces | Every table surface pack, now and future. |
| ja | テーブル素材全部 | すべてのテーブル素材パックを解放。 |
| zh-Hans | 全部桌面材质 | 解锁所有桌面材质包（含未来新增）。 |
| ar | كل أسطح الطاولة | افتح كل حزم أسطح الطاولة الحالية والقادمة. |
| he | כל משטחי השולחן | פותח את כל חבילות המשטחים, כולל עתידיות. |
| fr-FR | Toutes les surfaces | Tous les packs de surfaces, même futurs. |
| de-DE | Alle Tischoberflächen | Alle Tisch-Packs, jetzt und in Zukunft. |
| es-ES / es-MX | Todas las superficies | Todos los packs de mesas, y los futuros. |
| pt-BR | Todas as superfícies | Todos os pacotes de mesas, e os futuros. |

## 3. Party Night Pack — £1.99

- **Product ID:** `TeamDZX.dice.pack.partynight`
- **Reference name:** Dice — Party Night Pack
- Covers: this game pack only (Chinchirorin, Cee-lo, Drop Dead).

| Locale | Display name | Description |
|---|---|---|
| en-GB / en-US | Party Night Pack | Chinchirorin, Cee-lo and Drop Dead rules. |
| ja | パーティーナイトパック | チンチロリンなど3つのゲームルール。 |
| zh-Hans | 派对之夜包 | 三款派对骰子游戏的完整规则。 |
| ar | حزمة ليلة الحفلات | قواعد ثلاث ألعاب نرد حماسية. |
| he | חבילת ליל מסיבה | חוקים מלאים לשלושה משחקי קוביות. |
| fr-FR | Pack Soirée Festive | Chinchirorin, Cee-lo et Drop Dead. |
| de-DE | Partynacht-Paket | Chinchirorin, Cee-lo und Drop Dead. |
| es-ES / es-MX | Pack Noche de fiesta | Chinchirorin, Cee-lo y Drop Dead. |
| pt-BR | Pacote Noite de Festa | Chinchirorin, Cee-lo e Drop Dead. |

## 4. Tavern Classics — £1.99

- **Product ID:** `TeamDZX.dice.pack.tavernclassics`
- **Reference name:** Dice — Tavern Classics
- Covers: this game pack only (Shut the Box, Threes, Going to Boston).

| Locale | Display name | Description |
|---|---|---|
| en-GB / en-US | Tavern Classics | Shut the Box, Threes, Going to Boston. |
| ja | タバーンクラシックス | シャット・ザ・ボックスなど3ゲーム。 |
| zh-Hans | 酒馆经典 | 关盒子、逢三清零、波士顿之旅。 |
| ar | كلاسيكيات الحانة | ثلاث ألعاب نرد كلاسيكية بقواعد كاملة. |
| he | קלאסיקות הפאב | שלושה משחקי קוביות קלאסיים. |
| fr-FR | Classiques de Taverne | Shut the Box, Threes, En route pour Boston. |
| de-DE | Wirtshaus-Klassiker | Shut the Box, Threes, Nach Boston. |
| es-ES / es-MX | Clásicos de taberna | Cierra la caja, Treses, Rumbo a Boston. |
| pt-BR | Clássicos de Taverna | Feche a Caixa, Trios, Rumo a Boston. |

## 5. Everything Bundle — £4.99

- **Product ID:** `TeamDZX.dice.pack.allaccess`
- **Reference name:** Dice — Everything Bundle
- Covers: every paid pack in the gallery, current and future, regardless of
  the pack's own product id (special-cased in `PackStore.isOwned`).
- Shown as its own gift card in the gallery, hidden once owned.

| Locale | Display name | Description |
|---|---|---|
| en-GB / en-US | Everything Bundle | Every pack in the gallery. Forever. |
| ja | まるごとバンドル | ギャラリーの全パックを永久に解放。 |
| zh-Hans | 全部内容合集 | 永久解锁商店中的所有扩展包。 |
| ar | باقة كل شيء | كل الحزم في المعرض، إلى الأبد. |
| he | חבילת הכול | כל החבילות בגלריה, לתמיד. |
| fr-FR | Pack Intégral | Tous les packs de la galerie, pour toujours. |
| de-DE | Alles-Paket | Jedes Pack der Galerie, für immer. |
| es-ES / es-MX | Paquete completo | Todos los packs de la galería, para siempre. |
| pt-BR | Pacote completo | Todos os pacotes da galeria, para sempre. |

---

### Pricing sanity check

Individually: 1.99 + 0.99 + 1.99 + 1.99 = **£6.96** → bundle at **£4.99**
saves ~28%, a credible anchor without giving the catalog away.

### When adding future packs

- New dice pack → stamp `DICE_STYLES_ID` (owners get it automatically).
- New table pack → stamp `TABLES_ID`.
- New game pack → new product id `TeamDZX.dice.pack.<slug>` + new ASC product
  (copy this file's format); it is automatically covered by the Everything
  bundle with no ASC change.
