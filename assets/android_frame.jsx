/**
 * AndroidFrame — Pixel 8 / Pixel 8 Pro device frame
 *
 * Aligned to real Pixel 8 series specs:
 *   - Pixel 8     · CSS 412 × 915 logical px · 6.2" display
 *   - Pixel 8 Pro · CSS 448 × 997 logical px · 6.7" display
 *
 * Includes (do NOT redraw any of these in your screen content):
 *   - Body bezel + corner radius
 *   - Punch-hole front camera (centered top, 13×13 logical px, 9 px from top)
 *   - Material 3 status bar (36 px high, time left, signal/wifi/battery right)
 *   - Gesture-nav indicator (72 × 4 px, centered, 16 px from bottom)
 *   - 3-button nav alternative (◁ ○ □)
 *   - Content area sized so first row never sits under the punch-hole
 *
 * Usage:
 *   <AndroidFrame time="9:41" battery={85}>
 *     <YourAppContent />
 *   </AndroidFrame>
 *
 *   <AndroidFrame model="pixel8pro" darkMode navStyle="buttons">
 *     <YourAppContent />
 *   </AndroidFrame>
 */

const androidFrameModels = {
  pixel8: {
    width: 412,
    height: 915,
    bodyRadius: 30,
    screenRadius: 22,
    bezel: 8,
  },
  pixel8pro: {
    width: 448,
    height: 997,
    bodyRadius: 32,
    screenRadius: 24,
    bezel: 8,
  },
};

const androidFrameStyles = {
  wrapper: {
    display: 'inline-block',
    background: '#1a1a1a',
    boxShadow: '0 0 0 2px #2a2a2a, 0 20px 60px rgba(0,0,0,0.3)',
    position: 'relative',
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
    height: 36,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 24,
    paddingRight: 24,
    fontSize: 14,
    fontWeight: 500,
    fontFamily: 'Roboto, "Google Sans", -apple-system, sans-serif',
    fontVariantNumeric: 'tabular-nums',
    zIndex: 20,
    pointerEvents: 'none',
  },
  punchHole: {
    position: 'absolute',
    top: 9,
    left: '50%',
    transform: 'translateX(-50%)',
    width: 13,
    height: 13,
    background: '#000',
    borderRadius: '50%',
    zIndex: 30,
  },
  statusIcons: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  batteryText: {
    fontSize: 11,
    fontWeight: 600,
    marginLeft: 2,
    fontVariantNumeric: 'tabular-nums',
  },
  content: {
    position: 'absolute',
    top: 36,        // below status bar; punch-hole sits inside status bar at center
    left: 0,
    right: 0,
    bottom: 24,     // leave room for gesture nav / 3-button bar
    overflow: 'auto',
  },
  navBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 24,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 60,
    zIndex: 10,
  },
  gestureIndicator: {
    width: 72,
    height: 4,
    borderRadius: 999,
    marginBottom: 8,
  },
};

function AndroidFrame({
  children,
  model = 'pixel8',          // 'pixel8' | 'pixel8pro'
  width,                     // override per-model default if needed
  height,
  time = '9:41',
  battery = 100,
  darkMode = false,
  navStyle = 'gesture',      // 'gesture' | 'buttons'
}) {
  const spec = androidFrameModels[model] || androidFrameModels.pixel8;
  const screenW = width ?? spec.width;
  const screenH = height ?? spec.height;
  const textColor = darkMode ? '#fff' : '#1a1a1a';

  return (
    <div style={{
      ...androidFrameStyles.wrapper,
      padding: spec.bezel,
      borderRadius: spec.bodyRadius,
    }}>
      <div style={{
        ...androidFrameStyles.screen,
        width: screenW,
        height: screenH,
        borderRadius: spec.screenRadius,
        background: darkMode ? '#000' : '#fff',
      }}>
        {/* Status bar (Material 3, 36 px) — leaves the punch-hole visible at center */}
        <div style={{ ...androidFrameStyles.statusBar, color: textColor }}>
          <span>{time}</span>
          <div style={androidFrameStyles.statusIcons}>
            {/* signal bars */}
            <svg width="14" height="10" viewBox="0 0 14 10" fill="currentColor" aria-hidden="true">
              <rect x="0" y="6" width="2" height="4" rx="0.5" />
              <rect x="4" y="4" width="2" height="6" rx="0.5" />
              <rect x="8" y="2" width="2" height="8" rx="0.5" />
              <rect x="12" y="0" width="2" height="10" rx="0.5" />
            </svg>
            {/* wifi */}
            <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">
              <path d="M7 9a1 1 0 100-2 1 1 0 000 2z" fill="currentColor" />
              <path d="M3 6a5 5 0 018 0" stroke="currentColor" strokeWidth="1.2" />
              <path d="M0.5 3.5a11 11 0 0113 0" stroke="currentColor" strokeWidth="1.2" opacity="0.6" />
            </svg>
            {/* battery */}
            <div style={{
              width: 22,
              height: 10,
              border: '1.5px solid currentColor',
              borderRadius: 2,
              padding: 1,
              position: 'relative',
            }}>
              <div style={{
                width: `${battery}%`,
                height: '100%',
                background: 'currentColor',
                borderRadius: 1,
              }} />
            </div>
            <span style={androidFrameStyles.batteryText}>{battery}%</span>
          </div>
        </div>

        {/* Front camera punch-hole (Pixel 8: 13×13 px, top:9, centered horizontally) */}
        <div style={androidFrameStyles.punchHole} />

        {/* Content area — starts at top:36 so first row never overlaps punch-hole */}
        <div style={androidFrameStyles.content}>
          {children}
        </div>

        {navStyle === 'gesture' && (
          <div style={androidFrameStyles.navBar}>
            <div style={{
              ...androidFrameStyles.gestureIndicator,
              background: darkMode ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.4)',
            }} />
          </div>
        )}

        {navStyle === 'buttons' && (
          <div style={{ ...androidFrameStyles.navBar, gap: 56 }}>
            <span style={{ color: textColor, fontSize: 20, opacity: 0.7 }}>◁</span>
            <span style={{ color: textColor, fontSize: 16, opacity: 0.7 }}>○</span>
            <span style={{ color: textColor, fontSize: 16, opacity: 0.7 }}>□</span>
          </div>
        )}
      </div>
    </div>
  );
}

if (typeof window !== 'undefined') {
  window.AndroidFrame = AndroidFrame;
}
