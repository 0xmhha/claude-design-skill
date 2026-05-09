/**
 * IosFrame — iPhone 15 Pro / Pro Max device frame
 *
 * Aligned to Apple-published Tech Specs (verified 2026-05-09):
 *   - iPhone 15 Pro     · 393 × 852 logical pt · 6.1" OLED · status bar 54pt · home indicator inset 34pt
 *   - iPhone 15 Pro Max · 430 × 932 logical pt · 6.7" OLED · same insets
 *
 * Includes (do NOT redraw any of these in your screen content):
 *   - Titanium-edge body bezel + per-model corner radius
 *   - Dynamic Island as a children-receiving slot
 *     (defaults to a solid black pill; pass an `island` ReactNode to mock
 *     now-playing / timer / Live Activities; auto-expands to fit content)
 *   - SF-styled status bar (time left · signal / Wi-Fi / battery right)
 *   - Home indicator bar
 *   - Content area sized between status bar and home indicator inset
 *
 * Usage:
 *   <IosFrame time="9:41" battery={85}>
 *     <YourAppContent />
 *   </IosFrame>
 *
 * Pro Max + dark + custom Dynamic Island content:
 *   <IosFrame
 *     model="iphone15promax"
 *     darkMode
 *     island={<NowPlayingPill title="Anti-Hero" artist="Taylor Swift" />}
 *   >
 *     <YourAppContent />
 *   </IosFrame>
 *
 * Test (visual smoke):
 *   render <IosFrame /> → expect 393×852 screen, black pill at top center,
 *   home indicator at bottom center, status bar reads "9:41".
 */

const iosFrameModels = {
  iphone15pro: {
    width: 393,
    height: 852,
    bodyRadius: 60,
    screenRadius: 48,
    bezel: 12,
    statusBarHeight: 54,
    bottomInset: 34,
    island: { width: 126, height: 37, top: 11 },
  },
  iphone15promax: {
    width: 430,
    height: 932,
    bodyRadius: 64,
    screenRadius: 52,
    bezel: 12,
    statusBarHeight: 54,
    bottomInset: 34,
    island: { width: 126, height: 37, top: 11 },
  },
};

const iosFrameStyles = {
  wrapper: {
    display: 'inline-block',
    position: 'relative',
    background:
      'linear-gradient(140deg, #4a4a4a 0%, #2b2b2b 38%, #1a1a1a 65%, #2e2e2e 100%)',
    boxShadow:
      '0 0 0 1px rgba(255,255,255,0.08) inset, ' +
      '0 0 0 2px #0c0c0c, ' +
      '0 30px 60px rgba(0,0,0,0.32), ' +
      '0 6px 14px rgba(0,0,0,0.18)',
  },
  screen: {
    position: 'relative',
    overflow: 'hidden',
  },
  statusBar: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 28,
    paddingRight: 28,
    paddingTop: 14,
    fontSize: 16,
    fontWeight: 600,
    fontFamily:
      '-apple-system, "SF Pro Text", "SF Pro Display", system-ui, sans-serif',
    fontVariantNumeric: 'tabular-nums',
    letterSpacing: 0.2,
    zIndex: 20,
    pointerEvents: 'none',
  },
  islandLayer: {
    position: 'absolute',
    left: '50%',
    transform: 'translateX(-50%)',
    background: '#000',
    borderRadius: 999,
    zIndex: 30,
    overflow: 'hidden',
    transition: 'width 240ms ease, height 240ms ease',
  },
  statusIcons: {
    display: 'flex',
    alignItems: 'center',
    gap: 7,
  },
  battery: {
    position: 'relative',
    width: 25,
    height: 12,
    border: '1px solid currentColor',
    borderRadius: 3.5,
    padding: 1.5,
    opacity: 0.85,
  },
  batteryCap: {
    position: 'absolute',
    top: 3.5,
    right: -3,
    width: 2,
    height: 5,
    background: 'currentColor',
    borderRadius: '0 1px 1px 0',
  },
  content: {
    position: 'absolute',
    left: 0,
    right: 0,
    overflow: 'auto',
  },
  homeIndicator: {
    position: 'absolute',
    bottom: 8,
    left: '50%',
    transform: 'translateX(-50%)',
    width: 134,
    height: 5,
    borderRadius: 999,
    zIndex: 10,
  },
};

