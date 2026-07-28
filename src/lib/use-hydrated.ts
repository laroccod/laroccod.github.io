"use client";

import { useSyncExternalStore } from "react";

/** The value never changes after hydration, so there is nothing to subscribe
 * to; React only needs the unsubscribe function to exist. */
const subscribe = () => () => {};

/** False while server-rendering and during the first client render, true
 * afterwards. Lets a component defer browser-only output (platform, stored
 * theme) until after hydration without setting state inside an effect, which
 * would cascade an extra render. */
export function useHydrated(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => true,
    () => false,
  );
}
