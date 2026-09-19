import { formatMoney, profitTone, riskLabel } from "../lib/format";
import type { Deal } from "../types/deal";

export function ProfitRiskPanel({ deal }: { deal: Deal }) {
  const { score, listing } = deal;
  return (
    <aside className="panel">
      <div className="kicker">Profit / risk</div>
      <h2 className="serif">Score {score.overall_score}</h2>
      <div className="row">
        <span>Ask</span>
        <b>{formatMoney(listing.price)}</b>
      </div>
      <div className="row">
        <span>Modeled resale</span>
        <b>{formatMoney(score.estimated_resale)}</b>
      </div>
      <div className="row">
        <span>Repairs</span>
        <b>{formatMoney(score.repair_estimate)}</b>
      </div>
      <div className="row">
        <span>Fees</span>
        <b>{formatMoney(score.fees_estimate)}</b>
      </div>
      <div className="row">
        <span>Net profit</span>
        <b className={profitTone(score.net_profit)}>{formatMoney(score.net_profit)}</b>
      </div>
      <div className="row">
        <span>Risk</span>
        <b className={score.risk_score >= 65 ? "hot" : "mid"}>
          {score.risk_score} · {riskLabel(score.risk_score)}
        </b>
      </div>
      <p className="banner">{score.rationale}</p>
      <a className="ghost" href={listing.url} target="_blank" rel="noreferrer">
        <button className="ghost" type="button">
          Open listing
        </button>
      </a>
    </aside>
  );
}
