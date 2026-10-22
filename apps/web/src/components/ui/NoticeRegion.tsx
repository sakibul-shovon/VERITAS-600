"use client";

interface NoticeRegionProps {
  message?: string;
  onDismiss?: () => void;
}

export default function NoticeRegion({ message, onDismiss }: NoticeRegionProps) {
  if (!message) return null;
  return <div className="notice-region" role="status" aria-live="polite"><span>{message}</span>{onDismiss && <button type="button" onClick={onDismiss} aria-label="Dismiss message">Dismiss</button>}</div>;
}
