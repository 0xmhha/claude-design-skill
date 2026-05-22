# PRE-02: Figma MCP Inventory Spike

Date: 2026-05-21
Status: 1차 spike 완료 — critical 항목 사용자 검증 대기
Source: [github.com/figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) (SHA `a742f0a` — claude-plugins-official marketplace 등록)
Server endpoint: `https://mcp.figma.com/mcp` (remote, HTTP transport)
Context: `docs/2026-05-20-validate-idea-ai-figma-context-bridge.md` 의 PRE-02 block 작업

---

## Executive Summary

**Plan A 강한 default 확정. Plan B 우선순위 ↓↓.**

| 결정 항목 | 결과 |
|-----------|------|
| **Hard gate #1** (layer rename API 지원) | ✓ PASS — `use_figma` 가 frames/components/variants/variables/text *create+modify* 모두 지원 |
| **Hard gate #7** (Authentication / permission) | ✓ PASS — `whoami` + paid plan (Professional/Org/Enterprise) 의 Dev/Full seat 필요 |
| **Plan A 진행** | 권장 — Figma 공식 MCP + plugin marketplace 의 skills 가 본 wedge 의 *대부분* 을 cover |
| **Plan B trigger** | unlikely — 잔존 unknowns 3건 (atomic / timestamp / conditional write) 모두 *fail* 이어도 client-side mitigation 가능 |

