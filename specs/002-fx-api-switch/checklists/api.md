# API Checklist: 為替API切替

**Purpose**: Open Exchange Rates への切替要件が、実装前に十分な品質（完全性・明確性・一貫性・測定可能性）を満たしているかを検証する
**Created**: 2026-05-30
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [ ] CHK001 Open Exchange Rates の認証要件（app_id の取得元・設定箇所・必須性）は明示されているか？ [Completeness, Spec §FR-001]
- [ ] CHK002 `USD/JPY` 取得要件に、利用するレスポンス項目（`rates.JPY`）が明示されているか？ [Completeness, Spec §FR-004]
- [ ] CHK003 API切替の対象外範囲（EventBridge/LINEインターフェース変更禁止）は、機能境界として十分に記述されているか？ [Completeness, Spec §FR-006]
- [ ] CHK004 成功基準（Success Criteria）セクションに、API切替後の達成条件が定義されているか？ [Gap, Spec §Success Criteria]

## Requirement Clarity

- [ ] CHK005 「更新頻度が高い」の判定基準（比較対象・最小更新頻度・許容遅延）は定量化されているか？ [Clarity, Ambiguity, Spec §User Story 1]
- [ ] CHK006 「既存成功通知フォーマットを維持する」の許容差分（改行・空白・丸め規則）は明示されているか？ [Clarity, Spec §FR-002]
- [ ] CHK007 「JSONとして処理する」の完了条件（必須キー欠落時の扱いを含む）は明確か？ [Clarity, Spec §FR-004]

## Requirement Consistency

- [ ] CHK008 失敗時通知文言の維持要件は、Edge Cases の失敗シナリオ記述と矛盾なく整合しているか？ [Consistency, Spec §FR-003]
- [ ] CHK009 「自動再試行を有効化しない」要件は、運用前提と矛盾なく一貫しているか？ [Consistency, Spec §FR-007]
- [ ] CHK010 API切替のスコープ説明（概要）と機能要件（FR-001〜FR-007）の責務境界は一致しているか？ [Consistency, Spec §Overview, Spec §FR-001-007]

## Acceptance Criteria Quality

- [ ] CHK011 各 FR に対して「合否を客観判定できる受け入れ条件」が定義されているか？ [Acceptance Criteria, Gap]
- [ ] CHK012 成功基準は時間・割合・件数などの測定可能な単位で記述されているか？ [Measurability, Gap, Spec §Success Criteria]
- [ ] CHK013 ユーザーストーリー1の独立テストは、第三者が同一手順で再現可能な粒度で定義されているか？ [Acceptance Criteria, Spec §User Story 1]

## Scenario Coverage

- [ ] CHK014 Primaryシナリオ（正常取得→通知）に対して、前提条件と期待結果が不足なく定義されているか？ [Coverage, Spec §User Story 1]
- [ ] CHK015 Exceptionシナリオ（API障害・データ欠落・タイムアウト）の要求はすべて明示されているか？ [Coverage, Spec §Edge Cases]
- [ ] CHK016 Recoveryシナリオ（障害復旧後に通常通知へ戻る条件）は要件として必要か、または意図的に除外と明記されているか？ [Gap, Coverage]

## Edge Case Coverage

- [ ] CHK017 HTTP 200 かつ `rates` オブジェクト自体が欠落するケースの扱いは明記されているか？ [Edge Case, Gap, Spec §Edge Cases]
- [ ] CHK018 `rates.JPY` が文字列・null・負値の場合の境界条件と通知要件は定義されているか？ [Edge Case, Spec §FR-004]

## Non-Functional Requirements

- [ ] CHK019 API切替後の性能要件（例: 通知完了までの時間閾値）は仕様に明示されているか？ [Non-Functional, Gap]
- [ ] CHK020 観測可能性要件（ERRORログに必須フィールド、イベント種別、相関ID）は検証可能な形で規定されているか？ [Non-Functional, Spec §FR-005]

## Dependencies & Assumptions

- [ ] CHK021 Open Exchange Rates 無料プラン前提が破綻した場合の扱い（要件変更条件・制約）は定義されているか？ [Assumption, Spec §Assumptions]
- [ ] CHK022 既存 EventBridge/LINE 経路を流用する前提に対して、変更発生時の責任範囲は明示されているか？ [Dependency, Spec §FR-006, Spec §Assumptions]

## Ambiguities & Conflicts

- [ ] CHK023 「通知鮮度改善」の期待値は、Success Criteria 欠落と矛盾せず評価可能になっているか？ [Ambiguity, Conflict, Gap]
- [ ] CHK024 API仕様変更（レスポンス項目追加・型変更）時の要件レベルの追従方針は定義されているか？ [Ambiguity, Gap]

## Notes

- 本チェックリストは実装動作のテストではなく、要件記述の品質検証を目的とする。
- [Gap] は仕様に不足する要求の追記対象を示す。
