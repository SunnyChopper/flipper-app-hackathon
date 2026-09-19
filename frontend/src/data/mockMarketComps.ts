import type { MarketComp } from "../types/opportunity";

export const iphoneComps: MarketComp[] = [
  {
    id: "iphone-comp-1",
    title: "iPhone 15 Pro 256GB",
    price: 620,
    marketplace: "eBay",
    imageUrl: "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=200&q=80",
  },
  {
    id: "iphone-comp-2",
    title: "iPhone 15 Pro 256GB",
    price: 649,
    marketplace: "Swappa",
    imageUrl: "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=200&q=80",
  },
  {
    id: "iphone-comp-3",
    title: "iPhone 15 Pro 256GB",
    price: 675,
    marketplace: "Marketplace",
    imageUrl: "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=200&q=80",
  },
];

export const genericComps = (title: string, prices: number[], marketplace = "eBay"): MarketComp[] =>
  prices.map((price, index) => ({
    id: `${title}-${price}-${index}`,
    title,
    price,
    marketplace: index === 1 ? "Swappa" : marketplace,
  }));
