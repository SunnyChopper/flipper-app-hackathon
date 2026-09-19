import { create } from "zustand";

type ToastState = {
  message: string | null;
  show: (message: string) => void;
};

let timeout: number | undefined;

export const useToastStore = create<ToastState>((set) => ({
  message: null,
  show: (message) => {
    window.clearTimeout(timeout);
    set({ message });
    timeout = window.setTimeout(() => set({ message: null }), 2200);
  },
}));
