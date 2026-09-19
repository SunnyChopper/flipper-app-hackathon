import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import type { ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/cn";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-btn text-[13px] font-medium transition duration-150 disabled:pointer-events-none disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-primary/40",
  {
    variants: {
      variant: {
        primary: "h-10 bg-primary px-4 text-white hover:bg-primary-hover hover:-translate-y-px",
        secondary: "h-10 bg-[#f2f4f7] px-4 text-foreground hover:bg-[#e8ebf0]",
        outline: "h-10 border border-border bg-white px-4 text-foreground hover:border-border-strong hover:bg-[#fafafa]",
        ghost: "h-10 px-3 text-foreground hover:bg-surface-secondary",
        danger: "h-10 px-3 text-muted hover:bg-danger-soft hover:text-danger",
        icon: "h-10 w-10 text-muted hover:bg-surface-secondary hover:text-foreground",
      },
    },
    defaultVariants: {
      variant: "primary",
    },
  },
);

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  };

export function Button({ className, variant, asChild, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn(buttonVariants({ variant }), className)} {...props} />;
}
