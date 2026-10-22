"use client";

export default function GlobalError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <main className="route-error" role="alert"><p>VERITAS—600</p><h1>This view could not be prepared.</h1><span>The decision engine has not been changed. Try loading this view again.</span><button onClick={reset}>Try again</button></main>;
}
