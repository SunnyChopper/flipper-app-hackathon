import { useState } from "react";
import { cn } from "@/lib/cn";

export function ListingImage({
  src,
  alt,
  contain = true,
  className,
}: {
  src?: string;
  alt: string;
  contain?: boolean;
  className?: string;
}) {
  const [failed, setFailed] = useState(false);

  if (!src || failed) {
    return <div className={cn("bg-[#F7F8FA]", className)} aria-hidden />;
  }

  return (
    <img
      src={src}
      alt={alt}
      onError={() => setFailed(true)}
      className={cn("bg-[#F7F8FA]", contain ? "object-contain" : "object-cover", className)}
    />
  );
}