function IosFrame({
  children,
  model = 'iphone15pro',     // 'iphone15pro' | 'iphone15promax'
  width,                     // override per-model default if needed
  height,
  time = '9:41',
  battery = 100,
  darkMode = false,
  showStatusBar = true,
  showDynamicIsland = true,
  showHomeIndicator = true,
  island = null,             // ReactNode rendered inside the Dynamic Island slot;
                             // omit to fall back to the static black pill.
}) {
  const spec = iosFrameModels[model] || iosFrameModels.iphone15pro;
  const screenW = width ?? spec.width;
  const screenH = height ?? spec.height;
  const textColor = darkMode ? '#ffffff' : '#1a1a1a';

  // When island content is provided, widen + lengthen the pill enough to host
  // the slot. A 220×48 floor matches the "expanded" Live Activity ergonomics
  // without prescribing layout; callers retain full control inside the slot.
  const islandW = island ? Math.max(spec.island.width, 220) : spec.island.width;
  const islandH = island ? Math.max(spec.island.height, 48) : spec.island.height;

  const batteryPct = Math.max(0, Math.min(100, battery));

  return (
    <div style={{
      ...iosFrameStyles.wrapper,
      padding: spec.bezel,
      borderRadius: spec.bodyRadius,
    }}>
      <div style={{
        ...iosFrameStyles.screen,
        width: screenW,
        height: screenH,
        borderRadius: spec.screenRadius,
        background: darkMode ? '#000000' : '#ffffff',
      }}>
        {showStatusBar && (
          <div style={{
            ...iosFrameStyles.statusBar,
            height: spec.statusBarHeight,
            color: textColor,
          }}>
            <span>{time}</span>
            <div style={iosFrameStyles.statusIcons}>
              {/* Cellular signal — four bars 4 / 7 / 10 / 13 px ascending */}
              <svg width="18" height="13" viewBox="0 0 18 13" aria-hidden="true">
                <rect x="0"  y="9" width="3" height="4"  rx="0.6" fill="currentColor" />
                <rect x="5"  y="6" width="3" height="7"  rx="0.6" fill="currentColor" />
                <rect x="10" y="3" width="3" height="10" rx="0.6" fill="currentColor" />
                <rect x="15" y="0" width="3" height="13" rx="0.6" fill="currentColor" />
              </svg>
              {/* Wi-Fi — three nested arcs + signal dot */}
              <svg width="17" height="13" viewBox="0 0 17 13" aria-hidden="true" fill="none">
                <path d="M0.5 4.2a13 13 0 0116 0"
                      stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.55" />
                <path d="M3 7.0a8 8 0 0111 0"
                      stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.85" />
                <path d="M5.5 9.7a3.5 3.5 0 016 0"
                      stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                <circle cx="8.5" cy="11.5" r="1.1" fill="currentColor" />
              </svg>
              {/* Battery */}
              <div style={{ ...iosFrameStyles.battery, color: textColor }}>
                <div style={{
                  width: `${batteryPct}%`,
                  height: '100%',
                  background: 'currentColor',
                  borderRadius: 1.5,
                }} />
                <div style={iosFrameStyles.batteryCap} />
              </div>
            </div>
          </div>
        )}

        {showDynamicIsland && (
          <div style={{
            ...iosFrameStyles.islandLayer,
            top: spec.island.top,
            width: islandW,
            height: islandH,
          }}>
            {island /* fall through to a plain black pill when null */}
          </div>
        )}

        <div style={{
          ...iosFrameStyles.content,
          top: showStatusBar ? spec.statusBarHeight : 0,
          bottom: spec.bottomInset,
        }}>
          {children}
        </div>

        {showHomeIndicator && (
          <div style={{
            ...iosFrameStyles.homeIndicator,
            background: darkMode ? 'rgba(255,255,255,0.55)' : 'rgba(0,0,0,0.42)',
          }} />
        )}
      </div>
    </div>
  );
}

if (typeof window !== 'undefined') {
  window.IosFrame = IosFrame;
  window.iosFrameModels = iosFrameModels;
}