**중대한 부수 finding**:
- `generate_figma_design` tool 이 "UI 설명 → figma design 생성" 직접 path 제공 → 본 doc (d') Layer 2 (UI selection + explicit instruction) 가 *공식 흐름 그대로*
- `create_design_system_rules` tool 이 DESIGN.md 류 anti-slop rules 자동 생성 → North Star 의 brand consistency 의 *공식 지원*
- **본 wedge 가 thin 해짐** — 진짜 신규 가치는 (1) session-state cache, (2) collision detection logic, (3) globally-unique naming 강제. 나머지는 figma-power 위 thin wrapper

---

## Tool Inventory (Figma 공식 MCP)

### Read tools (rate limit 적용)

| Tool | 역할 | 본 wedge 매핑 |
|------|------|--------------|
| `get_metadata` | sparse XML node map (IDs / names / dimensions) | (d') Layer 1: layer tree 추출 baseline |
| `get_design_context` | structured React+Tailwind 표현 (layout / typography / colors / spacing) | (d') Layer 2: "어디" 의 답 — node-id 의 design data |
| `get_screenshot` | visual screenshot | D2 의 verbalization skill 의 visual aid |
| `get_variable_defs` | variables / styles (color / spacing / typography) | brand-spec align (autoplan §S1) |
| `get_code_connect_map` | Figma node ↔ code component mapping | A approach 의 sub-feature |
| `get_code_connect_suggestions` | Code Connect 매핑 추천 | A approach |
| `get_figjam` | FigJam → XML | scope 밖 |
| `whoami` | auth identity + plan info | permission check |

### Write tools (rate limit *exempt*, 현재 무료 beta — 향후 paid)

| Tool | 역할 | 본 wedge 매핑 |
|------|------|--------------|
| **`use_figma`** | **pages/frames/components/variants/variables/styles/text/images 의 create+modify** (Design files) / boards/stickies/sections/connectors/shapes/tables (FigJam) | **(d') Layer 3 의 hard gate — layer rename 의 superset** |
| **`generate_figma_design`** | **UI 설명 → figma design layers 변환** | **(d') Layer 2 직격 — "어떻게" 의 prompt 가 figma 에 자동 적용** |
| `create_new_file` | 새 Design/FigJam file 생성 | scope (단일 file trial) |
| `upload_assets` | PNG/JPG/GIF/WebP 업로드 (max 10MB) | brand asset import |
| `create_design_system_rules` | 프로젝트별 design system rules 파일 생성 | **North Star 의 anti-slop 가드레일 자동 생성** |
| `add_code_connect_map` | Code Connect 매핑 생성 | A approach |
| `send_code_connect_mappings` | 매핑 확정 | A approach |
| `generate_diagram` | Mermaid → FigJam diagram | scope 밖 |

---

## 9 Inventory Items 결과

| # | Item | 결과 | Gate type | Plan B trigger? |
|---|------|------|-----------|------------------|
| 1 | Layer rename API (element type 별) | **✓ PASS** — `use_figma` 가 frame/group/component/variant/variable/style/text 모두 지원 | hard | No |
| 2 | Layer 추가 / 삭제 / re-parent | ✓ PASS — `use_figma` 가 create+modify 명시 | soft | No |
| 3 | Atomic guarantee (batch all-or-nothing / 자동 rollback) | **? 미명시** — 공식 docs 에 transaction semantics 부재 | soft | **No** — autoplan D-01 의 verify+diff log mitigation 충분 |
| 4 | Timestamp granularity (file / page / layer) | **? 미명시** — modification time 조회 가능 여부 / granularity 둘 다 명시 안 됨 | soft | **No** — D3 의 scan-on-restart 가 file-level timestamp 만 있어도 작동 (page 단위 충돌 detection 은 layer name 비교로 fallback 가능) |
| 5 | Conditional write (if-match / optimistic concurrency) | **? 미명시** — ETag / version 기반 conditional write 미명시 | soft | **No** — D3-Q2 α (CLI lock) 가 이 미지원 가정 위에서 작동 |
| 6 | Read consistency / 1000+ element latency | partial — `get_metadata` (sparse) + `get_design_context` (full) 분리. *large selection* 시 truncated 경고 + `get_metadata` 우선 → 부분 fetch 권장 | soft | No |
| 7 | Authentication / permission model | ✓ PASS — `whoami` + paid plan 의 Dev/Full seat 필요 / Starter+View+Collab seat = 월 6 call only | hard for B | No (단 ICP 가 paid plan 가정) |
| 8 | Rate limit / API cost | Tier 1 REST API rate limits (Dev/Full seat 의 paid plan). Write tools 는 rate limit exempt (현재 무료 beta, 향후 paid) | soft | No |
| 9 | Plugin vs MCP capability 차이 | Figma 공식 plugin (`claude plugin install figma@claude-plugins-official`) = MCP server + 8 skills + rules. *공식 plugin 이 wedge 의 대부분 cover* | Plan B 평가 | **Plan B 우선순위 ↓↓** |

---

## 본 doc (d') Wedge 와의 매핑

### Layer 1: Session state resolution

- **Figma 공식 지원**: partial
  - `get_metadata` + `get_design_context` 로 현재 layer tree 추출 가능
  - Session state cache 는 *client 측 책임* (claude-design-skill 측)
- **신규 구현 필요**: ⚠️ session 관리 logic (5분 TTL, explicit reset, scan-on-restart) 은 claude-design-skill 안에서

### Layer 2: UI selection + explicit instruction *(핵심 layer — D2 grilling finding)*

- **Figma 공식 지원**: ✓ STRONG MATCH
  - 사용자 가 figma 에서 node 선택 → URL 의 node-id 가 자동 포함
  - `get_design_context(node_id)` 가 "어디" 에 대한 정확 답
  - prompt 의 사용자 설명 = "어떻게"
  - `generate_figma_design` 으로 prompt → figma 자동 변환 path 존재
- **신규 구현 필요**: ✓ 거의 zero — 공식 흐름 그대로

### Layer 3: Naming convention + collision disambiguation

- **Figma 공식 지원**: partial
  - `use_figma` 로 layer rename 가능 (hard gate PASS)
  - Naming pattern 강제 = *prompt + rules* (DESIGN.md / Cursor rules / Claude Code rules) 로 가능
  - **Collision detection logic 은 client 측 책임** — 공식 미지원
- **신규 구현 필요**: ⚠️ collision detector + globally-unique naming 강제 enforcement + visual disambiguation prompt-back (CLI 텍스트 알림 형식, D3 grilling finding)

---

## 잔존 unknowns (사용자 검증 또는 추가 spike 필요)

다음 3 항목은 공식 docs 에 명시 안 됨. *각각 mitigation 있어 Plan A 진행에 영향 없음*, 단 client-side 설계에 영향.

### U-01 — Atomic batch write 의 보장 수준

- 가능성 1: `use_figma` 한 호출에 multi-layer 변경 전송 → server 가 internal transaction 처리 → all-or-nothing
- 가능성 2: 호출별 individual op → partial failure 가능 → autoplan D-01 의 verify+diff log + rollback 필요
- **검증 방법**: 사용자 직접 실행 — multi-layer rename 한 호출에 보내고 일부러 invalid layer id 섞어 reject 시 다른 layer 가 commit 됐는지 확인
- **mitigation**: 두 가능성 모두 autoplan D-01 의 verify+diff log + rollback script 가 cover

### U-02 — Modification timestamp 조회 가능 여부 + granularity

- `get_metadata` 또는 `get_design_context` 의 응답에 *timestamp* 필드가 포함되는지 미명시
- 가능성 1: file-level lastModified 만 — 다른 페이지 변경에도 본인 페이지 scan 강제 (false positive)
- 가능성 2: layer-level lastModified 지원 — D3 의 scan-on-restart 가 fine-grained 작동
- **검증 방법**: 실제 응답 inspect — JSON payload 에 lastModified / version 필드 있는지
- **mitigation**: file-level 만 지원이어도 page 단위 collision detector (사용자 D3 finding) 가 fallback 작동

### U-03 — Conditional write (optimistic concurrency)

- if-match / expected-version 의 header 또는 parameter 가 `use_figma` 에 있는지 미명시
- **검증 방법**: tool 의 input schema 정밀 inspect (Anthropic 공식 plugin install 후 schema 조회)
- **mitigation**: 미지원이어도 D3-Q2 α (CLI lock) + scan-on-restart 가 multi-device race 처리. multi-user concurrent write 는 month-3+ defer (사용자 D3 finding)

---

## Plan A vs Plan B 결정

### Plan A (default 진행 권장)

- effort 추정: autoplan B approach 의 M (2-4 주) 유지
- 인프라: Figma 공식 MCP server (`https://mcp.figma.com/mcp`) + claude-plugins-official 의 figma plugin
- 신규 구현 영역: session-state cache + collision detector + naming convention 강제 layer
- distribution: claude-design-skill sub-skill (autoplan A-02 결정 유지)

### Plan B (fallback — 현재 trigger 조건 미충족)

- Trigger 조건: hard gate #1 또는 #7 fail. **둘 다 PASS** → Plan B trigger 안 됨
- 단 *향후* paid 가격이 ICP 의 affordability 위반 시 *부분 fallback* 가능: write tool 의 self-host 대안

---

## 본 doc 의 wedge sharpness 재평가 *(중요)*

### 신규 통찰

본 spike 가 **wedge 의 thin 화** 노출:

- (d') 의 *대부분* 이 Figma 공식 도구 위 thin wrapper
- 신규 가치 영역 = 3 piece:
  1. *Session state 관리* (cache + 5min TTL + scan-on-restart)
  2. *Collision detection logic* (globally-unique naming 강제)
  3. *Visual disambiguation prompt-back* (CLI 텍스트 알림 — D3 grilling finding)

### 의미

**Pros**:
- effort 추정 *축소 가능* — A approach 의 3-5일 ship 이 더 빨라질 수 있음 (Figma 공식 tool 직접 사용으로 자체 구현 영역 감소)
- claude-code marketplace 에서 figma 공식 plugin 과 *complementary* — 충돌 아닌 보강

**Cons**:
- **differentiation 약화** — figma 가 *대부분* cover. 본 wedge 가 "주변 friction 제거" 수준으로 narrow
- 본 doc P3 (wedge) 의 가치 명제가 *재산정* 필요할 수 있음 — 사용자 confirm 필요

### 결정 권장

본 spike 결과를 본 doc 에 *finding* 으로 추가 + wedge 가치 명제의 *재산정 session* 별도 진행 권장.

특히:
- "claude-design-skill 의 신규 가치 = session/collision/naming 의 *3 piece thin wrapper*" 라는 reframe 이 본 doc P3 의 *진짜 정확* 표현
- 이 reframe 후에도 paid commitment 가설 (Series A 디자인 팀 의 per-seat $39/mo) 가 valid 한지 = 다음 grilling 또는 trial 데이터 검증

---

## 사용자 검증 요청 항목 (critical)

1. **paid plan 보유 확인** — ICP (Series A 디자인 팀) 가 Professional/Org/Enterprise plan + Dev/Full seat 보유 가정 정확한지
2. **U-01 atomic write 검증** — 직접 multi-layer rename 호출에 invalid id 섞어 partial failure 행동 확인
3. **U-02 timestamp 검증** — `get_metadata` / `get_design_context` 응답 JSON 에 lastModified 또는 version 필드 inspect
4. **wedge sharpness 재산정 동의 여부** — 본 doc P3 의 가치 명제를 *3 piece thin wrapper* 로 reframe 진행 권장

---

## 다음 단계

- **A**: 사용자가 위 4 검증 항목 (paid plan / U-01 / U-02 / wedge reframe) 답변
- **B**: 본 doc 의 assumption_ledger 업데이트 (Plan B trigger confidence: low / Figma MCP 지원 범위 confidence: high)
- **C**: PRE-01 (Anchor-A 미팅 + 1-week trial) 진행 — PRE-02 의 답이 *Plan A 진행* 으로 unblock 됨
- **D**: PRE-01/PRE-02 모두 완료 후 `/buddy:plan-build` 진입 — A approach 의 3-5일 task graph

---

## References

- [Figma MCP Server Guide (claude-plugins-official source)](https://github.com/figma/mcp-server-guide)
- [Figma MCP Developer Docs](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)
- [Anthropic Claude Code Plugins](https://claude.com/blog/claude-code-plugins)
