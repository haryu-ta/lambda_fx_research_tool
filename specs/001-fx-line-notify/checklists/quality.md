# Requirements Quality Checklist: 為替レート LINE 通知

**Purpose**: 仕様記述の完全性・明確性・整合性を、PRレビュー観点で検証する
**Created**: 2026-05-16
**Feature**: [spec.md へのリンク](../spec.md)

## Requirement Completeness

- [ ] CHK001 通常通知と障害通知の両方について、通知対象（誰に送るか）が要件として明示されているか？ [Completeness, Spec §機能要件]
- [ ] CHK002 障害種別ごとの通知文言（為替API実行NG / 為替情報取得できず / 為替情報取得NG）が、網羅的に定義されているか？ [Completeness, Spec §エッジケース, Spec §FR-011〜FR-014]
- [ ] CHK003 成功時・失敗時それぞれで、実行終了条件（成功終了/失敗終了）が明示されているか？ [Completeness, Spec §ユーザーストーリー1-2, Spec §FR-007]
- [ ] CHK004 自動再実行しない方針について、適用範囲（どの起動経路か）が要件で明示されているか？ [Completeness, Spec §FR-015]

## Requirement Clarity

- [ ] CHK005 「有効な USD/JPY 数値」の判定基準（型、桁数、欠損条件）が明確化されているか？ [Clarity, Ambiguity, Spec §エッジケース]
- [ ] CHK006 「無料プラン互換」の判定基準（料金条件、制限条件）が明確化されているか？ [Clarity, Ambiguity, Spec §FR-002]
- [ ] CHK007 「5分以内」の起点と終点（トリガー時刻基準か、失敗検知時刻基準か）が定義されているか？ [Clarity, Spec §SC-005]
- [ ] CHK008 「認証情報が未設定または空文字」の対象キー範囲（為替API/LINE/APIキー等）が明示されているか？ [Clarity, Spec §FR-008, Spec §FR-014]

## Requirement Consistency

- [ ] CHK009 ユーザーストーリー2の受け入れシナリオと FR-011〜FR-015 に矛盾がないか？ [Consistency, Spec §ユーザーストーリー2, Spec §FR-011〜FR-015]
- [ ] CHK010 「リトライしない」方針と「失敗時通知送信」要件が競合しないよう、優先順序が定義されているか？ [Consistency, Conflict, Spec §エッジケース, Spec §FR-013, Spec §FR-015]
- [ ] CHK011 SC-001（通知1件）と障害時通知要件（FR-011〜FR-014）の適用条件が整合しているか？ [Consistency, Conflict, Spec §SC-001, Spec §FR-011〜FR-014]

## Acceptance Criteria Quality

- [ ] CHK012 各 FR に対して、客観的に合否判定できる受け入れ条件が存在するか？ [Acceptance Criteria, Gap]
- [ ] CHK013 SC-002/SC-005 の達成判定に必要な計測方法（ログ項目・時刻ソース）が定義されているか？ [Measurability, Spec §SC-002, Spec §SC-005]
- [ ] CHK014 「重複配信を発生させない」が観測可能な判定条件として定義されているか？ [Measurability, Spec §FR-015]

## Scenario Coverage

- [ ] CHK015 Primary（通常為替取得→通知）シナリオが、前提・操作・結果の3点で欠落なく定義されているか？ [Coverage, Spec §ユーザーストーリー1]
- [ ] CHK016 Exception（為替API失敗、LINE API失敗、認証欠落、無効数値）シナリオが、個別に区別され定義されているか？ [Coverage, Spec §ユーザーストーリー2, Spec §エッジケース]
- [ ] CHK017 Recovery（失敗後の次回実行への影響）に関する要件が明示されているか、または意図的に除外されているか？ [Coverage, Gap]

## Edge Case Coverage

- [ ] CHK018 スロットリング時の「非リトライ」方針が、将来の拡張（手動再送等）との境界を含めて定義されているか？ [Edge Case, Spec §FR-013]
- [ ] CHK019 送信完了直前タイムアウト時の通知欠損許容方針について、業務影響の許容条件が定義されているか？ [Edge Case, Assumption, Spec §エッジケース]
- [ ] CHK020 同一時刻に複数イベントが競合した場合の重複判定方針が定義されているか？ [Edge Case, Gap]

## Non-Functional Requirements

- [ ] CHK021 構造化ログ要件に、必須フィールド（実行ID、連携先、失敗理由、時刻）が明示されているか？ [Non-Functional, Spec §FR-005, Spec §FR-006]
- [ ] CHK022 セキュリティ要件として、秘匿情報のマスキング/非出力方針が明示されているか？ [Non-Functional, Gap, Spec §FR-008]
- [ ] CHK023 可用性要件として、外部依存障害時の期待運用品質（許容欠損率等）が定義されているか？ [Non-Functional, Gap]

## Dependencies & Assumptions

- [ ] CHK024 無料為替APIの利用制限（回数/秒間制限）の前提が、運用頻度と整合する形で検証可能に記述されているか？ [Dependency, Spec §前提]
- [ ] CHK025 LINE通知先が1宛先である前提が、将来変更時の影響範囲とともに明示されているか？ [Assumption, Spec §前提]

## Ambiguities & Conflicts

- [ ] CHK026 「通知配信呼び出しが失敗」の定義が、LINE Messaging API 呼び出し失敗と明記されているか？ [Ambiguity, Spec §ユーザーストーリー2]
- [ ] CHK027 時刻表記（HH:MM）のタイムゾーン基準が、通常通知と障害通知で一貫してJSTに固定されているか？ [Conflict, Spec §FR-003, Spec §FR-009, Spec §FR-011〜FR-014]
- [ ] CHK028 要件ID（FR/SC）間の参照整合が保たれ、欠番や重複がないか？ [Traceability, Spec §機能要件, Spec §成功基準]

## Notes

- このチェックリストは「実装の正しさ」ではなく「要件文書の品質」を検査する。
- 実装手順、テストコード、API呼び出し手順の検証項目は対象外とする。
