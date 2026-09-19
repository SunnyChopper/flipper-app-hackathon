const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

export function formatMoney(value: number): string {
  return money.format(value);
}

export function profitTone(profit: number): "up" | "down" {
  return profit >= 0 ? "up" : "down";
}

export function riskLabel(score: number): string {
  if (score < 35) return "Low risk";
  if (score < 65) return "Watch it";
  return "High risk";
}
